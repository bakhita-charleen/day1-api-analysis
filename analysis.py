"""
Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization - Data Science, AI & Analytics
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_DIR = Path("output")

# To test error handling, temporarily set API_URL to a bad address,
# e.g. ".../usersABC" (404) or "https://lllll.invalid".

def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}")
            return []
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Could not reach the API: {e}")
        return []


def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    for key, value in record.items():
        print("  " * indent + f"{key}: {type(value).__name__}")
        if isinstance(value, dict):
            explore(value, indent + 1)


def get_tld(email: str) -> str:
    """Return the top-level domain of an email address, e.g. 'biz'."""
    # text after "@", then the part after the last "."
    return email.split("@")[1].split(".")[-1]


def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    rows = []
    for c in customers:
        row = {
            "customer_id": c["id"],
            "name": c["name"],
            "username": c["username"],
            "email": c["email"],
            "email_domain": get_tld(c["email"]),
            "phone": c["phone"],
            "city": c["address"]["city"],
            "zipcode": c["address"]["zipcode"],
            "latitude": float(c["address"]["geo"]["lat"]),
            "longitude": float(c["address"]["geo"]["lng"]),
            "company": c["company"]["name"],
            "website": c["website"]
        }
        rows.append(row)
    return rows


def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    return {c["address"]["city"] for c in customers}


def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop and/or a dict comprehension (no Counter, no pandas)."""
    counts = {}
    for c in customers:
        city = c["address"]["city"]
        if city in counts:
            counts[city] += 1 # seen before: add one
        else:
            counts[city] = 1 #appearing for the first time: start at one
    return counts


def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email top-level domain (e.g. 'biz', 'tv')."""
    tlds = [get_tld(c["email"]) for c in customers] # one TLD per customer
    return {tld: tlds.count(tld) for tld in set(tlds)} # set() so each TLD is counted once


def sort_counts(counts: dict[str, int]) -> list[tuple[str, int]]:
    """Sort counts from most to least common, ties broken alphabetically."""
    # -pair[1] puts bigger counts first; pair[0] breaks ties A to Z
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))


def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    """Convert the flat rows into a pandas DataFrame."""
    return pd.DataFrame(rows)


def plot_distribution(counts: dict[str, int], path: Path,
                      title: str = "Customer distribution",
                      xlabel: str = "Category") -> None:
    """Save a labelled bar chart of the distribution to path."""
    ordered = sort_counts(counts)
    labels = [name for name, _ in ordered]
    values = [number for _, number in ordered]


    plt.figure(figsize=(8, 5)) #sets the size of the picture.
    plt.bar(labels, values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Number of customers")
    plt.xticks(rotation=45, ha="right") #tilts the city names so they don’t overlap
    plt.tight_layout() #stops the tilted labels being cut off
    plt.savefig(path)
    plt.close() # clears the figure, so the second chart doesn’t draw on top of the first.


if __name__ == "__main__":

    # Creating an output directory.
    OUTPUT_DIR.mkdir(exist_ok=True)

    print()
    print("-" * 50)

    # Task 1: fetch the data and stop early if it failed
    customers = get_customers()
    if not customers:
        print("No customer data retrieved. Stopping.")
        raise SystemExit(1)

    # Task 2: explore the structure of one record
    print("Structure of one customer record:")
    explore(customers[0])
    print()
    print("-" * 50)

    # Task 3: flatten the records
    rows = extract_attributes(customers)

    # Tasks 4:  unique cities and counts
    cities = unique_cities(customers)
    by_city = city_counts(customers)
    by_domain = email_domain_counts(customers)

    # Task 5: print the city counts most to least common
    print("Customers per city (most to least common):")
    print(dict(sort_counts(by_city)))
    print()
    print("-" * 50)

    # Task 6: DataFrame and check pandas agrees with the hand-written counts
    df = to_dataframe(rows)
    print("DataFrame shape:", df.shape)
    print(df.dtypes)
    print("City counts match pandas:", by_city == df["city"].value_counts().to_dict())
    print("Domain counts match pandas:", by_domain == df["email_domain"].value_counts().to_dict())
    print()
    print("-" * 50)

    # Task 7: export CSVs
    df.to_csv(OUTPUT_DIR / "customers.csv", index=False)
    city_pairs = sort_counts(by_city)
    pd.DataFrame(city_pairs, columns=["city", "customer_count"]).to_csv(
        OUTPUT_DIR / "city_counts.csv", index=False
    )

    # Task 8: charts
    plot_distribution(by_city, OUTPUT_DIR / "customer_distribution.png",
                      title="Customers by city", xlabel="City")
    plot_distribution(by_domain, OUTPUT_DIR / "email_domain_distribution.png",
                      title="Customers by email domain", xlabel="Email domain (TLD)")

    # Findings summary 
    top_city, top_count = city_pairs[0]
    print(f"Customers retrieved : {len(customers)}")
    print(f"Unique cities       : {len(cities)}")
    print(f"Most common city    : {top_city} ({top_count})")
    print(f"Email domains       : {dict(sort_counts(by_domain))}")
    print(f"Chart saved to      : {OUTPUT_DIR / 'customer_distribution.png'}")

    
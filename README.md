# Day 1: API Data Analysis

## Approach

**Task 1:** `get_customers` fetches the data with a 10-second timeout. It checks the status code for server-side errors (like 404) and uses try/except for network failures/ bad domains etc. In both cases it prints a clear message and returns an empty list so later functions don't crash.

**Task 2:** `explore` walks one customer record recursively. For each key it prints the name and the Python type, indented by depth. If a value is a dictionary, the function calls itself on it, that is, it runs explore on that inner dictionary to obtain individual keys. Values that are not dictionaries stop the recursion.

Nested attributes:
- `address` is a dictionary that has the information: (street, suite, city, zipcode, geo)
- `geo` is a dictionary inside `address` that houses (lat, lng)
- `company` is a dictionary that has the information: (name, catchPhrase, bs)

The deepest values are `lat` and `lng`, that are reached using `customer["address"]["geo"]["lat"]`. They arrive stored as strings so they need conversion to floats.

**Task 3:** `extract_attributes` flattens each nested customer record into one dictionary with 12 keys. 
Nested values are reached by chaining keys (for example `c["address"]["geo"]["lat"]`) to obtain the latitude. 
Latitude and longitude arrive from the API stored as strings, so they are converted with `float()`. 
The email domain is the TLD(Top level domain), worked out by the helper `get_tld`.
In the case of an email like johndoe@gmail.com: johndoe is the username, gmail.com is the domain and .com is now the top level domain(TLD).

**Task 4:** `unique_cities` uses a set comprehension to collect each distinct city. 
There are 10 unique cities for 10 customers, so no two customers share a city. 
City is therefore a weak way to group customers for regional campaigns.

**Task 5:** `city_counts` counts customers per city with a loop and an if/else on a dictionary (no Counter, no pandas). 
`email_domain_counts` uses a dictionary comprehension over the TLDs. 
`sort_counts` orders results from most to least common with ties broken alphabetically. 
Every city appears once, but `biz` is the most common email domain (3 of 10 customers).

**Task 6:** `to_dataframe` turns the flat rows into a pandas DataFrame (shape 10 x 12) which is the count of rows & columns(rows,columns). 
`latitude` and `longitude` are float64 because they were converted in Task 3. 
`value_counts()` in pandas gives the same city and email domain counts as hand-written functions.

**Task 7:** The script creates a directory called `output` if it does not exist then saves `customers.csv` and `city_counts.csv` sorted by count descending then city. 
Both are written with `index=False` so no extra index column appears at the start.

**Task 8:** `plot_distribution` draws a titled bar chart with labelled axes and rotated tick labels then saves it. 
I used it for two charts:`customer_distribution.png` (by city) and `email_domain_distribution.png` (by email TLD). 
The email chart is more useful because the counts vary while every city has just one customer.

## How to run

1. Create and activate a virtual environment:
   `python -m venv venv`, then `source venv/Scripts/activate` (Git Bash on
   Windows) or `source venv/bin/activate` (Mac/Linux).
2. Install the packages: `pip install -r requirements.txt`
3. Run the analysis: `python analysis.py`

The script prints a findings summary and writes its results to `output/`.

## Findings

- The API returned 10 customers, each in a different city, so city is not a useful way to group them for regional campaigns( There are as many unique cities as customers (10 and 10) so no two customers share a city and city-based campaigns would reach only one person each)
- Email domains vary more: `biz` is the most common (3 of 10 customers) and the other seven domains appear once each. This shows where customers cluster which is what marketing needs to prioritise.
- With only 10 customers these differences are small so they are hints rather than firm conclusions.

## Assumptions
- Nested values are dictionaries only. This API has no lists inside records, so `explore` does not handle lists.
- Phone numbers and zipcodes are kept as strings because they are identifiers and not quantities. They also contain symbols or may have leading zeros.


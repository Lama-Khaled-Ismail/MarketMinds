from pymongo import MongoClient
from datetime import datetime, timedelta
import random

from database import english_collection, ar_collection
"""

# Filter documents
documents = list(english_collection.find({"brand_id": 5, "platform": "Twitter"}))

# Number of documents
total_docs = len(documents)
if total_docs == 0:
    print("No documents found.")
    exit()

# Calculate the number of documents per month
months = [
    ("January", 31), ("February", 28), ("March", 31), ("April", 30),
    ("May", 31), ("June", 30), ("July", 31), ("August", 31),
    ("September", 30), ("October", 31), ("November", 30), ("December", 31)
]

docs_per_month = total_docs // len(months)
extra_docs = total_docs % len(months)

# Generate random dates for each month
dates = []
for i, (month, days) in enumerate(months):
    month_dates = [datetime(2023, i+1, day) for day in range(1, days+1)]
    random.shuffle(month_dates)
    dates.extend(month_dates[:docs_per_month])

# Distribute extra documents (if any)
if extra_docs > 0:
    remaining_dates = [
        datetime(2023, i+1, day) 
        for i, days in enumerate([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
        for day in range(1, days+1) if datetime(2023, i+1, day) not in dates
    ]
    random.shuffle(remaining_dates)
    dates.extend(remaining_dates[:extra_docs])

# Shuffle dates to ensure randomness
random.shuffle(dates)

# Update documents
for i, doc in enumerate(documents):
    formatted_date = dates[i].strftime("%d %B %Y")
    english_collection.update_one({"_id": doc["_id"]}, {"$set": {"time": formatted_date}})
    print(f"Updated document {i+1}/{total_docs} with date {formatted_date}")

print("All documents updated.")
"""
# Find all documents with dates
docs = list(ar_collection.find({"time": {"$exists": True}}))

# Separate December 2023 documents
december_docs = [doc for doc in docs if 'December 2023' in doc['time']]

# Shuffle and select a quarter of December 2023 documents to move to January 2024
random.shuffle(december_docs)
quarter_index = len(december_docs) // 4
docs_to_move = december_docs[:quarter_index]

for doc in docs:
    old_date_str = doc['time']

    try:
        old_date = datetime.strptime(old_date_str, '%d %B %Y')
        month = old_date.month

        # Determine the new year based on the month
        if 1 <= month <= 7:
            new_year = 2024
        else:
            new_year = 2023

        # Update the date with the new year
        new_date = old_date.replace(year=new_year)

        # Special case for moving December 2023 to January 2024
        if doc in docs_to_move:
            new_date = new_date.replace(month=1, year=2024)
    except ValueError:
        # Handle special case for 'Today'
        if old_date_str.lower() == 'today':
            new_month = random.randint(1, 7)
            new_day = random.randint(1, 28)  # Simplifying by using 28 to avoid invalid dates
            new_date = datetime(2024, new_month, new_day)
        else:
            continue  # Skip documents with other invalid date formats

    new_date_str = new_date.strftime('%d %B %Y')

    # Update the document
    ar_collection.update_one({"_id": doc["_id"]}, {"$set": {"time": new_date_str}})

print("Dates updated successfully.")
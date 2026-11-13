
import csv
import random
from pathlib import Path
from datetime import date, timedelta

random.seed(42)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

TOTAL_RECORDS = 2000
UNIQUE_RECORDS = 1600

first_names = [
    "Narendra", "Rahul", "Priya", "Amit", "Sneha",
    "Kiran", "Arjun", "Anjali", "Vijay", "Meera",
    "Ravi", "Divya", "Suresh", "Pooja", "Rohan"
]

last_names = [
    "Kumar", "Sharma", "Reddy", "Patel", "Verma",
    "Singh", "Rao", "Gupta", "Das", "Nair"
]

cities = ["Hyderabad", "Chennai", "Bangalore", "Mumbai", "Pune"]
sources = ["CRM", "Website", "Mobile App", "ERP"]

def random_date():
    start = date(2025, 1, 1)
    return (start + timedelta(days=random.randint(0, 680))).isoformat()


# ---------------- CUSTOMER DATA ----------------

customers = []

for i in range(UNIQUE_RECORDS):
    first = random.choice(first_names)
    last = random.choice(last_names)
    name = f"{first} {last}"

    customers.append({
        "customer_id": f"C{i + 1:05}",
        "name": name,
        "email": f"{first.lower()}.{last.lower()}{i}@example.com",
        "phone": str(9000000000 + i),
        "city": random.choice(cities),
        "updated_at": random_date(),
        "source": random.choice(sources)
    })

for i in range(UNIQUE_RECORDS, TOTAL_RECORDS):
    original = random.choice(customers[:UNIQUE_RECORDS]).copy()

    if i % 2 == 0:
        # Exact duplicate: same business details, new record ID
        pass
    else:
        # Probable duplicate: slightly different name or email
        original["name"] = original["name"].split()[0] + " " + original["name"].split()[1][0]
        original["email"] = "updated_" + original["email"]

    original["customer_id"] = f"C{i + 1:05}"
    original["updated_at"] = random_date()
    original["source"] = random.choice(sources)

    customers.append(original)

with open(DATA_DIR / "customers.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=customers[0].keys())
    writer.writeheader()
    writer.writerows(customers)


# ---------------- PRODUCT DATA ----------------

product_templates = [
    ("iPhone 15", "Mobile", "Apple", 65000),
    ("iPhone 15 Pro", "Mobile", "Apple", 85000),
    ("Galaxy S24", "Mobile", "Samsung", 70000),
    ("Galaxy S24 Ultra", "Mobile", "Samsung", 95000),
    ("Dell Inspiron 15", "Laptop", "Dell", 55000),
    ("HP Pavilion", "Laptop", "HP", 60000),
    ("Lenovo ThinkPad", "Laptop", "Lenovo", 75000),
    ("Sony Headphones", "Audio", "Sony", 12000),
    ("Boat Earbuds", "Audio", "Boat", 2500),
    ("Canon Camera", "Camera", "Canon", 45000)
]

products = []

for i in range(UNIQUE_RECORDS):
    name, category, brand, price = random.choice(product_templates)

    products.append({
        "product_id": f"P{i + 1:05}",
        "product_name": f"{name} Model {i + 1}",
        "category": category,
        "brand": brand,
        "price": price + random.randint(-500, 500),
        "updated_at": random_date(),
        "source": random.choice(sources)
    })

for i in range(UNIQUE_RECORDS, TOTAL_RECORDS):
    original = random.choice(products[:UNIQUE_RECORDS]).copy()

    if i % 2 != 0:
        # Probable duplicate: small product name variation
        original["product_name"] += " Edition"

    original["product_id"] = f"P{i + 1:05}"
    original["updated_at"] = random_date()
    original["source"] = random.choice(sources)

    products.append(original)

with open(DATA_DIR / "products.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=products[0].keys())
    writer.writeheader()
    writer.writerows(products)

print("Dataset generation completed!")
print("Customer records:", len(customers))
print("Product records:", len(products))
print("Files saved inside:", DATA_DIR)

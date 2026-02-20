import os
import random
import logging
from datetime import datetime, timedelta
from faker import Faker
import psycopg2
from dotenv import load_dotenv

# Load environment variables

load_dotenv()

# Initialize Faker

fake = Faker()

# Configure logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Connect to database

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT')
)
cur = conn.cursor()


# POPULATE STORES

logger.info("Inserting stores...")

for i in range(5):
    cur.execute("""
        INSERT INTO Stores (address, city, phone_number)
        VALUES (%s, %s, %s)
    """, (
        fake.street_address(), fake.city(), fake.unique.numerify('###-###-####')
    ))

conn.commit()
logger.info("Stores inserted successfully!")

# Populate Customers

logger.info("Inserting customers...")

for i in range(1000):
    cur.execute("""
        INSERT INTO Customers (first_name, last_name, email, phone_number)
        VALUES (%s, %s, %s, %s)
    """, (
        fake.first_name(), fake.last_name(), fake.unique.email(), fake.unique.numerify('###-###-####')
    ))

conn.commit()
logger.info("Customers inserted successfully!")


# POPULATE INGREDIENTS

logger.info("Inserting ingredients...")

ingredients = [
    # Dough & Base
    ("Pizza Dough", "kg"),
    ("Flour", "kg"),
    ("Yeast", "kg"),
    ("Sugar", "kg"),
    ("Salt", "kg"),

    # Oils & Sauces
    ("Olive Oil", "liters"),
    ("Tomato Sauce", "liters"),
    ("BBQ Sauce", "liters"),
    ("Alfredo Sauce", "liters"),
    ("Hot Sauce", "liters"),

    # Cheeses
    ("Mozzarella Cheese", "kg"),
    ("Parmesan Cheese", "kg"),
    ("Cheddar Cheese", "kg"),
    ("Ricotta Cheese", "kg"),
    ("Feta Cheese", "kg"),

    # Meats
    ("Pepperoni", "kg"),
    ("Italian Sausage", "kg"),
    ("Bacon", "kg"),
    ("Grilled Chicken", "kg"),
    ("Ham", "kg"),
    ("Ground Beef", "kg"),
    ("Anchovies", "kg"),

    # Vegetables
    ("Mushrooms", "kg"),
    ("Red Onions", "kg"),
    ("Bell Peppers", "kg"),
    ("Black Olives", "kg"),
    ("Fresh Tomatoes", "kg"),
    ("Spinach", "kg"),
    ("Jalapeños", "kg"),
    ("Pineapple", "kg"),
    ("Garlic", "kg"),
    ("Fresh Basil", "kg"),
    ("Arugula", "kg"),

    # Drinks
    ("Cola Syrup", "liters"),
    ("Sprite Syrup", "liters"),
    ("Orange Juice", "liters"),
    ("Bottled Water", "units"),
    ("Lemonade", "liters"),

    # Sides & Other
    ("Chicken Wings", "kg"),
    ("Bread Sticks", "units"),
    ("Ranch Dressing", "liters"),
    ("Garlic Butter", "kg"),
    ("Cornmeal", "kg"),
    
    #Extras
    ("Potatoes", "kg"),
    ("Butter", "kg"),
    ("Parsley", "kg"),
    ("Black Pepper", "kg"),
    ("Carbonated Water", "liters"),
]

for name, unit in ingredients:
    cur.execute("""
        INSERT INTO Ingredients (name, stock_quantity, unit)
        VALUES (%s, %s, %s)
    """, (
        name, round(random.uniform(10, 500), 2), unit
    ))

conn.commit()
logger.info(f"{len(ingredients)} ingredients inserted successfully!")


# POPULATE MENU ITEMS

logger.info("Inserting menu items..")

menu_items = [
    # (name, category, size, price)

    ("Margherita Pizza", "Pizza", "Small", 8.99),
    ("Margherita Pizza", "Pizza", "Medium", 11.99),
    ("Margherita Pizza", "Pizza", "Large", 14.99),

    ("Pepperoni Pizza", "Pizza", "Small", 9.99),
    ("Pepperoni Pizza", "Pizza", "Medium", 12.99),
    ("Pepperoni Pizza", "Pizza", "Large", 15.99),

    ("BBQ Chicken Pizza", "Pizza", "Small", 10.99),
    ("BBQ Chicken Pizza", "Pizza", "Medium", 13.99),
    ("BBQ Chicken Pizza", "Pizza", "Large", 16.99),

    ("Veggie Supreme Pizza", "Pizza", "Small", 9.49),
    ("Veggie Supreme Pizza", "Pizza", "Medium", 12.49),
    ("Veggie Supreme Pizza", "Pizza", "Large", 15.49),

    # ---------------- SIDES ----------------
    ("Garlic Bread", "Side", "Regular", 4.99),
    ("Cheesy Garlic Bread", "Side", "Regular", 5.99),
    ("Chicken Wings (6 pcs)", "Side", "Regular", 6.99),
    ("Chicken Wings (12 pcs)", "Side", "Large", 11.99),
    ("French Fries", "Side", "Regular", 3.99),
    ("Loaded Fries", "Side", "Large", 6.49),

    # ---------------- DRINKS ----------------
    ("Coca-Cola", "Drink", "Can", 1.99),
    ("Coca-Cola", "Drink", "Bottle", 2.99),
    ("Sprite", "Drink", "Can", 1.99),
    ("Sprite", "Drink", "Bottle", 2.99),
    ("Orange Juice", "Drink", "Small", 2.49),
    ("Orange Juice", "Drink", "Large", 3.49),
    ("Mineral Water", "Drink", "Small", 1.49),
    ("Mineral Water", "Drink", "Large", 2.49),
]

for name, category, size, price in menu_items:
    cur.execute("""
        INSERT INTO Menu_Items (name, category, size, price)
        VALUES (%s, %s, %s, %s)
    """, (
        name, category, size, price
    ))
conn.commit()
logger.info(f"{len(menu_items)} menu items inserted successfully!")

# FETCH EXISTING IDs FOR FOREIGN KEYS

# Get all customer IDs

logger.info("Fetcing existing customer ids..")

cur.execute("SELECT customer_id FROM Customers")
customer_ids =[row[0] for row in cur.fetchall()]

# Get all store_ids IDs

logger.info("Fetching store ids..")

cur.execute("SELECT store_id FROM Stores")
store_ids = [row[0] for row in cur.fetchall()]

# Get all item_id and prices

logger.info("Fetching item_id and prices..")

cur.execute("SELECT item_id, price FROM Menu_Items")
menu_items_data = cur.fetchall()

# POPULATE ORDERS AND ORDER ITEMS

logger.info("Inserting orders and order items...")


for i in range(5000):
    # Pick random customer, store, and timestamp
    customer_id = random.choice(customer_ids)
    store_id = random.choice(store_ids)
    order_date = fake.date_time_this_year()

    # Insert order with temporary total of 0
    cur.execute("""
        INSERT INTO Orders (customer_id, store_id, order_timestamp, total_amount)
        VALUES (%s, %s, %s, %s)
        RETURNING order_id
    """, (customer_id, store_id, order_date, 0))
    
    order_id = cur.fetchone()[0]

    num_items = random.randint(1, 5)
    order_total = 0

    for _ in range(num_items):
        item = random.choice(menu_items_data)
        item_id = item[0]
        price = item[1]

        quantity = random.randint(1, 3)
        line_total = price * quantity

        # Store UNIT PRICE, not line total
        cur.execute("""
            INSERT INTO Order_Items (order_id, item_id, quantity, item_price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, item_id, quantity, price))

        order_total += line_total

    # Update order total after inserting all items
    cur.execute("""
        UPDATE Orders
        SET total_amount = %s
        WHERE order_id = %s
    """, (round(order_total, 2), order_id))



conn.commit()
logger.info("Orders and order items inserted successfully!")

# POPULATE MENU ITEM INGREDIENTS

logger.info("Inserting menu item ingredients...")

# Fetch ingredient names and IDs
cur.execute("SELECT ingredient_id, name FROM Ingredients")
ingredient_map = {name: id for id, name in cur.fetchall()}

# Fetch menu item names and IDs
cur.execute("SELECT item_id, name FROM Menu_Items")
menu_item_map = {name: id for id, name in cur.fetchall()}

recipes = {

    # ---------------- PIZZAS ----------------
    "Margherita Pizza": [
        "Pizza Dough",
        "Tomato Sauce",
        "Mozzarella Cheese",
        "Fresh Basil",
        "Olive Oil"
    ],

    "Pepperoni Pizza": [
        "Pizza Dough",
        "Tomato Sauce",
        "Mozzarella Cheese",
        "Pepperoni"
    ],

    "BBQ Chicken Pizza": [
        "Pizza Dough",
        "BBQ Sauce",
        "Mozzarella Cheese",
        "Grilled Chicken",
        "Red Onions"
    ],

    "Veggie Supreme Pizza": [
        "Pizza Dough",
        "Tomato Sauce",
        "Mozzarella Cheese",
        "Bell Peppers",
        "Mushrooms",
        "Black Olives",
        "Red Onions"
    ],

    # ---------------- SIDES ----------------
    "Garlic Bread": [
        "Bread Sticks",
        "Garlic Butter",
        "Garlic"
    ],

    "Cheesy Garlic Bread": [
        "Bread Sticks",
        "Garlic Butter",
        "Garlic",
        "Mozzarella Cheese"
    ],

    "Chicken Wings (6 pcs)": [
        "Chicken Wings",
        "Hot Sauce",
        "Salt"
    ],

    "Chicken Wings (12 pcs)": [
        "Chicken Wings",
        "Hot Sauce",
        "Salt"
    ],

    "French Fries": [
        "Cornmeal",
        "Salt",
        "Olive Oil"
    ],

    "Loaded Fries": [
        "Cornmeal",
        "Salt",
        "Olive Oil",
        "Cheddar Cheese",
        "Bacon"
    ],

    # ---------------- DRINKS ----------------
    "Coca-Cola": [
        "Cola Syrup",
        "Bottled Water"
    ],

    "Sprite": [
        "Sprite Syrup",
        "Bottled Water"
    ],

    "Orange Juice": [
        "Orange Juice"
    ],

    "Mineral Water": [
        "Bottled Water"
    ],
}

for recipe_name, ingredient_list in recipes.items():
    # Find all menu items that match this recipe name
    # (e.g., "Margherita Pizza" matches Small, Medium, and Large)
    matching_items = [
        item_id for name, item_id in menu_item_map.items()
        if recipe_name in name
    ]

    for item_id in matching_items:
        for ingredient_name in ingredient_list:
            ingredient_id = ingredient_map[ingredient_name]
            cur.execute("""
                INSERT INTO Menu_Item_Ingredients (item_id, ingredient_id, quantity_needed)
                VALUES (%s, %s, %s)
            """, (
                item_id, ingredient_id, round(random.uniform(0.5, 3.0), 2)
            ))

conn.commit()
logger.info("Menu item ingredients inserted successfully!")

# CLEANUP

cur.close()
conn.close()
logger.info("Database connection closed. Population complete!")
import random
from faker import Faker
import mysql.connector

faker = Faker()
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="kia09381395696",
    database="onlineshopping"
)
cursor = conn.cursor()

# Predefined lists and dictionaries
categories = ['Electronics', 'Clothing', 'Books', 'Furniture', 'Toys', 'Food', 'Beauty']
brands = {
    'Electronics': ['Sony', 'Samsung', 'Apple', 'LG', 'Panasonic'],
    'Clothing': ['Nike', 'Adidas', 'Zara', 'H&M', 'Uniqlo'],
    'Books': ['Penguin', 'HarperCollins', 'Simon & Schuster', 'Macmillan', 'Hachette'],
    'Furniture': ['Ikea', 'Ashley Furniture', 'Wayfair', 'Herman Miller', 'Steelcase'],
    'Toys': ['Lego', 'Mattel', 'Hasbro', 'Fisher-Price', 'Nerf'],
    'Food': ['Nestle', 'Kraft', 'PepsiCo', 'Unilever', 'Coca-Cola'],
    'Beauty': ['L\'Oreal', 'Estee Lauder', 'Procter & Gamble', 'Niche', 'Shiseido']
}
product_names = {
    'Electronics': {
        'Sony': ['Bravia TV', 'PlayStation', 'Sony Camera'],
        'Samsung': ['Galaxy Phone', 'Samsung TV', 'Samsung Fridge'],
        'Apple': ['iPhone', 'MacBook', 'Apple Watch'],
        'LG': ['LG Washing Machine', 'LG Refrigerator', 'LG TV'],
        'Panasonic': ['Panasonic TV', 'Panasonic Camera', 'Panasonic Microwave']
    },
    'Clothing': {
        'Nike': ['Air Max', 'Running Shoes', 'Nike Hoodie'],
        'Adidas': ['Ultraboost', 'Adidas Sweatpants', 'Adidas T-Shirt'],
        'Zara': ['Zara Jacket', 'Zara Dress', 'Zara Jeans'],
        'H&M': ['H&M T-Shirt', 'H&M Dress', 'H&M Jacket'],
        'Uniqlo': ['Uniqlo Shirt', 'Uniqlo Pants', 'Uniqlo Jacket']
    },
    'Books': {
        'Penguin': ['The Catcher in the Rye', '1984', 'To Kill a Mockingbird'],
        'HarperCollins': ['Brave New World', 'American Gods', 'Good Omens'],
        'Simon & Schuster': ['The Great Gatsby', 'City of Girls', 'The Glass Castle'],
        'Macmillan': ['The Night Circus', 'Wolf Hall', 'The Luminaries'],
        'Hachette': ['The Girl on the Train', 'Gone Girl', 'The Nightingale']
    },
    'Furniture': {
        'Ikea': ['Billy Bookcase', 'Malm Bed', 'Ektorp Sofa'],
        'Ashley Furniture': ['Ashley Sofa', 'Ashley Bed', 'Ashley Table'],
        'Wayfair': ['Wayfair Chair', 'Wayfair Table', 'Wayfair Sofa'],
        'Herman Miller': ['Aeron Chair', 'Embody Chair', 'Setu Chair'],
        'Steelcase': ['Leap Chair', 'Steelcase Desk', 'Steelcase Storage']
    },
    'Toys': {
        'Lego': ['Lego Star Wars', 'Lego City', 'Lego Technic'],
        'Mattel': ['Barbie Doll', 'Hot Wheels', 'Fisher-Price'],
        'Hasbro': ['Monopoly', 'Nerf Gun', 'Play-Doh'],
        'Fisher-Price': ['Baby Toy', 'Educational Toy', 'Building Blocks'],
        'Nerf': ['Nerf Blaster', 'Nerf Super Soaker', 'Nerf Elite Dart']
    },
    'Food': {
        'Nestle': ['Nestle Chocolate', 'Nestle Milk', 'Nestle Ice Cream'],
        'Kraft': ['Kraft Cheese', 'Kraft Mac & Cheese', 'Kraft Salad Dressing'],
        'PepsiCo': ['Pepsi', 'Lays Chips', 'Gatorade'],
        'Unilever': ['Ben & Jerry\'s', 'Lipton Tea', 'Hellmann\'s Mayonnaise'],
        'Coca-Cola': ['Coca-Cola Soda', 'Sprite', 'Fanta']
    },
    'Beauty': {
        'L\'Oreal': ['L\'Oreal Shampoo', 'L\'Oreal Mascara', 'L\'OReal Lipstick'],
        'Estee Lauder': ['Estee Lauder Foundation', 'Estee Lauder Serum', 'Estee Lauder Perfume'],
        'Procter & Gamble': ['Olay Cream', 'Pantene Shampoo', 'Gillette Razor'],
        'Niche': ['Dove Soap', 'Axe Deodorant', 'TRESemme Shampoo'],
        'Shiseido': ['Shiseido Sunscreen', 'Shiseido Moisturizer', 'Shiseido Foundation']
    }
}
product_descriptions = [
    "High quality and durable.",
    "Budget-friendly and reliable.",
    "Stylish and modern design.",
    "Top-rated by customers.",
    "Best seller in its category.",
    "Eco-friendly and sustainable.",
    "Limited edition and exclusive.",
    "Compact and portable.",
    "User-friendly interface.",
    "Highly recommended by experts."
]

comments = {
    'approved': [
        "Great product, very satisfied!",
        "Exceeded my expectations.",
        "Excellent quality, will buy again.",
        "Highly recommended!",
        "Fantastic value for money.",
        "Worst product ever.",
        "Terrible quality, very disappointed.",
        "Very poor customer service."
    ],
    'inappropriate': [
        "Terrible quality, very disappointed. shitty product.",
        "Not as described, do not buy. wtf is this.",
        "Worst product ever. Fuckkkk",
        "Completely useless, Don't use this shit never.",
        "Fuck this product. Very poor customer service."
    ]
}

holidays = {
    'New Year': 'Celebrate the start of the new year with amazing discounts.',
    'Valentine\'s Day': 'Special offers for your loved ones on Valentine\'s Day.',
    'Easter': 'Easter discounts for the whole family.',
    'Memorial Day': 'Honor the heroes with our Memorial Day sale.',
    'Independence Day': 'Celebrate freedom with huge discounts on Independence Day.',
    'Halloween': 'Spooky deals for a spooky Halloween.',
    'Thanksgiving': 'Give thanks with great deals this Thanksgiving.',
    'Black Friday': 'Massive discounts for Black Friday.',
    'Cyber Monday': 'Unbeatable offers on Cyber Monday.',
    'Christmas': 'Merry Christmas! Enjoy our special holiday discounts.'
}

# Functions to generate data for online shopping database
def generate_users(n):
    for _ in range(n):
        try:
            username = faker.user_name()
            password = faker.password()
            name = faker.name()
            email = faker.email()
            contact_number = faker.phone_number()
            street = faker.street_address()
            city = faker.city()
            state = faker.state()
            postal_code = faker.postcode()
            country = faker.country()
            cursor.execute("INSERT INTO Users (username, password, name, email, contact_number, street, city, state, postal_code, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (username, password, name, email, contact_number, street, city, state, postal_code, country))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            continue
    conn.commit()

def generate_managers(n):
    for _ in range(n):
        try:
            username = faker.user_name()
            password = faker.password()
            email = faker.email()
            cursor.execute("INSERT INTO Managers (username, password, email) VALUES (%s, %s, %s)",
                           (username, password, email))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            continue
    conn.commit()

def generate_categories():
    cursor.execute("DELETE FROM Categories") 
    for category in categories:
        cursor.execute("INSERT INTO Categories (name) VALUES (%s)", (category,))
    conn.commit()

def fetch_category_ids():
    cursor.execute("SELECT category_id, name FROM Categories")
    rows = cursor.fetchall()
    return {name: category_id for category_id, name in rows}

def generate_brands():
    cursor.execute("DELETE FROM Brands") 
    for category, brand_list in brands.items():
        for brand in brand_list:
            status = random.choice(['active', 'inactive', 'old'])
            cursor.execute("INSERT INTO Brands (name, status) VALUES (%s, %s)", (brand, status))
    conn.commit()

def fetch_brand_ids():
    cursor.execute("SELECT brand_id, name FROM Brands")
    rows = cursor.fetchall()
    return {name: brand_id for brand_id, name in rows}

def generate_products(n):
    category_ids = fetch_category_ids()
    brand_ids = fetch_brand_ids()

    for _ in range(n):
        category = random.choice(categories)
        category_id = category_ids[category]
        brand = random.choice(brands[category])
        brand_id = brand_ids[brand]
        name = random.choice(product_names[category][brand])
        description = random.choice(product_descriptions)
        price = round(random.uniform(10.0, 1000.0), 2)
        stock = random.randint(0, 100)
        status = random.choice(['active', 'inactive'])
        cursor.execute("INSERT INTO Products (name, description, price, stock, category_id, brand_id, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (name, description, price, stock, category_id, brand_id, status))
    conn.commit()

def generate_shipping_info(n):
    shipping_info_ids = []
    for _ in range(n):
        tracking_number = faker.bothify(text='???-########')
        carrier = faker.company()
        shipping_date = faker.date_this_year()
        delivery_date = faker.date_between(start_date=shipping_date, end_date="+10d")
        status = random.choice(['pending', 'shipped', 'delivered', 'returned'])
        cursor.execute("INSERT INTO ShippingInfo (tracking_number, carrier, shipping_date, delivery_date, status) VALUES (%s, %s, %s, %s, %s)",
                       (tracking_number, carrier, shipping_date, delivery_date, status))
        shipping_info_ids.append(cursor.lastrowid)
    conn.commit()
    return shipping_info_ids

def generate_orders(n):
    user_ids = [i + 1 for i in range(100)] 
    shipping_info_ids = generate_shipping_info(n)
    for _ in range(n):
        user_id = random.choice(user_ids)
        shipping_info_id = random.choice(shipping_info_ids)
        status = random.choice(['pending', 'processing', 'shipped', 'delivered', 'cancelled', 'returned'])
        total_amount = round(random.uniform(20.0, 2000.0), 2)
        cursor.execute("INSERT INTO Orders (user_id, shipping_info_id, status, total_amount) VALUES (%s, %s, %s, %s)",
                       (user_id, shipping_info_id, status, total_amount))
    conn.commit()

def generate_order_details(n):
    order_ids = [i + 1 for i in range(100)] 
    product_ids = [i + 1 for i in range(100)] 
    for _ in range(n):
        order_id = random.choice(order_ids)
        product_id = random.choice(product_ids)
        quantity = random.randint(1, 10)
        price = round(random.uniform(10.0, 1000.0), 2)
        cursor.execute("INSERT INTO OrderDetails (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                       (order_id, product_id, quantity, price))
    conn.commit()

def generate_shopping_carts(n):
    user_ids = [i + 1 for i in range(100)] 
    for _ in range(n):
        user_id = random.choice(user_ids)
        cursor.execute("INSERT INTO ShoppingCart (user_id) VALUES (%s)", (user_id,))
    conn.commit()

def generate_cart_items(n):
    cart_ids = [i + 1 for i in range(100)] 
    product_ids = [i + 1 for i in range(100)]
    for _ in range(n):
        cart_id = random.choice(cart_ids)
        product_id = random.choice(product_ids)
        quantity = random.randint(1, 10)
        cursor.execute("INSERT INTO CartItems (cart_id, product_id, quantity) VALUES (%s, %s, %s)",
                       (cart_id, product_id, quantity))
    conn.commit()

def generate_purchase_history(n):
    user_ids = [i + 1 for i in range(100)]  
    order_ids = [i + 1 for i in range(100)] 
    for _ in range(n):
        user_id = random.choice(user_ids)
        order_id = random.choice(order_ids)
        cursor.execute("INSERT INTO PurchaseHistory (user_id, order_id) VALUES (%s, %s)",
                       (user_id, order_id))
    conn.commit()

def generate_comments(n):
    product_ids = [i + 1 for i in range(100)] 
    user_ids = [i + 1 for i in range(100)]  
    manager_ids = [i + 1 for i in range(10)]  
    for _ in range(n):
        product_id = random.choice(product_ids)
        user_id = random.choice(user_ids)
        comment_type = random.choice(['approved', 'inappropriate'])
        comment = random.choice(comments[comment_type])
        status = comment_type
        moderated_by = random.choice(manager_ids)
        cursor.execute("INSERT INTO Comments (product_id, user_id, comment, status, moderated_by) VALUES (%s, %s, %s, %s, %s)",
                       (product_id, user_id, comment, status, moderated_by))
    conn.commit()

def generate_discounts(n):
    for _ in range(n):
        name, description = random.choice(list(holidays.items()))
        discount_percentage = round(random.uniform(5.0, 50.0), 2)
        start_date = faker.date_this_year()
        end_date = faker.date_between(start_date=start_date, end_date="+30d")
        cursor.execute("INSERT INTO Discounts (name, description, discount_percentage, start_date, end_date) VALUES (%s, %s, %s, %s, %s)",
                       (name, description, discount_percentage, start_date, end_date))
    conn.commit()

def generate_product_discounts(n):
    product_ids = [i + 1 for i in range(100)]  
    discount_ids = [i + 1 for i in range(100)]  
    for _ in range(n):
        product_id = random.choice(product_ids)
        discount_id = random.choice(discount_ids)
        cursor.execute("INSERT INTO ProductDiscounts (product_id, discount_id) VALUES (%s, %s)",
                       (product_id, discount_id))
    conn.commit()

# Generate data
generate_users(100)
generate_managers(10)
generate_categories()
generate_brands()
generate_products(100)
generate_orders(100)
generate_order_details(200)
generate_shopping_carts(100)
generate_cart_items(200)
generate_purchase_history(100)
generate_comments(100)
generate_discounts(100)
generate_product_discounts(100)

cursor.close()
conn.close()
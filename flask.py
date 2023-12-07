import sqlite3

conn = sqlite3.connect('shopping_mall.db')
cursor = conn.cursor()

# Insert Adidas products
adidas_products = [
    ('Gazelle', 79.99, 'Adidas', 0, 30),
    ('Tobacco', 89.99, 'Adidas', 0, 25),
    ('Campus', 99.99, 'Adidas', 0, 20),
    ('Bermuda', 109.99, 'Adidas', 0, 15),
    # Add more Adidas products with similar structure
]

cursor.executemany("INSERT INTO products (product_name, product_price, brand, sales_quantity, stock_quantity) VALUES (?, ?, ?, ?, ?)", adidas_products)

# Insert Nike products
nike_products = [
    ('Cortez', 89.99, 'Nike', 0, 40),
    ('Dunk Low', 129.99, 'Nike', 0, 35),
    ('Air Force', 109.99, 'Nike', 0, 30),
    ('Air Max', 139.99, 'Nike', 0, 25),
    # Add more Nike products with similar structure
]

cursor.executemany("INSERT INTO products (product_name, product_price, brand, sales_quantity, stock_quantity) VALUES (?, ?, ?, ?, ?)", nike_products)

conn.commit()
conn.close()

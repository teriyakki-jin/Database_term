import sqlite3

conn = sqlite3.connect('shopping_mall.db')
cursor = conn.cursor()

# Index for inquiries table
cursor.execute("CREATE INDEX idx_user_id ON inquiries (user_id)")
cursor.execute("CREATE INDEX idx_inquiry_type ON inquiries (inquiry_type)")

# Indexes for products table
cursor.execute("CREATE INDEX idx_brand ON products (brand)")
cursor.execute("CREATE INDEX idx_stock_quantity ON products (stock_quantity)")
cursor.execute("CREATE INDEX idx_sales_quantity ON products (sales_quantity)")

# Index for reviews table
cursor.execute("CREATE INDEX idx_product_id ON reviews (product_id)")
cursor.execute("CREATE INDEX idx_rating ON reviews (rating)")

# Indexes for users table
cursor.execute("CREATE INDEX idx_username ON users (username)")
cursor.execute("CREATE INDEX idx_role ON users (role)")

conn.commit()
conn.close()
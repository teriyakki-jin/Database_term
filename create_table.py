CREATE TABLE users (
	id INTEGER,
	username TEXT,
	password TEXT,
	"role" TEXT
);

CREATE TABLE products (
	id INTEGER,
	product_name TEXT,
	product_price REAL,
	brand TEXT,
	sales_quantity INTEGER,
	stock_quantity INTEGER
);

CREATE TABLE reviews (
	id INTEGER,
	product_id INTEGER,
	rating INTEGER,
	comment INTEGER
);
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    product_price REAL NOT NULL,
    brand TEXT NOT NULL,
    sales_quantity INTEGER NOT NULL,
    stock_quantity INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    comment TEXT,
    FOREIGN KEY (product_id) REFERENCES products (id)
);

CREATE TABLE IF NOT EXISTS inquiries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    inquiry_type TEXT NOT NULL,
    content TEXT NOT NULL,
    response TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);



CREATE VIEW product_reviews_view AS
    SELECT 
        p.id, p.product_name, p.product_price, p.brand, p.sales_quantity, p.stock_quantity, 
        AVG(r.rating) AS avg_rating, COUNT(r.id) AS review_count 
    FROM 
        products p 
        LEFT JOIN reviews r ON p.id = r.product_id 
    GROUP BY 
        p.id, p.product_name, p.product_price, p.brand, p.sales_quantity, p.stock_quantity;
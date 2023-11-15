import sqlite3

# 데이터베이스 연결 및 테이블 생성
conn = sqlite3.connect('shopping_mall.db')
cursor = conn.cursor()

# 사용자 테이블 생성
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
''')

# 제품 정보를 저장하는 테이블 생성
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        product_price REAL,
        brand TEXT,
        sales_quantity INTEGER,
        stock_quantity INTEGER
    )
''')

# 사용자 추가
cursor.execute("INSERT INTO users (username, password, role) VALUES ('user1', 'password1', 'user')")
cursor.execute("INSERT INTO users (username, password, role) VALUES ('user2', 'password2', 'user')")
cursor.execute("INSERT INTO users (username, password, role) VALUES ('201924592', '201924592', 'admin')")
# 제품 정보 추가 예시
cursor.execute("INSERT INTO products (product_name, product_price, brand, sales_quantity, stock_quantity) VALUES (?, ?, ?, ?, ?)",
               ('Product 1', 29.99, 'Brand A', 100, 50))
cursor.execute("INSERT INTO products (product_name, product_price, brand, sales_quantity, stock_quantity) VALUES (?, ?, ?, ?, ?)",
               ('Product 2', 39.99, 'Brand B', 75, 30))

conn.commit()
conn.close()

def login(username, password):
    conn = sqlite3.connect('shopping_mall.db')
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    role = cursor.fetchone()

    conn.close()

    if role:
        return role[0]
    else:
        return None

def display_products():
    conn = sqlite3.connect('shopping_mall.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    print("\n제품 목록:")
    for product in products:
        print(f"ID: {product[0]}, 제품명: {product[1]}, 가격: {product[2]}, 브랜드: {product[3]}, 판매량: {product[4]}, 재고: {product[5]}")

def add_product():
    product_name = input("제품명: ")
    product_price = float(input("가격: "))
    brand = input("브랜드: ")
    sales_quantity = int(input("판매량: "))
    stock_quantity = int(input("재고: "))

    conn = sqlite3.connect('shopping_mall.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO products (product_name, product_price, brand, sales_quantity, stock_quantity) VALUES (?, ?, ?, ?, ?)",
                   (product_name, product_price, brand, sales_quantity, stock_quantity))
    conn.commit()

    print(f"{product_name} 제품이 추가되었습니다.")

def delete_product():
    product_id = int(input("삭제할 제품의 ID를 입력하세요: "))

    conn = sqlite3.connect('shopping_mall.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()

    print(f"ID {product_id} 제품이 삭제되었습니다.")

def main():
    username = None
    while True:
        if not username:
            print("1. 로그인")
        else:
            
            print(f"1. 로그아웃: {username}")  # 로그인한 경우 로그아웃 옵션 표시

        if username:
            print("2. 쇼핑하기")
            if role == 'admin':
                print("3. 제품 추가")
                print("4. 제품 삭제")
        print("5. 종료")

        choice = input("원하는 메뉴를 선택하세요: ")

        if not username and choice == '1':
            username = input("사용자 이름: ")
            password = input("비밀번호: ")
            role = login(username, password)
            if role:
                print(f"{username}님, 환영합니다. 역할: {role}")
        elif username and choice == '2':
            print("--------------------")
            display_products()
        elif username and choice == '3' and role == 'admin':
            add_product()
        elif username and choice == '4' and role == 'admin':
            delete_product()
        elif (username or choice == '5') and username != 'admin':
            username = None  # 로그아웃할 때 사용자 이름 초기화
        elif choice == '5':
            break
        else:
            print("잘못된 선택입니다. 다시 시도하세요.")

if __name__ == "__main__":
    main()

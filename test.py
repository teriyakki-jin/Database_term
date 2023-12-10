import sqlite3

role = None  # 전역 변수로 선언
username = ''

def login(username, password):
    global role
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

   # Find the maximum length of the product names
    max_product_name_length = max(len(str(product[1])) for product in products)

    # Set the minimum column width
    min_column_width = 8

    # Calculate the column widths
    id_width = max(min_column_width, len(str(max(product[0] for product in products))))
    name_width = max(min_column_width, max_product_name_length)
    price_width = max(min_column_width, len('가격'))
    brand_width = max(min_column_width, len('브랜드'))
    sales_width = max(min_column_width, len('판매량'))
    stock_width = max(min_column_width, len('재고'))

    id_width2 = id_width 
    name_width2 = name_width -3
    price_width2 = price_width - 2
    brand_width2 = brand_width - 3
    sales_width2 = sales_width -3
    stock_width2 = stock_width -2


    # Print the table with dynamic formatting
    border = f"┌{'─' * (id_width)}┬{'─' * (name_width )}┬{'─' * (price_width)}┬{'─' * (brand_width)}┬{'─' * (sales_width )}┬{'─' * (stock_width)}┐"
    print(border)
    print(f"│{'ID':^{id_width2}}│{'제품명':^{name_width2}}│{'가격':^{price_width2}}│{'브랜드':^{brand_width2}}│{'판매량':^{sales_width2}}│{'재고':^{stock_width2}}│")
    print(f"├{'─' * (id_width)}┼{'─' * (name_width)}┼{'─' * (price_width )}┼{'─' * (brand_width)}┼{'─' * (sales_width )}┼{'─' * (stock_width)}┤")

    for product in products:
        print(f"│{product[0]:^{id_width}}│{product[1]:^{name_width}}│{product[2]:^{price_width}.2f}│{product[3]:^{brand_width}}│{product[4]:^{sales_width}}│{product[5]:^{stock_width}}│")

    print(f"└{'─' * (id_width )}┴{'─' * (name_width)}┴{'─' * (price_width )}┴{'─' * (brand_width)}┴{'─' * (sales_width )}┴{'─' * (stock_width)}┘")

def purchase_product():
    product_id = int(input("구매할 제품의 ID를 입력하세요: "))
    quantity = int(input("구매할 수량을 입력하세요: "))

    conn = sqlite3.connect('shopping_mall.db')
    cursor = conn.cursor()

    # Check if the product exists and has sufficient stock
    cursor.execute("SELECT product_name, stock_quantity, sales_quantity, product_price FROM products WHERE id=?", (product_id,))
    product_info = cursor.fetchone()

    if product_info:
        product_name, stock_quantity, sales_quantity,product_price = product_info
        if quantity > 0 and quantity <= stock_quantity:
            total_price = quantity * product_price

            # Update stock quantity
            cursor.execute("UPDATE products SET stock_quantity=?, sales_quantity=?  WHERE id=?", (stock_quantity - quantity,sales_quantity + quantity, product_id))
            conn.commit()

            print(f"\n구매 완료!\n제품명: {product_name}, 수량: {quantity}, 총 가격: {total_price}")
        else:
            print("잘못된 수량 입력이거나 재고가 부족합니다.")
    else:
        print("해당 제품이 존재하지 않습니다.")

    conn.close()



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

def display_original_inquiries():
    conn = sqlite3.connect('shopping_mall.db')
    cursor = conn.cursor()

    # Original inquiries (excluding newly added)
    cursor.execute("SELECT * FROM inquiries WHERE response IS NOT NULL")
    original_inquiries = cursor.fetchall()

    conn.close()

    print("\n기존 문의 목록:")
    for inquiry in original_inquiries:
        print(f"ID: {inquiry[0]}, 유형: {inquiry[2]}, 내용: {inquiry[3]}, 응답: {inquiry[4]}")

def manage_inquiries():
    conn = sqlite3.connect('shopping_mall.db')
    cursor = conn.cursor()

    # Unanswered inquiries
    cursor.execute("SELECT * FROM inquiries WHERE response IS NULL")
    unanswered_inquiries = cursor.fetchall()

    # All inquiries
    cursor.execute("SELECT * FROM inquiries")
    all_inquiries = cursor.fetchall()

    conn.close()

    print("\n미응답 문의 목록:")
    for inquiry in unanswered_inquiries:
        print(f"ID: {inquiry[0]}, 유형: {inquiry[2]}, 내용: {inquiry[3]}")

    print("\n전체 문의 목록:")
    for inquiry in all_inquiries:
        print(f"ID: {inquiry[0]}, 유형: {inquiry[2]}, 내용: {inquiry[3]}, 응답: {inquiry[4]}")

def respond_to_inquiry():
    manage_inquiries()
    inquiry_id = int(input("응답할 문의의 ID를 입력하세요: "))
    response = input("응답 내용을 입력하세요: ")

    conn = sqlite3.connect('shopping_mall.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE inquiries SET response=? WHERE id=?", (response, inquiry_id))
    conn.commit()

    print(f"ID {inquiry_id} 문의에 대한 응답이 등록되었습니다.")

    conn.close()

def add_inquiry():
    inquiry_type = input("문의 유형을 입력하세요 (문의/불만/교환/반품): ")
    content = input("문의 내용을 입력하세요: ")

    conn = sqlite3.connect('shopping_mall.db')
    cursor = conn.cursor()

    # 사용자 확인
    cursor.execute("SELECT id FROM users WHERE username=?", (username,))
    user_id = cursor.fetchone()

    if user_id:
        cursor.execute("INSERT INTO inquiries (user_id, inquiry_type, content) VALUES (?, ?, ?)",
                       (user_id[0], inquiry_type, content))
        conn.commit()

        print("문의가 등록되었습니다.")
    else:
        print("사용자를 찾을 수 없습니다.")

    conn.close()


def display_products_for_review():
    conn = sqlite3.connect('shopping_mall.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    # Find the maximum length of the product names
    max_product_name_length = max(len(str(product[1])) for product in products)

    # Set the minimum column width
    min_column_width = 8

    # Calculate the column widths
    id_width = max(min_column_width, len(str(max(product[0] for product in products))))
    name_width = max(min_column_width, max_product_name_length)
    price_width = max(min_column_width, len('가격'))
    brand_width = max(min_column_width, len('브랜드'))
    sales_width = max(min_column_width, len('판매량'))
    stock_width = max(min_column_width, len('재고'))

    id_width2 = id_width 
    name_width2 = name_width - 3
    price_width2 = price_width - 2
    brand_width2 = brand_width - 3
    sales_width2 = sales_width - 3
    stock_width2 = stock_width - 2

    # Print the table with dynamic formatting
    border = f"┌{'─' * (id_width)}┬{'─' * (name_width )}┬{'─' * (price_width)}┬{'─' * (brand_width)}┬{'─' * (sales_width )}┬{'─' * (stock_width)}┐"
    print(border)
    print(f"│{'ID':^{id_width2}}│{'제품명':^{name_width2}}│{'가격':^{price_width2}}│{'브랜드':^{brand_width2}}│{'판매량':^{sales_width2}}│{'재고':^{stock_width2}}│")
    print(f"├{'─' * (id_width)}┼{'─' * (name_width)}┼{'─' * (price_width )}┼{'─' * (brand_width)}┼{'─' * (sales_width )}┼{'─' * (stock_width)}┤")

    for product in products:
        print(f"│{product[0]:^{id_width}}│{product[1]:^{name_width}}│{product[2]:^{price_width}.2f}│{product[3]:^{brand_width}}│{product[4]:^{sales_width}}│{product[5]:^{stock_width}}│")

    print(f"└{'─' * (id_width )}┴{'─' * (name_width)}┴{'─' * (price_width )}┴{'─' * (brand_width)}┴{'─' * (sales_width )}┴{'─' * (stock_width)}┘")

# You can call this function wherever needed, like in display_products_with_reviews or add_review.


def add_review():
    display_products_for_review()
    product_id = int(input("리뷰를 등록할 제품의 ID를 입력하세요: "))
    rating = int(input("평점을 입력하세요 (1에서 5까지): "))
    comment = input("리뷰 내용을 입력하세요: ")

    conn = sqlite3.connect('shopping_mall.db')
    cursor = conn.cursor()

    # Check if the product exists
    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()

    if product:
        # Insert the review
        cursor.execute("INSERT INTO reviews (product_id, rating, comment) VALUES (?, ?, ?)",
                       (product_id, rating, comment))
        conn.commit()

        print(f"\n리뷰 등록 완료!\n제품명: {product[1]}, 평점: {rating}, 내용: {comment}")
    else:
        print("해당 제품이 존재하지 않습니다.")

    conn.close()



def add_user():
    new_username = input("새로운 사용자 이름을 입력하세요: ")
    new_password = input("새로운 비밀번호를 입력하세요: ")
    new_role = input("새로운 사용자 역할을 입력하세요: ")

    conn = sqlite3.connect('shopping_mall.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                   (new_username, new_password, new_role))
    conn.commit()

    print(f"{new_username} 사용자가 추가되었습니다.")

    conn.close()

def display_products_with_reviews():
    conn = sqlite3.connect('shopping_mall.db')
    cursor = conn.cursor()

    # Using DML, SFW, ORDER BY, GROUP BY, and HAVING
    cursor.execute("""
        SELECT 
            p.id, p.product_name, p.product_price, p.brand, p.sales_quantity, p.stock_quantity, 
            AVG(r.rating) AS avg_rating, COUNT(r.id) AS review_count 
        FROM 
            products p 
            LEFT JOIN reviews r ON p.id = r.product_id 
        GROUP BY 
            p.id, p.product_name, p.product_price, p.brand, p.sales_quantity, p.stock_quantity
        HAVING 
            AVG(r.rating) >= 4
        ORDER BY 
            avg_rating DESC
    """)
    products = cursor.fetchall()

    conn.close()

    # Find the maximum length of the product names
    max_product_name_length = max(len(str(product[1])) for product in products)

    # Set the minimum column width
    min_column_width = 8

    # Calculate the column widths
    id_width = max(min_column_width, len(str(max(product[0] for product in products))))
    name_width = max(min_column_width, max_product_name_length)
    price_width = max(min_column_width, len('가격'))
    brand_width = max(min_column_width, len('브랜드'))
    sales_width = max(min_column_width, len('판매량'))
    stock_width = max(min_column_width, len('재고'))
    avg_rating_width = max(min_column_width, len('평균 평점')) + 2
    review_count_width = max(min_column_width, len('리뷰 수'))

    id_width2 = id_width 
    name_width2 = name_width - 3
    price_width2 = price_width - 2
    brand_width2 = brand_width - 3
    sales_width2 = sales_width - 3
    stock_width2 = stock_width - 2
    avg_rating_width2 = avg_rating_width - 4
    review_count_width2 = review_count_width - 3

    # Print the table with dynamic formatting
    border = f"┌{'─' * (id_width)}┬{'─' * (name_width )}┬{'─' * (price_width)}┬{'─' * (brand_width)}┬{'─' * (sales_width )}┬{'─' * (stock_width)}┬{'─' * (avg_rating_width)}┬{'─' * (review_count_width)}┐"
    print(border)
    print(f"│{'ID':^{id_width2}}│{'제품명':^{name_width2}}│{'가격':^{price_width2}}│{'브랜드':^{brand_width2}}│{'판매량':^{sales_width2}}│{'재고':^{stock_width2}}│{'평균 평점':^{avg_rating_width2}}│{'리뷰 수':^{review_count_width2}}│")
    print(f"├{'─' * (id_width)}┼{'─' * (name_width)}┼{'─' * (price_width )}┼{'─' * (brand_width)}┼{'─' * (sales_width )}┼{'─' * (stock_width)}┼{'─' * (avg_rating_width)}┼{'─' * (review_count_width)}┤")

    for product in products:
        print(f"│{product[0]:^{id_width}}│{product[1]:^{name_width}}│{product[2]:^{price_width}.2f}│{product[3]:^{brand_width}}│{product[4]:^{sales_width}}│{product[5]:^{stock_width}}│{product[6]:^{avg_rating_width}.2f}│{product[7]:^{review_count_width}}│")

    print(f"└{'─' * (id_width )}┴{'─' * (name_width)}┴{'─' * (price_width )}┴{'─' * (brand_width)}┴{'─' * (sales_width )}┴{'─' * (stock_width)}┴{'─' * (avg_rating_width)}┴{'─' * (review_count_width)}┘")


def main_loop():
    global role, username 

    while True:
        try:

            print_menu()

            choice = input("원하는 메뉴를 선택하세요: ")

            if choice == '12':
                return 0
            if not username and choice == '1':
                username = input("사용자 이름: ")
                password = input("비밀번호: ")
                role = login(username, password)
                if role:
                    print(f"{username}님, 환영합니다. 역할: {role}")
                else:
                    print("로그인에 실패했습니다. 다시 시도하세요.")
                    username = None  # Reset username if login fails
                    main_loop()  # Recursive call to retry login
            elif username and choice == '2' and (role != 'sell' and role != 'customer_service_representative'):
                display_products()
                purchase_option = input("제품을 구매하시겠습니까? (y/n): ").lower()
                if purchase_option == 'y':
                    purchase_product()
            elif username and choice == '3' and (role == 'admin' or role == 'sell'):
                add_product()
            elif username and choice == '4' and (role == 'admin' or role == 'sell'):
                delete_product()
            elif username and choice == '5' and role == 'admin':
                add_user()
            elif username and choice == '6' and (role == 'admin' or role == 'user' or role == 'sell'):
                display_products_with_reviews()
            elif username and choice == '7' and (role == 'admin' or role == 'user'):
                add_review()
            elif username and choice == '8' and (role == 'customer_service_representative' or role == 'admin'):
                display_original_inquiries()
            elif username and choice == '9' and (role == 'admin' or role == 'user'):
                add_inquiry()
            elif username and choice == '10' and (role == 'customer_service_representative' or role == 'admin'):
                respond_to_inquiry()
            elif username and choice == '11' and (role == 'customer_service_representative' or role == 'admin'):
                manage_inquiries()
            else:
                print("잘못된 선택입니다. 다시 시도하세요.")
            print("\n")
        except Exception as e:
            #print(f"오류 발생: {e}")
            print("잘못된 입력.")
            main_loop()

def print_menu():
    if not username:
        print("1. 로그인")
        print("12. 종료")
    else:
        print(f"1. 로그아웃: {username}")
        if role == 'sell':
            print("3. 제품 추가")
            print("4. 제품 삭제")
            print("5. 사용자 추가")
            print("6. 제품 및 리뷰 목록")
            print("11. 전체 문의 관리")
        elif role == 'admin':
            print("2. 쇼핑하기")
            print("3. 제품 추가")
            print("4. 제품 삭제")
            print("5. 사용자 추가")
            print("6. 제품 및 리뷰 목록")
            print("7. 제품 리뷰 등록")
            print("8. 고객 문의 관리")
            print("9. 고객 문의 등록")
            print("10. 문의 답변")
            print("11. 전체 문의 관리")
        elif role == 'user':
            print("2. 쇼핑하기")
            print("6. 제품 및 리뷰 목록")
            print("7. 제품 리뷰 등록")
            print("9. 고객 문의 등록")

        elif role == 'customer_service_representative':
            print("8. 고객 문의 관리")
            print("10. 문의 답변")
            print("11. 전체 문의 관리")

if __name__ == "__main__":
    main_loop()


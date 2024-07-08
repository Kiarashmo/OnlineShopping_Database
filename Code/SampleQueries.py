import argparse
import mysql.connector
from mysql.connector import Error
from pprint import pprint

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="kia09381395696",
            database="OnlineShopping"
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query, params=None):
    cursor = connection.cursor(dictionary=True)
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor.rowcount
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_select_query(connection, query, params=None):
    cursor = connection.cursor(dictionary=True)
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"The error '{e}' occurred")

# User sign up
def user_sign_up(connection, user_data):
    query = """
    INSERT INTO Users (username, password, name, email, contact_number, street, city, state, postal_code, country)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    params = (
        user_data['username'],
        user_data['password'],
        user_data['name'],
        user_data['email'],
        user_data['contact_number'],
        user_data['street'],
        user_data['city'],
        user_data['state'],
        user_data['postal_code'],
        user_data['country']
    )
    return execute_query(connection, query, params)

# User login
def user_login(connection, username, password):
    query = """
    SELECT * FROM Users WHERE username = %s AND password = %s;
    """
    params = (username, password)
    return execute_select_query(connection, query, params)

# Manager login
def manager_login(connection, username, password):
    query = """
    SELECT * FROM Managers WHERE username = %s AND password = %s;
    """
    params = (username, password)
    return execute_select_query(connection, query, params)

# Add new manager
def add_manager(connection, manager_data):
    query = """
    INSERT INTO Managers (username, password, email)
    VALUES (%s, %s, %s);
    """
    params = (
        manager_data['username'],
        manager_data['password'],
        manager_data['email']
    )
    return execute_query(connection, query, params)

# User-specific queries
def query_brand_availability(connection, brand_name):
    query = """
    SELECT name, status
    FROM Brands
    WHERE name = %s;
    """
    params = (brand_name,)
    return execute_select_query(connection, query, params)

def query_user_spending(connection, user_id, interval_days):
    query = """
    SELECT SUM(total_amount) AS total_spent
    FROM Orders
    WHERE user_id = %s AND order_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY) AND status != 'cancelled';
    """
    params = (user_id, interval_days)
    return execute_select_query(connection, query, params)

def query_user_orders(connection, user_id):
    query = """
    SELECT order_id, order_date, status, total_amount
    FROM Orders
    WHERE user_id = %s;
    """
    params = (user_id,)
    return execute_select_query(connection, query, params)

# Manager-specific queries
def query_users_with_recent_purchases(connection, interval_days):
    query = """
    SELECT name, email, contact_number
    FROM Users
    WHERE user_id IN (
        SELECT DISTINCT user_id
        FROM Orders
        WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
    );
    """
    params = (interval_days,)
    return execute_select_query(connection, query, params)

def query_total_sales_by_category(connection, interval_days):
    query = """
    SELECT c.name AS category, SUM(od.price * od.quantity) AS total_sales
    FROM OrderDetails od
    JOIN Products p ON od.product_id = p.product_id
    JOIN Categories c ON p.category_id = c.category_id
    JOIN Orders o ON od.order_id = o.order_id
    WHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
    GROUP BY c.name;
    """
    params = (interval_days,)
    return execute_select_query(connection, query, params)

def query_pending_orders(connection):
    query = """
    SELECT o.order_id, u.name AS user_name, o.order_date, o.total_amount
    FROM Orders o
    JOIN Users u ON o.user_id = u.user_id
    WHERE o.status = 'pending';
    """
    return execute_select_query(connection, query)

def query_low_stock_products(connection, stock_threshold):
    query = """
    SELECT name, stock
    FROM Products
    WHERE stock < %s;
    """
    params = (stock_threshold,)
    return execute_select_query(connection, query, params)

def query_high_spending_users(connection, amount_threshold):
    query = """
    SELECT u.name, u.email, SUM(o.total_amount) AS total_spent
    FROM Orders o
    JOIN Users u ON o.user_id = u.user_id
    GROUP BY u.user_id
    HAVING total_spent > %s;
    """
    params = (amount_threshold,)
    return execute_select_query(connection, query, params)

def query_add_discount(connection, discount_data):
    query = """
    INSERT INTO Discounts (name, description, discount_percentage, start_date, end_date)
    VALUES (%s, %s, %s, %s, %s);
    """
    params = (
        discount_data['name'],
        discount_data['description'],
        discount_data['discount_percentage'],
        discount_data['start_date'],
        discount_data['end_date']
    )
    return execute_query(connection, query, params)

def query_label_comment_inappropriate(connection, comment_id, manager_id):
    query = """
    UPDATE Comments
    SET status = 'inappropriate', moderated_by = %s
    WHERE comment_id = %s;
    """
    params = (manager_id, comment_id)
    return execute_query(connection, query, params)

def query_top_selling_products_last_month(connection, limit=5):
    query = """
    SELECT p.name AS product, SUM(od.price * od.quantity) AS total_sales
    FROM OrderDetails od
    JOIN Products p ON od.product_id = p.product_id
    JOIN Orders o ON od.order_id = o.order_id
    WHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
    GROUP BY p.name
    ORDER BY total_sales DESC
    LIMIT %s;
    """
    params = (limit,)
    return execute_select_query(connection, query, params)

def query_inactive_brands_product_count(connection):
    query = """
    SELECT b.name AS brand, COUNT(p.product_id) AS product_count
    FROM Brands b
    JOIN Products p ON b.brand_id = p.brand_id
    WHERE b.status = 'inactive'
    GROUP BY b.name;
    """
    return execute_select_query(connection, query)

def query_total_discount_by_product_last_month(connection):
    query = """
    SELECT p.name AS product, SUM(d.discount_percentage * od.price * od.quantity / 100) AS total_discount
    FROM ProductDiscounts pd
    JOIN Discounts d ON pd.discount_id = d.discount_id
    JOIN Products p ON pd.product_id = p.product_id
    JOIN OrderDetails od ON p.product_id = od.product_id
    JOIN Orders o ON od.order_id = o.order_id
    WHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
    GROUP BY p.name;
    """
    return execute_select_query(connection, query)

# Custom query for managers
def query_custom_sql(connection, custom_query):
    return execute_select_query(connection, custom_query)

def main():
    connection = create_connection()

    parser = argparse.ArgumentParser(description="Online Shopping CLI")
    subparsers = parser.add_subparsers(dest="role", help="Role (user or manager)")

    # User subcommands
    user_parser = subparsers.add_parser("user", help="User actions")
    user_subparsers = user_parser.add_subparsers(dest="action", help="User actions")

    user_sign_up_parser = user_subparsers.add_parser("sign_up", help="Sign up a new user")
    user_sign_up_parser.add_argument("--username", required=True)
    user_sign_up_parser.add_argument("--password", required=True)
    user_sign_up_parser.add_argument("--name", required=True)
    user_sign_up_parser.add_argument("--email", required=True)
    user_sign_up_parser.add_argument("--contact_number", required=True)
    user_sign_up_parser.add_argument("--street", required=True)
    user_sign_up_parser.add_argument("--city", required=True)
    user_sign_up_parser.add_argument("--state", required=True)
    user_sign_up_parser.add_argument("--postal_code", required=True)
    user_sign_up_parser.add_argument("--country", required=True)

    user_login_parser = user_subparsers.add_parser("login", help="Login as user")
    user_login_parser.add_argument("--username", required=True)
    user_login_parser.add_argument("--password", required=True)

    # Manager subcommands
    manager_parser = subparsers.add_parser("manager", help="Manager actions")
    manager_subparsers = manager_parser.add_subparsers(dest="action", help="Manager actions")

    manager_login_parser = manager_subparsers.add_parser("login", help="Login as manager")
    manager_login_parser.add_argument("--username", required=True)
    manager_login_parser.add_argument("--password", required=True)

    add_manager_parser = manager_subparsers.add_parser("add_manager", help="Add a new manager")
    add_manager_parser.add_argument("--username", required=True)
    add_manager_parser.add_argument("--password", required=True)
    add_manager_parser.add_argument("--email", required=True)

    manager_query_parser = manager_subparsers.add_parser("query", help="Query options for managers")
    manager_query_parser.add_argument("query_choice", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], help="Choose a query:\n1: Users with recent purchases\n2: Total sales by category\n3: Pending orders\n4: Low stock products\n5: High spending users\n6: Add discount\n7: Label comment inappropriate\n8: Top selling products last month\n9: Inactive brands and product count\n10: Total discount by product last month")
    manager_query_parser.add_argument("--interval_days", type=int, help="Interval days for recent purchases or sales by category queries")
    manager_query_parser.add_argument("--stock_threshold", type=int, help="Stock threshold for low stock products query")
    manager_query_parser.add_argument("--amount_threshold", type=float, help="Amount threshold for high spending users query")
    manager_query_parser.add_argument("--discount_data", type=str, help="Discount data for adding discount query in JSON format")
    manager_query_parser.add_argument("--comment_id", type=int, help="Comment ID for labeling comment inappropriate")
    manager_query_parser.add_argument("--manager_id", type=int, help="Manager ID for labeling comment inappropriate")
    manager_query_parser.add_argument("--limit", type=int, help="Limit for top selling products last month query")

    custom_query_parser = manager_subparsers.add_parser("custom_query", help="Execute a custom SQL query")
    custom_query_parser.add_argument("--query", required=True)

    args = parser.parse_args()

    if args.role == "user":
        if args.action == "sign_up":
            user_data = {
                'username': args.username,
                'password': args.password,
                'name': args.name,
                'email': args.email,
                'contact_number': args.contact_number,
                'street': args.street,
                'city': args.city,
                'state': args.state,
                'postal_code': args.postal_code,
                'country': args.country
            }
            result = user_sign_up(connection, user_data)
            print(f"User signed up, rows affected: {result}")

        elif args.action == "login":
            user_data = user_login(connection, args.username, args.password)
            if user_data:
                print("User logged in successfully.")
                # User-specific actions
                while True:
                    user_query_choice = input("Choose a query:\n1: Check brand availability\n2: Check total spending in a month\n3: List of user's orders\n0: Exit\n")
                    if user_query_choice == "0":
                        break
                    elif user_query_choice == "1":
                        brand_name = input("Enter brand name: ")
                        result = query_brand_availability(connection, brand_name)
                    elif user_query_choice == "2":
                        interval_days = int(input("Enter interval days: "))
                        user_id = user_data[0]['user_id']
                        result = query_user_spending(connection, user_id, interval_days)
                    elif user_query_choice == "3":
                        user_id = user_data[0]['user_id']
                        result = query_user_orders(connection, user_id)
                    else:
                        print("Invalid choice")
                        continue
                    pprint(result)

    elif args.role == "manager":
        if args.action == "login":
            manager_data = manager_login(connection, args.username, args.password)
            if manager_data:
                print("Manager logged in successfully.")
                # Manager-specific actions
                while True:
                    manager_query_choice = input("Choose a query:\n1: Users with recent purchases\n2: Total sales by category\n3: Pending orders\n4: Low stock products\n5: High spending users\n6: Add discount\n7: Label comment inappropriate\n8: Top selling products last month\n9: Inactive brands and product count\n10: Total discount by product last month\n11: Custom query\n0: Exit\n")
                    if manager_query_choice == "0":
                        break
                    elif manager_query_choice == "1":
                        interval_days = int(input("Enter interval days: "))
                        result = query_users_with_recent_purchases(connection, interval_days)
                    elif manager_query_choice == "2":
                        interval_days = int(input("Enter interval days: "))
                        result = query_total_sales_by_category(connection, interval_days)
                    elif manager_query_choice == "3":
                        result = query_pending_orders(connection)
                    elif manager_query_choice == "4":
                        stock_threshold = int(input("Enter stock threshold: "))
                        result = query_low_stock_products(connection, stock_threshold)
                    elif manager_query_choice == "5":
                        amount_threshold = float(input("Enter amount threshold: "))
                        result = query_high_spending_users(connection, amount_threshold)
                    elif manager_query_choice == "6":
                        discount_data = {
                            'name': input("Enter discount name: "),
                            'description': input("Enter discount description: "),
                            'discount_percentage': float(input("Enter discount percentage: ")),
                            'start_date': input("Enter start date (YYYY-MM-DD): "),
                            'end_date': input("Enter end date (YYYY-MM-DD): ")
                        }
                        result = query_add_discount(connection, discount_data)
                    elif manager_query_choice == "7":
                        comment_id = int(input("Enter comment ID: "))
                        manager_id = int(input("Enter manager ID: "))
                        result = query_label_comment_inappropriate(connection, comment_id, manager_id)
                    elif manager_query_choice == "8":
                        limit = int(input("Enter limit: "))
                        result = query_top_selling_products_last_month(connection, limit)
                    elif manager_query_choice == "9":
                        result = query_inactive_brands_product_count(connection)
                    elif manager_query_choice == "10":
                        result = query_total_discount_by_product_last_month(connection)
                    elif manager_query_choice == "11":
                        custom_query = input("Enter your custom SQL query: ")
                        result = query_custom_sql(connection, custom_query)
                    else:
                        print("Invalid choice")
                        continue
                    pprint(result)

        elif args.action == "add_manager":
            manager_data = {
                'username': args.username,
                'password': args.password,
                'email': args.email
            }
            result = add_manager(connection, manager_data)
            print(f"Manager added, rows affected: {result}")

        elif args.action == "custom_query":
            result = query_custom_sql(connection, args.query)
            pprint(result)

    if connection:
        connection.close()
        print("Connection closed")

if __name__ == "__main__":
    main()
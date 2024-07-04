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

# Query 1:
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

#Query 2:
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

# Query 3:
def query_pending_orders(connection):
    query = """
    SELECT o.order_id, u.name AS user_name, o.order_date, o.total_amount
    FROM Orders o
    JOIN Users u ON o.user_id = u.user_id
    WHERE o.status = 'pending';
    """
    return execute_select_query(connection, query)

# Query 4:
def query_low_stock_products(connection, stock_threshold):
    query = """
    SELECT name, stock
    FROM Products
    WHERE stock < %s;
    """
    params = (stock_threshold,)
    return execute_select_query(connection, query, params)

# Query 5:
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

# Query 6:
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

# Query 7:
def query_label_comment_inappropriate(connection, comment_id, manager_id):
    query = """
    UPDATE Comments
    SET status = 'inappropriate', moderated_by = %s
    WHERE comment_id = %s;
    """
    params = (manager_id, comment_id)
    return execute_query(connection, query, params)

# Query 8:
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

# Query 9:
def query_inactive_brands_product_count(connection):
    query = """
    SELECT b.name AS brand, COUNT(p.product_id) AS product_count
    FROM Brands b
    JOIN Products p ON b.brand_id = p.brand_id
    WHERE b.status = 'inactive'
    GROUP BY b.name;
    """
    return execute_select_query(connection, query)

# Query 10:
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

# Example of usage:
if __name__ == "__main__":
    connection = create_connection()

    if connection:
        # Example: Get users with recent purchases (Query 1)
        print("1. Users with recent purchases:")
        interval_days = 30 
        users_with_recent_purchases = query_users_with_recent_purchases(connection, interval_days)
        pprint(users_with_recent_purchases)

        # Example: Get total sales by category (Query 2)
        print("2. Total sales by category:")
        total_sales_by_category = query_total_sales_by_category(connection, interval_days)
        pprint(total_sales_by_category)

        # Example: Get pending orders (Query 3)
        print("3. Pending orders:")
        pending_orders = query_pending_orders(connection)
        pprint(pending_orders)

        # Example: Get low stock products (Query 4)
        print("4. Low stock products:")
        stock_threshold = 10
        low_stock_products = query_low_stock_products(connection, stock_threshold)
        pprint(low_stock_products)

        # Example: Get high spending users (Query 5)
        print("6. High spending users:")
        amount_threshold = 100
        high_spending_users = query_high_spending_users(connection, amount_threshold)
        pprint(high_spending_users)

        # Example: Add a discount to the discount list (Query 6)
        print("7. Adding a discount to the discount list:")
        discount_data = {
            'name': 'Summer Sale',
            'description': '20% off on all items during the summer sale',
            'discount_percentage': 20.00,
            'start_date': '2024-07-01',
            'end_date': '2024-07-31'
        }
        add_discount_result = query_add_discount(connection, discount_data)
        print(f"Number of rows affected: {add_discount_result}")

        # Example: Label a comment as inappropriate (Query 7)
        print("8. Labeling a comment as inappropriate:")
        comment_id = 10 
        manager_id = 1  
        label_comment_result = query_label_comment_inappropriate(connection, comment_id, manager_id)
        print(f"Number of rows affected: {label_comment_result}")

        # Example: Get top selling products last month (Query 8)
        print("9. Top selling products last month:")
        limit = 5 
        top_selling_products = query_top_selling_products_last_month(connection, limit)
        pprint(top_selling_products)

        # Example: Get inactive brands and product count (Query 9)
        print("10. Inactive brands and product count:")
        inactive_brands_product_count = query_inactive_brands_product_count(connection)
        pprint(inactive_brands_product_count)

        # Example: Get total discount by product last month (Query 10)
        print("11. Total discount by product last month:")
        total_discount_by_product = query_total_discount_by_product_last_month(connection)
        pprint(total_discount_by_product)

    if connection:
        connection.close()
        print("Connection closed")
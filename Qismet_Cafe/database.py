import mysql.connector
import DbConfig

PIN_CODES = {
    "Admin": "1234",
    "Customer": "2345",
    "Barista": "3456"
}

PRODUCTS = [
    {"name": "Espresso", "image": "espresso.jpg", "price": {"SMALL": 80, "MEDIUM": 100, "LARGE": 120}, "category": "Coffee"},
    {"name": "Americano", "image": "americano.jpg", "price": {"SMALL": 90, "MEDIUM": 110, "LARGE": 130}, "category": "Coffee"},
    {"name": "Cappuccino", "image": "capuccino.jpg", "price": {"SMALL": 100, "MEDIUM": 120, "LARGE": 140}, "category": "Coffee"},
    {"name": "Macchiato", "image": "macchiato.jpg", "price": {"SMALL": 100, "MEDIUM": 120, "LARGE": 140}, "category": "Coffee"},
    {"name": "Caramel Dolce Latte", "image": "caramel dolce latte.jpg", "price": {"SMALL": 110, "MEDIUM": 130, "LARGE": 150}, "category": "Coffee"},
    {"name": "Mocha", "image": "mocha.jpg", "price": {"SMALL": 110, "MEDIUM": 130, "LARGE": 150}, "category": "Coffee"},
    {"name": "Oreo Milkshake", "image": "oreo_milkshake.jpg", "price": {"SMALL": 90, "MEDIUM": 110, "LARGE": 130}, "category": "Non-Coffee"},
    {"name": "Matcha Latte", "image": "matcha_latte.jpg", "price": {"SMALL": 100, "MEDIUM": 120, "LARGE": 140}, "category": "Non-Coffee"},
    {"name": "Chai Latte", "image": "chai.jpg", "price": {"SMALL": 95, "MEDIUM": 115, "LARGE": 135}, "category": "Non-Coffee"},
    {"name": "Banana Milkshake", "image": "banana.jpg", "price": {"SMALL": 95, "MEDIUM": 115, "LARGE": 135}, "category": "Non-Coffee"},
    {"name": "Strawberry Shake", "image": "strawberry.jpg", "price": {"SMALL": 90, "MEDIUM": 110, "LARGE": 130}, "category": "Non-Coffee"},
    {"name": "Iced Lemon Tea", "image": "lemon.jpg", "price": {"SMALL": 100, "MEDIUM": 120, "LARGE": 140}, "category": "Non-Coffee"},
    {"name": "Cookies", "image": "cookies.jpg", "price": 60, "category": "Pastries", "flavors": ["Chocolate Chip", "Oatmeal Raisin", "Double Chocolate"]},
    {"name": "Muffins", "image": "muffins.jpg", "price": 70, "category": "Pastries", "flavors": ["Blueberry", "Banana Nut", "Chocolate"]},
    {"name": "Croissant", "image": "croissant.jpg", "price": 75, "category": "Pastries", "flavors": ["Plain", "Chocolate", "Almond"]},
    {"name": "Donut", "image": "donut.jpg", "price": 50, "category": "Pastries", "flavors": ["Glazed", "Chocolate", "Strawberry"]},
    {"name": "Brownie", "image": "brownie.jpg", "price": 65, "category": "Pastries", "flavors": ["Classic", "Walnut", "Caramel"]},
    {"name": "Cheesecake", "image": "cheesecake.jpg", "price": 85, "category": "Pastries", "flavors": ["New York", "Blueberry", "Mango"]},
]

def create_database_if_not_exists():
    try:
        connection = mysql.connector.connect(
            user=DbConfig.DB_CONFIG['user'],
            password=DbConfig.DB_CONFIG['password'],
            host=DbConfig.DB_CONFIG['host']
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS qismet_cafe")
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")

def connect():
    return DbConfig.connect()

def initialize_tables():
    conn = connect()
    cursor = conn.cursor()

    TABLES = {}

    TABLES['Users'] = """
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            role ENUM('Customer', 'Admin', 'Barista') NOT NULL,
            pin VARCHAR(10) NOT NULL
        )"""

    TABLES['Categories'] = """
        CREATE TABLE IF NOT EXISTS Categories (
            category_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE
        )"""

    TABLES['Menu'] = """
        CREATE TABLE IF NOT EXISTS Menu (
            menu_id INT AUTO_INCREMENT PRIMARY KEY,
            category_id INT,
            name VARCHAR(100) NOT NULL,
            price SMALLINT NOT NULL,
            size ENUM('SMALL', 'MEDIUM', 'LARGE') DEFAULT NULL,
            image VARCHAR(255),
            vat_percent DECIMAL(5,2) DEFAULT 12.00,
            flavors TEXT DEFAULT NULL,
            is_hidden BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (category_id) REFERENCES Categories(category_id)
        )"""

    TABLES['Orders'] = """
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            order_type ENUM('Dine In', 'Take Out') NOT NULL,
            status ENUM('Pending', 'Preparing', 'Ready', 'Completed') DEFAULT 'Pending',
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )"""

    TABLES['orderitems'] = """
        CREATE TABLE IF NOT EXISTS orderitems (
            order_item_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT,
            menu_id INT,
            quantity INT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (menu_id) REFERENCES menu(menu_id) ON DELETE CASCADE
        )"""

    TABLES['Payments'] = """
        CREATE TABLE IF NOT EXISTS Payments (
            payment_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT,
            method ENUM('Cash', 'E-Wallet') NOT NULL,
            vat_total DECIMAL(10,2) DEFAULT 0.00,
            paid_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id)
        )"""

    TABLES['SalesReport'] = """
        CREATE TABLE IF NOT EXISTS SalesReport (
            report_id INT AUTO_INCREMENT PRIMARY KEY, 
            order_date DATE,                         
            item_name VARCHAR(100),                 
            total_orders INT,                     
            total_qty INT,                         
            total_vat DECIMAL(10,2) DEFAULT 0.00,   
            total_sales DECIMAL(10,2) DEFAULT 0.00  
        )"""

    TABLES['OrderStatusLog'] = """
        CREATE TABLE IF NOT EXISTS OrderStatusLog (
            log_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT,
            updated_by INT,
            new_status ENUM('Preparing', 'Ready', 'Completed'),
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id),
            FOREIGN KEY (updated_by) REFERENCES Users(user_id)
        )"""

    for table_name in TABLES:
        cursor.execute(TABLES[table_name])

    conn.commit()
    cursor.close()
    conn.close()

def insert_initial_data():
    conn = connect()
    cursor = conn.cursor()

    for role, pin in PIN_CODES.items():
        cursor.execute("INSERT IGNORE INTO Users (role, pin) VALUES (%s, %s)", (role, pin))

    categories = set(p['category'] for p in PRODUCTS)
    for category in categories:
        cursor.execute("INSERT IGNORE INTO Categories (name) VALUES (%s)", (category,))

    conn.commit()

    cursor.execute("SELECT category_id, name FROM Categories")
    category_map = {name: cid for cid, name in cursor.fetchall()}

    for product in PRODUCTS:
        cat_id = category_map[product['category']]
        image = product.get('image', '')
        flavors = ','.join(product.get('flavors', [])) if product.get('flavors') else None

        if isinstance(product['price'], dict):
            for size, price in product['price'].items():
                cursor.execute("""
                    INSERT INTO Menu (category_id, name, price, size, image, flavors)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (cat_id, product['name'], price, size, image, flavors))
        else:
            cursor.execute("""
                INSERT INTO Menu (category_id, name, price, size, image, flavors)
                VALUES (%s, %s, %s, NULL, %s, %s)
            """, (cat_id, product['name'], product['price'], image, flavors))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_database_if_not_exists()
    initialize_tables()
    insert_initial_data()
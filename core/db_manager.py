import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self, host="localhost", user="root", password="", database="botgame"):
        """
        Initialize the connection to the database.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """
        Connect to the MySQL database.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error: {e}")

    def create_table(self):
        """
        Create the TabImages table if it doesn't exist.
        """
        try:
            cursor = self.connection.cursor()
            create_table_query = """
            CREATE TABLE IF NOT EXISTS TabImages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                unique_id VARCHAR(255) NOT NULL UNIQUE,
                game_name VARCHAR(255) NOT NULL,
                tab_name VARCHAR(255) NOT NULL,
                image_name VARCHAR(255) NOT NULL,
                config_file_path VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_table_query)
            self.connection.commit()
            print("Table TabImages created successfully")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def insert_data(self, unique_id, game_name, tab_name, image_name, config_file_path):
        """
        Insert data into the TabImages table.
        """
        try:
            cursor = self.connection.cursor()
            insert_query = """
            INSERT INTO TabImages (unique_id, game_name, tab_name, image_name, config_file_path)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (unique_id, game_name, tab_name, image_name, config_file_path))
            self.connection.commit()
            print("Data inserted successfully")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def fetch_all(self, game_name=None):    
        """
        Fetch all rows from the TabImages table, optionally filtered by game_name.
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            if game_name:
                # Query with filtering by game_name
                query = "SELECT * FROM TabImages WHERE game_name = %s;"
                cursor.execute(query, (game_name,))
            else:
                # Query to fetch all rows
                query = "SELECT * FROM TabImages;"
                cursor.execute(query)

            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()


    def close_connection(self):
        """
        Close the database connection.
        """
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

# Example usage
if __name__ == "__main__":
    # สร้าง DatabaseManager instance
    db_manager = DatabaseManager(host="localhost", user="root", password="Password!123", database="botgame")

    # เชื่อมต่อฐานข้อมูล
    db_manager.connect()

    # ดึงข้อมูลที่มี game_name = 'MyGame'
    mygame_data = db_manager.fetch_all(game_name="MyGame")
    print(mygame_data)

    # ปิดการเชื่อมต่อ
    db_manager.close_connection()

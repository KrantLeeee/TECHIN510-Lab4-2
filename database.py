import psycopg2
import os

class Database:
    def __init__(self, database_url) -> None:
        self.con = psycopg2.connect(database_url)
        self.cur = self.con.cursor()

    def create_table(self):
        q = """
        CREATE TABLE IF NOT EXISTS books (
            id INT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            price TEXT NOT NULL,
            rating TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.cur.execute(q)
        self.con.commit()

    def insert_book(self, book):
        q = """
        INSERT INTO books (id, title, description, price, rating) VALUES (%s, %s, %s, %s, %s)
        """
        self.cur.execute(q, (book['book_id'], book['title'], book['description'], book['price'], book['rating'],))
        self.con.commit()
    
    def truncate_table(self):
        self.cur.execute("TRUNCATE TABLE books")
        self.con.commit()

    def search_books(self, search_term):
        q = """
        SELECT * FROM books
        WHERE title ILIKE %s OR description ILIKE %s
        """
        self.cur.execute(q, (f'%{search_term}%', f'%{search_term}%'))
        return self.cur.fetchall()

    def filter_and_order_books(self, order_by='rating', order_direction='ASC'):
        if order_by not in ['rating', 'price']:
            raise ValueError("order_by must be 'rating' or 'price'")
        if order_direction not in ['ASC', 'DESC']:
            raise ValueError("order_direction must be 'ASC' or 'DESC'")
        
        q = f"""
        SELECT * FROM books
        ORDER BY {order_by} {order_direction}
        """
        self.cur.execute(q)
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.con.close()

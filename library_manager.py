import sqlite3

# Database setup
DB_NAME = "library.db"

def connect_db():
    """Create a connection to the database and return the connection object."""
    return sqlite3.connect(DB_NAME)

def create_table():
    """Create the books table if it does not exist."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER
        )
        """)
        conn.commit()

def add_book(title, author, year):
    """Add a book to the database."""
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", 
                           (title, author, year))
            conn.commit()
            print(f"✅ Book '{title}' added successfully!")
    except Exception as e:
        print(f"❌ Error adding book: {e}")

def view_books():
    """Retrieve and display all books from the database."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()

        if books:
            print("\n📚 Your Library:")
            for book in books:
                print(f" {book[0]}. {book[1]} by {book[2]} ({book[3]})")
        else:
            print(" No books found.")

def update_book(book_id, title=None, author=None, year=None):
    """Update book details based on user input."""
    with connect_db() as conn:
        cursor = conn.cursor()

        # Fetch the existing record
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        book = cursor.fetchone()

        if not book:
            print("❌ Book not found.")
            return

        # Use the existing values if no new input is provided
        new_title = title if title else book[1]
        new_author = author if author else book[2]
        new_year = year if year else book[3]

        cursor.execute("UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?", 
                       (new_title, new_author, new_year, book_id))
        conn.commit()
        print("✅ Book updated successfully!")

def delete_book(book_id):
    """Delete a book from the database."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print("✅ Book deleted successfully!")
        else:
            print("❌ Book not found.")

# Command-line interface
if __name__ == "__main__":
    create_table()  # Ensure table exists

    while True:
        print("\n🔹 Personal Library Manager 🔹")
        print("1 Add a Book")
        print("2 View All Books")
        print("3 Update a Book")
        print("4 Delete a Book")
        print("5 Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            year = input("Enter publication year (optional): ")
            add_book(title, author, int(year) if year else None)

        elif choice == "2":
            view_books()

        elif choice == "3":
            book_id = int(input("Enter book ID to update: "))
            new_title = input("New title (press enter to keep current): ")
            new_author = input("New author (press enter to keep current): ")
            new_year = input("New year (press enter to keep current): ")
            update_book(book_id, new_title or None, new_author or None, int(new_year) if new_year else None)

        elif choice == "4":
            book_id = int(input("Enter book ID to delete: "))
            delete_book(book_id)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("❌ Invalid choice! Please try again.")

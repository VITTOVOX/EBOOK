import sqlite3

# Connect to (or create) the ebookstore database
conn = sqlite3.connect('ebookstore.db')
cursor = conn.cursor()

# Create the book table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        qty INTEGER
    )
''')

# Insert the initial books
initial_books = [
    (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
    (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
    (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
    (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
    (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
]

cursor.executemany('''
    INSERT OR IGNORE INTO book (id, title, author, qty)
    VALUES (?, ?, ?, ?)
''', initial_books)

conn.commit()

# Menu options
def enter_book():
    try:
        id = int(input("Enter book ID: "))
        title = input("Enter book title: ")
        author = input("Enter author name: ")
        qty = int(input("Enter quantity: "))
        cursor.execute("INSERT INTO book (id, title, author, qty) VALUES (?, ?, ?, ?)",
                       (id, title, author, qty))
        conn.commit()
        print("Book added successfully.")
    except Exception as e:
        print(f"Error: {e}")

def update_book():
    try:
        id = int(input("Enter the ID of the book to update: "))
        field = input("Enter the field to update (title, author, qty): ").lower()
        new_value = input("Enter the new value: ")
        if field == "qty":
            new_value = int(new_value)
        cursor.execute(f"UPDATE book SET {field} = ? WHERE id = ?", (new_value, id))
        conn.commit()
        print("Book updated successfully.")
    except Exception as e:
        print(f"Error: {e}")

def delete_book():
    try:
        id = int(input("Enter the ID of the book to delete: "))
        cursor.execute("DELETE FROM book WHERE id = ?", (id,))
        conn.commit()
        print("Book deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")

def search_books():
    try:
        keyword = input("Enter the title or part of the title to search: ")
        cursor.execute("SELECT * FROM book WHERE title LIKE ?", ('%' + keyword + '%',))
        results = cursor.fetchall()
        if results:
            for book in results:
                print(book)
        else:
            print("No books found.")
    except Exception as e:
        print(f"Error: {e}")

# Main loop
while True:
    print("\nMenu:")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("0. Exit")

    choice = input("Enter your choice: ")
    if choice == '1':
        enter_book()
    elif choice == '2':
        update_book()
    elif choice == '3':
        delete_book()
    elif choice == '4':
        search_books()
    elif choice == '0':
        break
    else:
        print("Invalid choice. Please try again.")

# Close the connection
conn.close()
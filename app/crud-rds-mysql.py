from flask import Flask, request, jsonify
import mysql.connector
from connection import config
import logging


app = Flask(__name__)
logging.basicConfig(filename='access.log', level=logging.INFO, 
                    format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
access_logger = logging.getLogger('access_logger')

@app.before_request
def log_request_info():
    log_data = f"{request.remote_addr} - {request.method} {request.path} - {request.user_agent}"
    access_logger.info(log_data)


# Create connection to the MySQL database
db = mysql.connector.connect(**config)

# Create a cursor object to interact with the database
cursor = db.cursor()

# Create the 'mybook' table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS mybooks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    author VARCHAR(255),
    title VARCHAR(255),
    isbn INT
)
"""
cursor.execute(create_table_query)


# Route to get all books
@app.route('/books', methods=['GET'])
def get_books():
    print("1- get all books")
    select_query = "SELECT * FROM mybook"
    cursor.execute(select_query)
    books = cursor.fetchall()
    
    # Convert the result to a list of dictionaries
    books_list = []
    for book in books:
        book_dict = {
            'id': book[0],
            'author': book[1],
            'title': book[2],
            'isbn': book[3]
        }
        books_list.append(book_dict)
        print("2) get all books")
    
    return jsonify(books_list)


# Route to add a new book
@app.route('/books', methods=['POST'])
def add_book():
    print("1)add a new book")
    book_data = request.get_json()
    author = book_data.get('author')
    title = book_data.get('title')
    isbn = book_data.get('isbn')
    
    insert_query = "INSERT INTO mybook (author, title, isbn) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (author, title, isbn))
    db.commit()
    
    print("add a new book")
    return jsonify({'message': 'Book added successfully'}), 201


# Route to update an existing book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book_data = request.get_json()
    author = book_data.get('author')
    title = book_data.get('title')
    isbn = book_data.get('isbn')
    
    update_query = "UPDATE mybook SET author=%s, title=%s, isbn=%s WHERE id=%s"
    cursor.execute(update_query, (author, title, isbn, book_id))
    db.commit()
    print("update an existing book")
    return jsonify({'message': 'Book updated successfully'})


# Route to delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    print("to delete a book")
    delete_query = "DELETE FROM mybook WHERE id=%s"
    cursor.execute(delete_query, book_id)
    db.commit()
    
    
    return jsonify({'message': 'Book deleted successfully'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


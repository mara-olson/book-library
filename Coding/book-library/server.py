from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_to_db, User, Book, Note
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/add-book', methods=['POST'])
def add_book():
    """Create a new book to save in db."""
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], year_published=data['year_published'], date_read=data['date_read'], rating=data['rating'], read=data['read'])
    db.session.add(new_book)
    db.session.commit()
    return f'{new_book.title} added successfully'

if __name__ == '__main__':
    connect_to_db(app)
    app.run()

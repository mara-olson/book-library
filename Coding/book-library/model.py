from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User id={self.id} username={self.username}'

class Book(db.Model):
    """A book."""
    __tablename__ = "books"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    year_published = db.Column(db.Integer)
    date_read = db.Column(db.DateTime)
    rating = db.Column(db.Integer)
    read = db.Column(db.Boolean)
    notes = db.relationship("Note", back_populates="book")

    @classmethod
    def create_book(cls, title, author, year_published=None, date_read=None, rating=None, read=False):
        """Add a new book to the database."""
        book = cls(title=title, author=author, year_published=year_published, date_read=date_read, rating=rating, read=read)
        
        db.session.add(book)
        db.session.commit()

        return book

    @classmethod
    def delete_book(cls, book_title, book_id=None):
        if book_id is not None:
            book = Book.query.get(book_id)
        else:
            book = Book.get_book_by_title(book_title)

        db.session.delete(book)
        db.session.commit()

    @classmethod
    def get_book_by_title(cls, title):
        """Retrieve a book by its title."""
        return Book.query.filter(Book.title==title).first()

    def __repr__(self):
        return f'<Book id={self.book_id} title={self.title}'


class Note(db.Model):
    """A book."""
    __tablename__ = "notes"

    note_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    book_title = db.Column(db.String, db.ForeignKey("books.title"))
    content = db.Column(db.Text)
    category = db.Column(db.String)
    quote = db.Column(db.Boolean)

    book = db.relationship("Book", back_populates="notes")
    
    @classmethod
    def create_note(cls, book, content):
        """Add a new book to the database."""
        note = cls(book=book, content=content)
        db.session.add(note)
        db.session.commit()

        return note

    @classmethod
    def delete_note(cls, book_title, note_id):
        if Note.query.get(note_id):
            note = Note.query.get(note_id)
        else:
            note = Note.query.filter(Note.book_title==book_title).first()

        db.session.delete(note)
        db.session.commit()
    

    def __repr__(self):
        return f'<Note id={self.note_id} content={self.content[:8]}'


def connect_to_db(app, db_uri="postgresql:///library", echo=True):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = echo

    db.app = app
    db.init_app(app)

    print('Connected to database!')
    # db.create_all()


if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    
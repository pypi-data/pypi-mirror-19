"""SQLAlchemy database model for blog posts."""
import getpass
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy import (
    create_engine, Column, ForeignKey, Integer,
    String, Table, Text
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


# SQLAlchemy objects
engine = create_engine('sqlite:///blog.db')
Base = declarative_base()
session = Session(bind=engine)


class Post(Base):
    """Blog posts
    Store blog posts with associated banner image
    and tags. Date assigned automatically when
    posted in the application."""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    content = Column(String(250))
    image = Column(String(250))
    date = Column(String(100))
    tags = relationship('Tag',
                secondary='post_tag_association')

    def __init__(self, title, content, image, date, tags):
        self.title = title
        self.content = content
        self.image = image
        self.date = date
        self.tags = tags

    @classmethod
    def random(cls):
        """Returns a new Post with random attribute text blocks.

            :field_len: = length of text blocks
            :post_data: = Post model arguments

        generates new Post with post_data.
        """

        from datetime import datetime

        def randomtext(length):
            """Returns a random string of text."""

            def randomletter():
                """Returns a random letter."""
                import random
                import string
                alphabet = string.ascii_lowercase
                return random.choice(alphabet)

            rand = ''.join(randomletter() for _ in range(length))
            return rand

        # set string field length
        TITLE = 100
        CONTENT = 200
        post_data = {
            'title': randomtext(TITLE),
            'content': randomtext(CONTENT),
            'date': datetime.today(),
            'image': '',
            'tags': []
        }
        return cls(**post_data)


class Tag(Base):
    """Tags for blog post categories."""
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __init__(self, name):
        self.name = name


class PostTagAssociation(Base):
    """Many-to-Many association table
    relationship()
     -> post
     -> tag
     """
    __tablename__ = 'post_tag_association'

    post_id = Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True)
    tag_id = Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
    post = relationship('Post')
    tag = relationship('Tag')


class User(Base):
    """User table
    Holds the login for Admin users."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50))

    def __init__(self, username):
        """Store a hashed password with a username."""
        def set_pass():
            password = getpass.getpass('Enter new password: ')
            pw_hash = generate_password_hash(password)
            return pw_hash
        self.username = username
        self.password = set_pass()  # stores hash

    def check_pass(self, password):
        """Returns `True` if password input
        matches the stored hash."""
        return check_password_hash(self.password, password)

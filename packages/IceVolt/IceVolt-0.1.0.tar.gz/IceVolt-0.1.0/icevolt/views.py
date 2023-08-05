"""View functions for the blog."""
from datetime import datetime
from flask import render_template, request
from sqlalchemy.exc import IntegrityError
from . import app
from .models import session, Post, Tag


@app.route('/', methods=['GET'])
@app.route('/page/<int:page>', methods=['GET'])
def main(page=1):
    posts_per_page = 10
    offset = (posts_per_page * (page - 1))
    start = 1 + offset
    stop = 10 + offset
    posts = session.query(Post).slice(start, stop)
    return render_template('blog.html', posts=posts)


@app.route('/new', methods=['GET', 'POST'])
def newpost():
    """Create new blog posts."""

    def post():
        """Push new post to the database."""
        form = request.form.to_dict()
        form['tags'] = []
        for tag_name in request.form.getlist('tags'):
            try:
                # add tags as new row objects
                tag = Tag(tag_name)
                session.add(tag)
                session.commit()
            except IntegrityError:
                session.rollback()
                tag = session.query(Tag).filter(Tag.name==tag_name).first()
            form['tags'].append(tag)
        # automatically assign date to blog post
        current_date = datetime.today()
        fmt_date = current_date.strftime('%A, %b %m, %Y  -  %I:%M%p')
        post = Post(**form, date=fmt_date)
        session.add(post)
        session.commit()
        return None

    def get():
        """Gets the list of existing tags from db.
        Loads form to create new posts."""
        return session.query(Tag).all()

    if request.method == 'POST':
        post()
        return render_template('newpost.html')
    else:
        tags = get()
        return render_template('newpost.html', tags=tags)


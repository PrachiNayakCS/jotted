#ths is the blog content blueprint

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from datetime import datetime


bp = Blueprint('blog', __name__)



@bp.route('/')
@login_required
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, edited, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY edited DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

# create view only when logged in 
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        created = datetime.now()
        edited = created
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, created, edited)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, body, g.user['id'], created, edited)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


# update and delete posts.Both the update and delete views will need to fetch a post by id and check if the author matches the logged in user. To avoid duplicating code, you can write a function to get the post and call it from each view.
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, edited, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        edited = datetime.now()
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, edited = ?'
                ' WHERE id = ?',
                (title, body, edited, id)
                
            )
            
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
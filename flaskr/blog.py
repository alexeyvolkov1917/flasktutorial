from flask import Blueprint,flash,g,redirect,render_template,request,url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog',__name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute('SELECT p.id,title,body,created,author_id,username'
                       ' FROM post p JOIN user u ON p.author_id = u.id'
                       ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    sql = 'INSERT INTO post (title,body,author_id) VALUES (?, ?, ?)'
    id = g.user['id']
    path = 'blog/create.html'
    return ifpost(sql, id, path)


def get_post(id,check_author=True):
    post = get_db().execute(
        'SELECT p.id, title,body,created,author_id,username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        " WHERE p.id = ?",
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

def ifpost(sql, id, path ,post=None):
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title:
            flash('Title is required.')
            return render_template(path,post=post)
        else:
            db = get_db()
            db.execute(sql, (title, body, id))
            db.commit()
            return redirect(url_for('blog.index'))
    else:
        return render_template(path,post=post)



@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    sql = 'UPDATE post SET title = ?, body = ? WHERE id = ?'
    path = 'blog/update.html'
    return ifpost(sql,id,path,get_post(id))

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


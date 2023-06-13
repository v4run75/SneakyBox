import os

from flask import Flask
from . import db
from flask import render_template
from . import home
from . import auth
from flaskr.db import get_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='bl0g.c!f-443',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.debug = False

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp)

    @app.route('/')
    def homePage():
        db = get_db()
        posts = db.execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' ORDER BY created DESC'
        ).fetchall()
        return render_template('home.html', posts=posts)

    @app.route('/')
    def homePageRedirect(redirectArgument):
        db = get_db()
        posts = db.execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' ORDER BY created DESC'
        ).fetchall()
        return render_template('home.html', posts=posts, anchor=redirectArgument)


    def get_post(post_id):
        post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (post_id,)
        ).fetchone()
        # post = get_db().execute(
        #     'SELECT * FROM post WHERE id = ?', (post_id,)
        # ).fetchone()
        return post
            

    @app.route("/post/<int:post_id>")
    def postSingle(post_id):
        post = get_post(post_id)
        return render_template("auth/post-single.html", post=post)    

    return app
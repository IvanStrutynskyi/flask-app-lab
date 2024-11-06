import json
from . import post_bp
from flask import render_template, abort, flash, redirect, url_for
from .forms import PostForm
from datetime import datetime

POSTS_FILE = 'app/posts/posts.json'  

def save_post(post):
    try:
        with open(POSTS_FILE, 'r') as f:
            posts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        posts = []

    posts.append(post)

    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=4)

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = {
            "id": datetime.now().strftime('%Y%m%d%H%M%S'),  
            "title": form.title.data,
            "content": form.content.data,
            "category": form.category.data,
            "is_active": form.is_active.data,
            "publish_date": form.publish_date.data.strftime('%Y-%m-%d'),
            "author": "Ivan"  
        }
        
        save_post(post)
        flash(f'Post "{form.title.data}" added successfully!', 'success')
        return redirect(url_for('.get_posts'))
    
    return render_template("add_post.html", form=form)

@post_bp.route('/posts')
def get_posts():
    try:
        with open(POSTS_FILE, 'r') as f:
            posts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        posts = []

    return render_template("posts.html", posts=posts)

@post_bp.route('/posts/<int:id>')
def detail_post(id):
    try:
        with open(POSTS_FILE, 'r') as f:
            posts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        abort(404)
    
    post = next((post for post in posts if int(post["id"]) == id), None)
    if post is None:
        abort(404)
    
    return render_template("detail_post.html", post=post)

@post_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

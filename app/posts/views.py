from . import post_bp
from flask import render_template, request, abort, flash, redirect, url_for
from .forms import PostForm
from .models import Post
from app import db

from .utils import save_post, load_posts, get_post

# Функція для додавання поста
@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        category = form.category.data  # Додаємо категорію
        author = form.author.data  # Додаємо автора
        is_active = form.is_active.data  # Додаємо поле активності
        publish_date = form.publish_date.data  # Додаємо дату публікації
        
        # Створюємо новий пост
        post_new = Post(
            title=title, 
            content=content, 
            category=category,
            author=author,
            is_active=is_active,
            posted=publish_date  # Це поле зберігається як "posted"
        )
        
        # Додаємо пост до сесії та зберігаємо його в базі даних
        db.session.add(post_new)
        db.session.commit()
        
        # Сповіщаємо про успішне додавання поста
        flash(f'Post "{title}" added successfully!', 'success')
        
        # Переходимо до списку постів
        return redirect(url_for('.get_posts'))
    
    elif form.errors:
        flash(f"Enter the correct data in the form!", "danger")
   
    return render_template("add_post.html", form=form)

# Доданий маршрут для видалення поста
@post_bp.route('/delete_post/<int:id>', methods=['GET', 'POST'])
def delete_post(id):
    # Отримуємо пост по id
    post = Post.query.get(id)
    
    if post:
        # Видаляємо пост з бази даних
        db.session.delete(post)
        db.session.commit()

        # Сповіщаємо про успішне видалення
        flash(f'Post "{post.title}" deleted successfully!', 'success')
    else:
        # Якщо пост не знайдений, сповіщаємо про помилку
        flash('Post not found!', 'danger')
    
    # Переходимо до списку постів після видалення
    return redirect(url_for('posts.get_posts'))

# Функція для отримання всіх постів
@post_bp.route('/') 
def get_posts():
    stmt = db.select(Post).order_by(Post.posted.desc())  # Отримуємо всі пости, відсортовані за датою публікації по спаданні
    posts = db.session.scalars(stmt).all()  # Виконуємо запит і отримуємо всі пости
    return render_template("posts.html", posts=posts)


@post_bp.route('/<int:id>')
def detail_post(id):
    # Отримуємо пост із бази даних за id
    post = Post.query.get(id)
    if post:
        return render_template('detail_post.html', post=post)
    return abort(404)  # Якщо пост не знайдений, повертаємо помилку 404

# Доданий маршрут для редагування поста
@post_bp.route('/edit_post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    # Отримуємо пост із бази даних за id
    post = Post.query.get(id)
    if not post:
        flash('Post not found!', 'danger')
        return redirect(url_for('.get_posts'))

    form = PostForm(obj=post)  # Заповнюємо форму існуючими даними поста

    if form.validate_on_submit():
        # Оновлюємо пост на основі даних форми
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.author = form.author.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data

        # Зберігаємо оновлені дані в базі даних
        db.session.commit()

        # Сповіщаємо про успішне редагування
        flash(f'Post "{post.title}" updated successfully!', 'success')
        
        # Переходимо до детальної сторінки цього поста
        return redirect(url_for('.detail_post', id=post.id))

    return render_template('edit_post.html', form=form, post=post)

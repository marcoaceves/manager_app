
from dataclasses import dataclass
from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.task import Task
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.like import Like


# html page for adding
@app.route('/announcements')
def announcemets():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    users= User.get_all()
    posts = Post.get_all_posts(data)
    print(posts)
    return render_template('announcements.html', user=User.get_one(data), users=users, posts=posts)

@app.route("/like/<int:post_id>")
def like_post(post_id):
    data = {
        "user_id": session["user_id"],
        "post_id" : post_id
    }

    like_in_db = Like.get_likes_by_id(data)
    if not like_in_db:
        Post.like(data)
    else:
        Post.destroy_like(data)
    return redirect("/announcements")

@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    data = {
        "user_id": session["user_id"],
        "post_id" : post_id
    }
    Post.destroy(data)
    return redirect("/announcements")


@app.route('/add/post', methods=['POST'])
def add_post():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'content': request.form['content'],
        "user_id": session["user_id"]
    }

    Post.create_post(data)
    return redirect ('/announcements')


# html edit page for posting
@app.route('/post/edit/<int:id>')
def edit_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data ={
        'id': session['user_id']
    }

    return render_template('edit_post.html', user=User.get_one(user_data), post=Post.get_one(data))

# process edit form
@app.route('/edit/post', methods=['POST'])
def update_post():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'content': request.form['content'],
        'id': request.form['id']
    }
    if not Post.validate_show(request.form):
        return redirect('/announcements')
    Post.update(data)
    return redirect ('/announcements')

@app.route('/destroy/post/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    Post.destroy(data)
    return redirect('/announcements')
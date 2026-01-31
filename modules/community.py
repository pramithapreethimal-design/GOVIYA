import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from extensions import mysql
from flask_login import login_required, current_user

community_bp = Blueprint('community', __name__)

# --- 1. LIST ALL POSTS (The Feed) ---
@community_bp.route('/community')
@login_required
def feed():
    cur = mysql.connection.cursor()
    # We join with 'farmers' table to get the name of the person who posted
    cur.execute("""
        SELECT posts.id, posts.title, posts.content, farmers.name, posts.created_at 
        FROM posts 
        JOIN farmers ON posts.user_id = farmers.id 
        ORDER BY posts.created_at DESC
    """)
    posts = cur.fetchall()
    cur.close()
    return render_template('community/feed.html', posts=posts)

# --- 2. CREATE A NEW POST ---
@community_bp.route('/community/new', methods=['GET', 'POST'])
@login_required
def new_post():
    # If we came from the Solution page, pre-fill the title/content
    pre_title = request.args.get('title', '')
    pre_content = request.args.get('content', '')

    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        user_id = current_user.id
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO posts (user_id, title, content) VALUES (%s, %s, %s)", (user_id, title, content))
        mysql.connection.commit()
        cur.close()
        
        flash("Post created successfully!", "success")
        return redirect(url_for('community.feed'))

    return render_template('community/new_post.html', title=pre_title, content=pre_content)

# --- 3. VIEW POST & ADD COMMENTS ---
@community_bp.route('/community/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def view_post(post_id):
    cur = mysql.connection.cursor()

    # Handle New Comment
    if request.method == "POST":
        comment_content = request.form['comment']
        cur.execute("INSERT INTO comments (post_id, user_id, content) VALUES (%s, %s, %s)", 
                    (post_id, current_user.id, comment_content))
        mysql.connection.commit()
        flash("Comment added!", "success")

    # Get Post Details
    cur.execute("""
        SELECT posts.id, posts.title, posts.content, farmers.name, posts.created_at 
        FROM posts JOIN farmers ON posts.user_id = farmers.id 
        WHERE posts.id = %s
    """, [post_id])
    post = cur.fetchone()

    # Get All Comments for this Post
    cur.execute("""
        SELECT comments.content, farmers.name, comments.created_at 
        FROM comments 
        JOIN farmers ON comments.user_id = farmers.id 
        WHERE comments.post_id = %s 
        ORDER BY comments.created_at ASC
    """, [post_id])
    comments = cur.fetchall()
    cur.close()

    return render_template('community/view_post.html', post=post, comments=comments)
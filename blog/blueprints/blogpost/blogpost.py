from flask import Blueprint, jsonify, request, session
from datetime import datetime

blog_post = Blueprint("blog_post", __name__)

### ! should be logged in, there should be no need to put in username
## get all posts by me  --- ME
@blog_post.route('/get', methods = ['GET'])
def get_posts_all():
    if "user_det" in session:
        user_det = session['user_det']
        username = user_det['u_username']
        from db_run import db, db_connection
        conn = db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM BlogPost WHERE username_post = %s', (username,))
        blogs = cur.fetchall()
        conn.close()
        if blogs:
            return jsonify(blogs), 200
        else:
            return jsonify({'error': 'Could not fetch BlogPosts'}), 404
    

## get a particular post using title but MY post -- Me, should pass username
@blog_post.route('/get/login/<string:title>', methods = ['GET'])
def get_post_l(title):
    if "user_det" in session:
        user_det = session['user_det']
        username = user_det['u_username']
        from db_run import db, db_connection
        conn = db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM BlogPost WHERE user_id = %s AND Post_Title = %s', (username, title))
        blog = cur.fetchone()
        conn.close()
        if blog:
            return jsonify(blog), 200
        else:
            return jsonify({'error': 'Could not fetch BlogPost'}), 404



### ! no need to login 
## get a particular post (using title) --- ANYONE, doesnot pass in username
@blog_post.route('/get/<string:title>', methods = ['GET'])
def get_post_o(title):
    from db_run import db, db_connection
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM BlogPost WHERE Post_Title = %s', (title,))
    blog = cur.fetchall()
    conn.close()
    if blog:
        return jsonify(blog), 200
    else:
        return jsonify({'error': 'Could not fetch BlogPost'}), 404


## ! needs to be logged in
## create a new post
@blog_post.route('/post', methods = ['POST'])
def create_post():
    if "user_det" in session:
        user_det = session['user_det']
        name = user_det['u_name']
        username = user_det['u_username'] # username_post

        from db_run import db, db_connection
        conn = db_connection()
        cur = conn.cursor()
        data = request.get_json()

        title = data.get('Post_Title')
        content = data.get('Post_Content')
        cur.execute(
            '''INSERT INTO BlogPost (username_post, Post_Title, Post_Content, Post_Author, Post_Time_created, Post_Time_updated)
            VALUES (%s, %s, %s, %s, %s, %s)''',
            (username, title, content, name, datetime.now(), datetime.now())
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Post Created Successfully'}), 200
    else:
        return jsonify({'message': 'Unauthorized access. Please log in.'}), 401


## ! needs to be logged in 
##update a post
@blog_post.route('/put/<string:title>', methods = ['PUT'])
def update_post(title):
    if "user_det" in session:
        user_det = session['user_det']
        username = user_det['u_username']
        from db_run import db, db_connection
        conn = db_connection()
        cur = conn.cursor()
        data = request.get_json()

        cur.execute('SELECT b_id FROM BlogPost WHERE Post_Title = %s AND username_post = %s', (title, username))
        if cur.fetchone() is None:
            return jsonify({'message': 'Post not found'}), 404
        
        cur.execute('''
        UPDATE BlogPost 
        SET Post_Title = %s, 
            Post_Content = %s,
            Post_Time_updated = %s
        WHERE Post_Title = %s AND username_post = %s
        ''', (data['Post_Title'], data['Post_Content'], datetime.now(), title, username))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message' : 'Post Updated Successfully'})
    else:
        return jsonify({'message': 'Unauthorized, Please Login or Signup'}), 401


## ! needs to be logged in
## delete a post -- ME
@blog_post.route('/delete/<string:title>', methods = ['DELETE'])
def delete_post(title):
    if "user_det" in session:
        user_det = session['user_det']
        username = user_det['u_username']
        from db_run import db, db_connection
        conn = db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM BlogPost WHERE Post_Title = %s AND username_post = %s', (title, username))
        conn.commit()
        cur.close()
        conn.close()
        if cur.rowcount > 0:
            return jsonify({'message': 'Post deleted succcessfully'}), 200
        else:
            return jsonify({'message': 'Post not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized, Please Login or Signup'}), 401
    
    
from flask import Blueprint, jsonify, request, session
from datetime import datetime

comments = Blueprint("comments", __name__)

### ! should be logged in, there should be no need to put in username, shoould search from only users posts
## get all comments on my post by giving title --- ME, but post title might not be unique, thats why username
@comments.route('/get/login/<string:title>', methods = ['GET'])
def get_comments(title):
    from db_run import db, db_connection
    conn = db_connection()
    cur = conn.cursor()
    if "user_det" in session:
        user_det = session['user_det']
        username = user_det['u_username']
        cur.execute('SELECT * FROM Comments  WHERE username_post = %s AND Post_title = %s', (username, title,))
    else:
        cur.execute('SELECT * FROM Comments WHERE Post_Title = %s', (title,))
    comments = cur.fetchall()
    conn.close()
    if comments:
        return jsonify(comments), 200
    else:
        return jsonify({'error': 'Could not fetch Comments'}), 404



### ! no need to login 
## get comments for a particular post (using title) --- ANYONE, doesnot pass in username
@comments.route('/get/<string:title>', methods = ['GET'])
def get_comments_one(title):
    from db_run import db, db_connection
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Comments WHERE post_title = %s', (title,))
    comments = cur.fetchall()
    conn.close()
    if comments:
        return jsonify({'comments': comments}), 200
    else:
        return jsonify({'error': 'Could not fetch Comments'}), 404

## ! needs to be logged in, c_id, Post_title, c_Author, Post_Time should come on its own
## create a new post
@comments.route('/post/<string:title>', methods = ['POST'])
def create_comment(title):
    if "user_det" in session:
        user_det = session['user_det']
        username = user_det['u_username'] # username_id
        name = user_det['u_name']
        from db_run import db, db_connection
        conn = db_connection()
        cur = conn.cursor()
        data = request.get_json()

        content = data.get('c_Content')
        cur.execute(
            '''INSERT INTO Comments (Post_title, username_post, c_Content, c_Author, c_Time_created, c_Time_updated)
            VALUES (%s, %s, %s, %s, %s, %s)''',
            (title, username, content, name, datetime.now(), datetime.now())
        )

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Comment Created Successfully'}), 200


## ! needs to be logged in , username passed in, timestamp should be passed on its own
##update a post
@comments.route('/put/<string:title>', methods = ['PUT'])
def update_comm(title):
    if "user_det" in session:
        user_det = session['user_det']
        username = user_det['u_username']
        from db_run import db, db_connection
        conn = db_connection()
        cur = conn.cursor()
        data = request.get_json()

        cur.execute('''
        UPDATE Comments
        SET c_Content = %s, 
            c_Time_updated = %s
        WHERE Post_title = %s AND username_post = %s
        ''', (data['c_Content'], datetime.now(), title, username))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message' : 'Comment Updated Successfully'})
    else:
        return jsonify({'message': 'Unauthorized access'}), 401

######
## ! needs to be logged in, username passed in on its own, after title it should pass username of comment author
## delete a comment on a particular post -- ME
@comments.route('/delete/<string:title>', methods = ['DELETE'])
def delete_comm(title):
    if "user_det" in session:
        user_det = session['user_det']
        username = user_det['u_username']
        from db_run import db, db_connection
        conn = db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM Comments WHERE Post_title = %s AND username_post = %s', (title, username))
        conn.commit()
        cur.close()
        conn.close()
        if cur.rowcount > 0:
            return jsonify({'message': 'Comment deleted succcessfully'}), 200
        else:
            return jsonify({'message': 'Comment not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized access'}), 401
    
        
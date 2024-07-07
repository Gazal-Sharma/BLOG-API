from flask import Flask, Blueprint, request, jsonify, session
from flask_bcrypt import Bcrypt
user = Blueprint("user", __name__)


## get list of users (only by company itself) ???

## ! could be logged in or not logged in
## enter as a user
### sign in (first time)

@user.route('/signin', methods = ['POST'])
def sign_in():
    from db_run import app, db, db_connection
    bcrypt = Bcrypt(app)
    conn = db_connection()
    cur = conn.cursor()
    data = request.get_json()

    cur.execute(
        ''' SELECT * FROM Users WHERE u_username = %s OR u_email = %s ''',
        (data['u_username'], data['u_email'])
        )
    user = cur.fetchone()
    if user:
        return jsonify({'message': 'User already exists, Please Login'}), 400
    

    hashed_password = bcrypt.generate_password_hash (data['u_password']).decode('utf-8')
    cur.execute(
        '''INSERT INTO Users (u_name, u_email, u_username, u_password) 
        VALUES (%s, %s, %s, %s)''',
        (data['u_name'], data['u_email'], data['u_username'], hashed_password)
        )
    conn.commit()
    user_id = cur.fetchone()[0]
    session['user_det'] = {
            'u_id': user_id,
            'u_name' : data['u_name'],
            'u_email': data['u_email'],
            'u_username': data['u_username']
        }
    cur.close()
    conn.close()
    return jsonify({'message': 'User registered successfully'}), 201

@user.route('/login', methods = ['POST'])
def login():
    from db_run import app, db, db_connection
    bcrypt = Bcrypt(app)
    conn = db_connection()
    cur = conn.cursor()
    data = request.get_json()
    cur.execute(
        '''SELECT u_id, u_name, u_email, u_username, u_password FROM Users WHERE u_email = %s OR u_username = %s''',
        (data['u_email'], data['u_username'])
    )
    user = cur.fetchone()
    if not user:
        return jsonify({'message': 'User does not exist. Please sign up.'}), 400

    password_table = user[4]
    if bcrypt.check_password_hash(password_table, data['u_password']):
        session['user_det'] = {
            'u_id': user[0],
            'u_name' : user[1],
            'u_email': user[2],
            'u_username': user[3]

        }
        cur.close()
        conn.close()
        return jsonify({'message': 'User logged in successfully'}), 200
    else:
        return jsonify({'message': 'Incorrect password'}), 401
    
    

   
    # ? cur.execute(
    #    '''SELECT u_email, u_username, u_password FROM Users'''
    # )
    # user = cur.fetchone()
    # if (user[0] != data['u_email'] or user[1] != data['u_username']):
    #     return jsonify({'message': 'user doesnot exist, Please sign in'})
    
    # if (user[0] == data['u_email'] and user[1] == data['u_username'] and user[2] == data['u_password']):
    #     return jsonify({'message': 'User logged in successfully'}), 201

@user.route('/getusers', methods=['GET'])
def get_all_users():
    from db_run import db, db_connection
    try:
        conn = db_connection()
        cur = conn.cursor()

        # Query all users
        cur.execute('SELECT u_id, u_name, u_email, u_username, u_password FROM Users')
        users = cur.fetchall()

        # Prepare response data
        user_list = []
        for user in users:
            user_data = {
                'u_id': user[0],
                'u_name': user[1],
                'u_email': user[2],
                'u_username': user[3],
                'u_password': user[4]
            }
            user_list.append(user_data)

        return jsonify({'users': user_list}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

    finally:
        cur.close()
        conn.close()

## logout
@user.route('/logout', methods = ['POST'])
def logout():
    if "user_det" in session:
        session.pop("user_det")
        return jsonify({'message': 'User has been logged out'}), 200
    else:
        return jsonify({'message': 'No user logged in'}), 400
    

## update user credentials, after login
@user.route('/update', methods = ['PUT'])
def update():
    if "user_det" in session:
        user_det = session['user_det']
        u_id = user_det['u_id']
        from db_run import app, db, db_connection
        bcrypt = Bcrypt(app)
        conn = db_connection()
        cur = conn.cursor()
        data = request.get_json()
        password = data.get('u_password')
        new_password = data.get('new_u_password')
        cur.execute(
            '''SELECT u_password FROM Users WHERE u_id = %s''', (u_id,)
            )
        stored_pass = cur.fetchone()
        if not stored_pass:
            return jsonify({'message': 'User not found'}), 404
        if bcrypt.check_password_hash(stored_pass[0], password):
                hash_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                cur.execute('''
                UPDATE Users
                SET u_name = %s, 
                    u_email = %s, 
                    u_username = %s, 
                    u_password = %s
                WHERE u_id = %s
                ''', (data['u_name'], data['u_email'], data['u_username'], hash_password, u_id)
            )
                conn.commit()
                if cur.rowcount > 0:
                    return jsonify({'message': 'User updated successfully'}), 200
                else:
                    return jsonify({'message': 'No changes made or user not found'}), 404
        else:
            return jsonify({'message': 'Incorrect password'}), 401
        
        cur.close()
        conn.close()
    else:
        return jsonify({'message': 'Unauthorized access'}), 401



## delete user credentials, have to be logged in for this
    ## require password for deleting
@user.route('/delete', methods=['DELETE'])
def delete():
    if "user_det" in session:
        user_det = session['user_det']
        u_id = user_det['u_id']
        from db_run import app, db, db_connection
        bcrypt = Bcrypt(app)
        conn = db_connection()
        cur = conn.cursor()
        data = request.get_json()
        password = data.get('u_password')

        cur.execute(
            '''SELECT u_password FROM Users WHERE u_id = %s''', (u_id,)
        )
        stored_pass = cur.fetchone()

        if stored_pass and bcrypt.check_password_hash(stored_pass[0], password):
            cur.execute('DELETE FROM Users WHERE u_id = %s', (u_id,))
            conn.commit()
            if cur.rowcount > 0:
                cur.close()
                conn.close()
                session.clear()  # Clear session after deletion
                return jsonify({'message': 'User deleted successfully'}), 200
            else:
                cur.close()
                conn.close()
                return jsonify({'message': 'User could not be deleted'}), 404
        else:
            cur.close()
            conn.close()
            return jsonify({'message': 'Incorrect password'}), 401
    else:
        return jsonify({'message': 'Unauthorized access'}), 401
# import unittest
# from flask import Flask, jsonify, session
# from flask_testing import TestCase
# from datetime import datetime
# import requests
# from main.blueprints.blogpost.blogpost import blog_post

# # Import your Flask app and necessary modules
# from main.db_run import app  # Adjust this import based on your app structure
# # app.register_blueprint(blog_post, url_prefix = '/blogp/1')
# class TestBlogPostEndpoints(TestCase):

#     def create_app(self):
#         app.config['TESTING'] = True
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database for testing
#         app.config['SECRET_KEY'] = 'test_secret_key'
#         return app

#     def setUp(self):
#         # Create tables or initialize the database as needed
#         # For SQLAlchemy, you might create tables or drop/create them in memory
#         from main.db_run import db  # Adjust import based on your app structure
#         db.create_all()

#     def tearDown(self):
#         # Clean up after each test, for example, remove data from the database
#         from main.db_run import db  # Adjust import based on your app structure
#         db.session.remove()
#         db.drop_all()
#     def test_create_post(self):
#         url = '/blogp/post'
#         headers = {'Content-Type': 'application/json'}
#         data = {
#             'Post_Title': 'New Post Title',
#             'Post_Content': 'Sample content for the new post',
#         }

#         response = self.client.post(url, json=data, headers=headers)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json['message'], 'Post Created Successfully')

#     def test_update_post(self):
#         # First, create a post
#         with self.client:
#             url = '/blogp/post'
#             headers = {'Content-Type': 'application/json'}
#             data = {
#                 'Post_Title': 'Original Title',
#                 'Post_Content': 'Original content',
#             }
#             self.client.post(url, json=data, headers=headers)

#         # Now, update the post
#         url = '/blogp/put/Original Title'
#         headers = {'Content-Type': 'application/json'}
#         data = {
#             'Post_Title': 'Updated Title',
#             'Post_Content': 'Updated content',
#         }

#         response = self.client.put(url, json=data, headers=headers)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json['message'], 'Post Updated Successfully')

# if __name__ == '__main__':
#     unittest.main()
    

import unittest
from flask import session
from flask_testing import TestCase
from main.db_run import app, db  # Adjust this import based on your app structure
from main.blueprints.blogpost.blogpost import blog_post
from main.blueprints.user_details.user import user

class TestUserEndpoints(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database for testing
        app.config['SECRET_KEY'] = 'test_secret_key'  # Needed for session handling
        # app.register_blueprint(blog_post, url_prefix='/blogp')
        # app.register_blueprint(user, url_prefix='/user')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_signin(self):
        url = '/user/signin'
        headers = {'Content-Type': 'application/json'}
        data = {
            'u_name': 'John Doe',
            'u_email': 'johndoe@example.com',
            'u_username': 'johndoe',
            'u_password': 'password123'
        }

        response = self.client.post(url, json=data, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['message'], 'User registered successfully')
        with self.client.session_transaction() as sess:
            self.assertIn('user_det', sess)

    def test_login(self):
        # First, sign up the user
        with self.client:
            url = '/user/signin'
            headers = {'Content-Type': 'application/json'}
            data = {
                'u_name': 'John Doe',
                'u_email': 'johndoe@example.com',
                'u_username': 'johndoe',
                'u_password': 'password123'
            }
            self.client.post(url, json=data, headers=headers)

        # Now, login the user
        url = '/user/login'
        headers = {'Content-Type': 'application/json'}
        data = {
            'u_email': 'johndoe@example.com',
            'u_username': 'johndoe',
            'u_password': 'password123'
        }

        response = self.client.post(url, json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User logged in successfully')
        with self.client.session_transaction() as sess:
            self.assertIn('user_det', sess)

if __name__ == '__main__':
    unittest.main()


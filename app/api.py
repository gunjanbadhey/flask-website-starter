from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

@api.route('/api/products', methods=['GET'])
def get_products():
    products = [
        {"id": 1, "name": "Product A", "price": 50},
        {"id": 2, "name": "Product B", "price": 75}
    ]
    return jsonify({"success": True, "data": products})

@api.route('/api/blog', methods=['GET'])
def get_blog_posts():
    posts = [
        {"title": "Post 1", "content": "Content of Post 1", "author": "Author 1"},
        {"title": "Post 2", "content": "Content of Post 2", "author": "Author 2"}
    ]
    return jsonify({"success": True, "data": posts})

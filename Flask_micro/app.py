from flask import Flask, jsonify, request 
from flask_sqlaclchemy import SQLAlchemy 
from flask_jwt_extended import JWTManager, jwt_required, create_account_token
from flask_limiter import Limiter
from flask_caching import Cache 
import sentry_sdk 
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_restplus import Api, Resource
from flask_talisman import Talisman


app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://user:passwordlocalhost:5432/mydatabase'
app.config['JWT_SECRET_KEY']= 'super-secret'
jwt=JWTManager(app)
db=SQLAlchemy(app)
limiter=Limiter(app, key_func=get_remote_address)
cache=Cache(app, config={'CACHE_TYPE': 'simple'})
api=Api(app, version='1.0', title='My Api', description='A simple flask Api')
talisman=Talisman(app)


sentry_sdk.init(
    dsn="fillmeIn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)



@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Error occured: {str(e)}")
    return jsonify(error=str(e)), 500




class Book(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(80), Nullable=False)
    author=db.Column(db.String(120), nullable=False)
    
    
    
@api.router('/api/v1/books')    
class BookList(Resource):
    def get(self):
        return {"books": books}
api.init_app(app)

    
@app.route('/api/books', methods=['GET'])
@limiter.limit("10 per minute")
@cache.cached(timeout=60)
def get_books():
    return jsonify({"books": books}), 200


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book():
    return jsonify({"books": books}), 200


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book=next((book for book in books if book["id"] ==book_id), None)
    if book is None:
        return jsonify({"error": "book not found"}), 404
    return jsonify(book), 200


@app.route('/api/books', methods=['POST'])
def create_book():
    new_book=request.get_json()
    new_book['id']=len(books) +1
    books.append(new_book)
    return jsonify(new_book), 201

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book=next((book for book in book if book['id'] ==book_id),None)
    if book is None:
        return jsonify({"error": "book not found"}), 404
    
    data=request.get_json()
    book.update(data)
    return jsonify(book), 200


@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books=[book for book in books if book['id'] != book_id]
    return jsonify({"message": "book deleted"}), 200

@app.route('/login', methods=['POST'])
def login():
    username=request.json.get(''username)
    password=request.json.get('password')

    access_token=create_account_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/api/books', methods=['POST'])
@jwt_required
def create_book():
    new_book=request.get_json()
    return jsonify(new_book), 201
if __name__ == '__name__':
    app/run(host='0.0.0.0', port=5000)


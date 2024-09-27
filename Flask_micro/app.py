from flask import Flask, jsonify, request 


app= Flask(__name__)


books=[
    {"id": 1, "title": "book one", "author": "author one"},
    {"id": 2, "title": "book two", "author": "author two"}
]

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book():
    return jsonify({"books": books}), 200


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book=next((book for book in books if book["id"] ==book_id), None)
    if book is None:
        return jsonify({"error": "book not found"}), 404
    return jsonify(book), 200


@app..route('/api/books', methods=['POST'])
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

if __name__ == '__name__':
    app/run(host='0.0.0.0', port=5000)


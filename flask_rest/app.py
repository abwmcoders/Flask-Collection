from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('books.sqlite')
        print("Successfully connect")
    except sqlite3.Error as e:
        print(f"Error in connection")
        print(e) 
    return conn       


books_list = [
    {
        'id': 0,
        'author': "Chinua Achebe",
        'language': 'English',
        'title': 'Things fall apart',
    },
    {
        'id': 1,
        'author': "Hans Christain Anderson",
        'language': 'Danish',
        'title': 'Fairy Tales',
    },
    {
        'id': 2,
        'author': "Bob Job",
        'language': 'French',
        'title': 'Apache',
    },
    {
        'id': 3,
        'author': "Chinua Achebe",
        'language': 'English',
        'title': 'Things fall in',
    },
    {
        'id': 4,
        'author': "John Ranbo",
        'language': 'English',
        'title': 'First Blood',
    },
    {
        'id': 5,
        'author': "Jet li",
        'language': 'Chinese',
        'title': 'Twins Warrior',
    },
    {
        'id': 6,
        'author': "Jackie Chan",
        'language': 'Japanese',
        'title': 'Police Story',
    },
    
]

@app.route('/')
def root():
    return "Hello world"

# @app.route('/<name>')
# def talk_name(name):
#     return "Hi, {}".format(name)

@app.route('/books', methods=['GET','POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM  books")
        books = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]

        if books is not None:
            return jsonify(books)
        else:
            return "No Books at the moment"
        # if len(books_list) > 0:
        #     return jsonify(books_list)
        # else:
        #     "Nothing Found", 404

    if request.method == 'POST':
        new_author = request.form["author"]
        new_lang = request.form['language']
        new_title = request.form['title']
        # iD = books_list[-1]['id']+1

        sql = """INSERT INTO book (author, language, title) VALUES (?, ?, ?)"""
        cursor = conn.execute(sql, (new_author, new_lang, new_title))
        conn.commit()
        return f"Book with id: {cursor.lastrowid} created successfully", 201

        # new_obj = {
        #     'id': iD,
        #     'author': new_author,
        #     'language': new_lang,
        #     'title': new_title,
        # }      

        # books_list.append(new_obj)

@app.route('/book/<int:id>', methods= ['GET', 'PUT', 'DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM book WHERE id=?", (id))
        rows = cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book), 200
        else:
            return "Something went wrong", 404    
        # for book in books_list:
        #     if book['id'] == id:
        #         return jsonify(book),200
        #     pass

    if request.method == 'PUT':
        sql = """UPDATE book SET title=?, author=?, language=? WHERE id = ?"""

        author = request.form['author']
        title =  request.form['title']
        language = request.form['language']
        updated_book = {
                'id': id,
                'author': author,
                'language': language,
                'title': title,
               }  
        conn.execute(sql, (author, language, title, id))
        conn.commit()
        return jsonify(updated_book)

        # for book in books_list:
        #     if book['id'] == id:
        #         book["author"] = request.form['author']
        #         book['title'] =  request.form['title']
        #         book['language'] = request.form['language']
        #         updated_book = {
        #         'id': id,
        #         'author': book["author"],
        #         'language': book['language'],
        #         'title': book['title'],
        #        }    
        #         return jsonify(updated_book)
    if request.method ==  'DELETE':
        sql = """DELETE FROM book WHERE id=?"""
        conn.execute(sql, (id))
        conn.commit()
        return "The book with id: {} has been deleted.".format(id), 200

        for index, book in books_list:
            if book['id'] == id:
                books_list.pop(index) 
                return jsonify(books_list)       





if __name__ == "__main__":
    app.run(debug=True)

# w ----> WEB
# s ----> SERVER
# g ----> GATEWAY
# i ----> INTERFACE
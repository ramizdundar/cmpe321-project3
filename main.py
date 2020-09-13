import mysql.connector
from datetime import datetime
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# create table books (isbn INT PRIMARY KEY, title VARCHAR(255), author VARCHAR(255), borrowed BOOLEAN);
# create table borrows (tc INT, isbn INT, date VARCHAR(255));

repopulate = 1
debug = 1

mydb = mysql.connector.connect(
    host="localhost",
    user="ramiz",
    password="1234",
    database="cmpe321"
)

# mycursor = mydb.cursor()

# sql = "CREATE TRIGGER tr_borrow BEFORE INSERT ON borrows FOR EACH ROW UPDATE books SET borrowed = 1 WHERE isbn = NEW.isbn"

# mycursor.execute(sql)


def insert(isbn, title, author):
    mycursor = mydb.cursor()

    borrowed = 0

    sql = "INSERT INTO books (isbn, title, author, borrowed) VALUES (%s, %s, %s, %s)"
    val = (isbn, title, author, borrowed)
    mycursor.execute(sql, val)

    mydb.commit()

    print("Added book:", val)
    return val


def delete(isbn):
    mycursor = mydb.cursor()

    sql = "DELETE FROM books WHERE isbn = %s"
    val = (isbn, )

    mycursor.execute(sql, val)

    print("Deleted book:", val)

    mydb.commit()

    return val


def flush():
    mycursor = mydb.cursor()

    sql = "DELETE FROM books"

    mycursor.execute(sql)

    sql = "DELETE FROM borrows"

    mycursor.execute(sql)

    mydb.commit()

    print("Flushed books and borrows")


def search(value, field):
    mycursor = mydb.cursor()

    sql = f"SELECT * FROM books WHERE {field} = %s"
    val = (value, )

    mycursor.execute(sql, val)

    myresult = mycursor.fetchall()

    return myresult


def search_person(tc):
    
    mycursor = mydb.cursor()

    sql = "SELECT * FROM borrows WHERE tc = %s"
    val = (tc, )

    mycursor.execute(sql, val)

    myresult = mycursor.fetchall()

    return myresult   


def borrow(tc, isbn):
    book = search(isbn, "isbn")

    if len(book) == 0:
        print("Book not found")
        return "Book not found"

    if book[0][3] == 1:
        print("Book is not available")
        return "Book is not available"

    person = search_person(tc)

    if len(person) == 8:
        print("You can't borrow more than 8 books")
        return "You can't borrow more than 8 books"

    mycursor = mydb.cursor()
    # Added this part to trigger
    # sql = "UPDATE books SET borrowed = %s WHERE isbn = %s"
    # val = (1, isbn)

    # mycursor.execute(sql, val)

    sql = "INSERT INTO borrows (tc, isbn, date) VALUES (%s, %s, %s)"
    val = (tc, isbn, (datetime.now()+timedelta(days=14)).strftime("%d-%m-%Y"))
    mycursor.execute(sql, val)

    mydb.commit()

    print(f"TC: {tc} borrowed ISBN: {isbn}")
    return f"TC: {tc} borrowed ISBN: {isbn}"


if repopulate == 1:
    flush()
    for i in range(1000, 2000):
        insert(i, f"book{i}", f"ramiz{i%10}")

    for i in range(1003, 2000, 5):
        delete(i)

    for i in range(1002, 2100, 5):
        borrow(i*1000,i)

    for i in range(1002, 1102, 5):
        borrow(i*10,i)


if debug == 1:
    # print(search("ramiz2", "author"))

    print(search_person(1812000))

    for i in range(1000, 1100, 5):
        borrow(1812000,i)

    print(search_person(1812000))


@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        action = request.form['action']

        if action == 'insert':
            return redirect(url_for('insertflask'))

        if action == 'delete':
            return redirect(url_for('deleteflask'))

        if action == 'search':
            return redirect(url_for('searchflask'))

        if action == 'borrow':
            return redirect(url_for('borrowflask'))

        if action == 'search_person':
            return redirect(url_for('search_personflask'))
    
    return render_template('home.html')


@app.route('/insert', methods=['POST','GET'])
def insertflask():
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        author = request.form['author']
        book = insert(isbn, title, author)
        return render_template('message.html', message=f'Book {book} added.')

    return render_template('insert.html')


@app.route('/delete', methods=['POST','GET'])
def deleteflask():
    if request.method == 'POST':
        isbn = request.form['isbn']
        book = delete(isbn)
        return render_template('message.html', message=f'Book {book} deleted.')

    return render_template('delete.html')


@app.route('/search', methods=['POST','GET'])
def searchflask():
    if request.method == 'POST':
        field = request.form['field']
        value = request.form[field]
        books = search(value, field)
        message = ''

        for book in books:
            message += str(book) + '\n'

        return render_template('message.html', message=message)

    return render_template('search.html')


@app.route('/borrow', methods=['POST','GET'])
def borrowflask():
    if request.method == 'POST':
        tc = request.form['tc']
        isbn = request.form['isbn']
        message = borrow(tc, isbn)
        return render_template('message.html', message=message)

    return render_template('borrow.html')


@app.route('/search_person', methods=['POST','GET'])
def search_personflask():
    if request.method == 'POST':
        tc = request.form['tc']
        books = search_person(tc)
        message = ''

        for book in books:
            message += str(book) + '\n'

        return render_template('message.html', message=message)

    return render_template('search_person.html')


if __name__ == '__main__':
    app.run(debug=True)

import mysql.connector
from datetime import datetime
from datetime import timedelta

# create table books (isbn INT PRIMARY KEY, title VARCHAR(255), author VARCHAR(255), borrowed BOOLEAN);
# create table borrows (tc INT, isbn INT, date VARCHAR(255));

repopulate = 0
debug = 0

mydb = mysql.connector.connect(
    host="localhost",
    user="ramiz",
    password="1234",
    database="cmpe321"
)

def insert(isbn, title, author):
    mycursor = mydb.cursor()

    borrowed = 0

    sql = "INSERT INTO books (isbn, title, author, borrowed) VALUES (%s, %s, %s, %s)"
    val = (isbn, title, author, borrowed)
    mycursor.execute(sql, val)

    mydb.commit()

    print("Added book:", val)
    return


def delete(isbn):
    mycursor = mydb.cursor()

    sql = "DELETE FROM books WHERE isbn = %s"
    val = (isbn, )

    mycursor.execute(sql, val)

    print("Deleted book:", val)

    mydb.commit()


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


# incomplete needs 8 book limit
def borrow(tc, isbn):
    book = search(isbn, "isbn")

    if len(book) == 0:
        print("Book not found")
        return False

    if book[0][3] == 1:
        print("Book is not available")
        return False

    person = search_person(tc)

    if len(person) == 8:
        print("You can't borrow more than 8 books")
        return False

    mycursor = mydb.cursor()

    sql = "UPDATE books SET borrowed = %s WHERE isbn = %s"
    val = (1, isbn)

    mycursor.execute(sql, val)

    sql = "INSERT INTO borrows (tc, isbn, date) VALUES (%s, %s, %s)"
    val = (tc, isbn, (datetime.now()+timedelta(days=14)).strftime("%d-%m-%Y"))
    mycursor.execute(sql, val)

    mydb.commit()

    print(f"TC: {tc} borrowed ISBN: {isbn}")
    return True



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






print("====END====")
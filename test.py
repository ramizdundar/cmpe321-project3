import mysql.connector

# create table books (isbn INT PRIMARY KEY, title VARCHAR(255), author VARCHAR(255), borrowed BOOLEAN);
# create table borrows (tc INT PRIMARY KEY, isbn INT, date INT);

repopulate = 0

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

    print("Flushed books")

    mydb.commit()


if repopulate == 1:
    flush()
    for i in range(1000, 2000):
        insert(i, f"book{i}", f"ramiz{i%10}")

    for i in range(1003, 2000, 5):
        delete(i)






print("====END====")
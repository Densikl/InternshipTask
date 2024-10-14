import sqlite3
import time

dbName = 'finance.db'

# connecting to the database
def connectToDatabase():
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()

    return connection, cursor


def addData(userId, category, amount, date, description=''):
    # setting up connection here, although its ineffective, 
    # because this func works in another thread
    connection, cursor = connectToDatabase()
    cursor.execute('INSERT INTO finance (userId, category, amount, description, date) VALUES (?, ?, ?, ?, ?)', 
                   (userId, category, amount, description, date))
    connection.commit()
    connection.close()


def deleteData(id):
    # setting up connection here, although its ineffective, 
    # because this func works in another thread
    connection, cursor = connectToDatabase()
    cursor.execute('DELETE FROM finance WHERE id = (?)', (id,))
    connection.commit()
    connection.close()


def getAmountData(userId):
    # setting up connection here, although its ineffective, 
    # because this func works in another thread
    connection, cursor = connectToDatabase()
    result = [row[0] for row in cursor.execute('SELECT amount FROM finance WHERE userId = (?)', (userId,))]
    connection.close()

    return result


def getDataInInterval(userId, interval):
    # setting up connection here, although its ineffective, 
    # because this func works in another thread
    connection, cursor = connectToDatabase()
    currentTime = int(time.time())
    data = cursor.execute('SELECT * FROM finance WHERE userId = (?) AND date BETWEEN (?) AND (?)', 
                        (userId, currentTime - interval, currentTime))
    result = [row for row in data]
    connection.close()

    return result


def addCategory(userId, name):
    # setting up connection here, although its ineffective, 
    # because this func works in another thread
    connection, cursor = connectToDatabase()
    cursor.execute(f'INSERT INTO categories (userId, name) VALUES (?, ?)', (userId, name))
    connection.commit()
    connection.close()


def deleteCategory(cursor, id):
    # setting up connection here, although its ineffective, 
    # because this func works in another thread
    connection, cursor = connectToDatabase()
    cursor.execute('DELETE FROM categories WHERE id = (?)', (id,))
    connection.commit()
    connection.close()


def getCategories(userId):
    # setting up connection here, although its ineffective, 
    # because this func works in another thread
    connection, cursor = connectToDatabase()
    result = [row for row in cursor.execute(f'SELECT * FROM categories WHERE userId = (?)', (userId,))]
    connection.close()

    return result

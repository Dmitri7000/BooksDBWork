import sqlite3
#Попытка создания приложения "УчетКниг" в консоли с использованием БД
#Это моя первая самостоятельная работа с СУБД, использовал ИИ как помощника синтаксиса и для того, чтобы узнать как создавать авторов без дублей
#Работа не закончена!!!
class Bookwork:
    def __init__(self):
        pass
    def condb(self):
        with sqlite3.connect("Books.db") as con:
            con.execute("PRAGMA foreign_keys = ON;")
            return con
    def creattabauth(self):
            with self.condb() as con:
                 cursor = con.cursor()
                 cursor.execute("""
                                CREATE TABLE IF NOT EXISTS Authors (
                                id INTEGER PRIMARY KEY, 
                                FIO_Author TEXT UNIQUE
                                )""")
                 con.commit()
    def creattabbook(self):
            with self.condb() as con:
                cursor = con.cursor()
                cursor.execute("""
                                CREATE TABLE IF NOT EXISTS Books (
                                id INTEGER PRIMARY KEY,
                                Name TEXT,
                                Author TEXT REFERENCES Authors (id),
                                Date TEXT)""")
                con.commit()
    def insauth(self, FIO_Author):
         with self.condb() as con:
              cursor = con.cursor()
              cursor.execute("""INSERT INTO Authors (FIO_Author) SELECT ? WHERE NOT EXISTS
              (SELECT 1 FROM Authors WHERE FIO_Author = ?)""", (FIO_Author, FIO_Author))
              con.commit()
              cursor.execute("SELECT id FROM Authors WHERE FIO_Author = ?", (FIO_Author, ))
              row = cursor.fetchone()
              if row:
                   return row[0]
              return None
    def haveauthor(self, FIO_Author): #Проверка на наличие автора и его добавление в случае отсутствия
         with self.condb() as con:
              cursor = con.cursor()
              cursor.execute("SELECT id FROM Authors WHERE FIO_Author = ?", (FIO_Author, ))
              row = cursor.fetchone()
              if row:
                   return row[0]
              cursor.execute("INSERT INTO Authors (FIO_Author) Values (?)", (FIO_Author, ))
              con.commit()
              return cursor.lastrowid
    def insbook(self, name, author, date):
         author_id = self.haveauthor(author)
         with self.condb() as con:
              cursor = con.cursor()
              cursor.execute("INSERT INTO Books (Name, Author, Date) Values (?, ?, ?)", (name, author_id, date))
              con.commit()
    def delauth(self, idauth):
         with self.condb() as con:
              cursor = con.cursor()
              cursor.execute("DELETE FROM Authors WHERE id = ?", (idauth, ))
              con.commit()
    def delbook(self, idbook):
         with self.condb() as con:
            cursor = con.cursor()
            cursor.execute("DELETE FROM Books WHERE id = ?", (idbook, ))
            con.commit()
    def getauthors(self):
         with self.condb() as con:
              cursor = con.cursor()
              cursor.execute("SELECT * FROM Authors")
              rows = cursor.fetchall()
              return rows
    def getbooks(self):
         with self.condb() as con:
              cursor = con.cursor()
              cursor.execute("SELECT * FROM Books")
              rows = cursor.fetchall()
              return rows
#Работа не закончена!!!
bookking = Bookwork()
bookking.creattabauth()
bookking.creattabbook()
bookking.insauth("А. С. Пушкин")
"""bookking.insbook('Капитанская дочка', "А. С. Пушкин", '01.08.1828')
bookking.insbook('Кортик', 'А. Рыбаков', '18.03.1935')"""
print(bookking.getbooks()) #-Выводит все, даже что вы добавили в базу своими руками, но это и не удивительно
#Работа не закончена!!!
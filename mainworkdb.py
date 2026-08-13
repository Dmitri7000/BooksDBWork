import sqlite3
#Попытка создания приложения "УчетКниг" в консоли с использованием БД

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
    def workinconsole(self):
         print('Старт работы!')
         while True:
              print('Для вывода данных введите 1, для ввода 2, для удаления 3, для выхода из работы 4:')
              choice = int(input())
              if choice == 1:
                   print("Авторы произведений")
                   print(self.getauthors())
                   print("Произведения")
                   print(self.getbooks())
              if choice == 2:
                   a = int(input('Что вы хотите ввести? Автор - 1, книга - 2, введите число: '))
                   if a == 1:
                        Fio = input("Введите ФИО или псевдоним автора: ") 
                        self.insauth(Fio)
                   if a == 2:
                        nam = input("Введите название книги: ")
                        auth = input("Введите ФИО или псевдоним автора: ")
                        dat = input("Введите дату в формате 'дд.мм.гггг': ")
                        self.insbook(nam, auth, dat)  
              if choice == 3:
                    a = int(input('Что вы хотите удалить? Автор - 1, книга - 2, введите число: '))
                    if a == 1:
                         ida = int(input("Введите ID автора для удаления: "))
                         self.delauth(ida)
                    if a == 2:
                         idb = int(input("Введите ID книги для удаления: "))
                         self.delbook(idb)
              if choice == 4: 
                   print("Завершение работы")
                   break 
              if choice not in [1, 2, 3, 4]:
                   print("Вы ввели некорректное значение!")

bookking = Bookwork()
"""bookking.creattabauth()
bookking.creattabbook()
bookking.insauth("А. С. Пушкин")
bookking.insbook('Капитанская дочка', "А. С. Пушкин", '01.08.1828')
bookking.insbook('Кортик', 'А. Рыбаков', '18.03.1935')
print(bookking.getbooks()) #-Выводит все, даже что вы добавили в базу своими руками, но это и не удивительно"""
# Выше я проверил работоспособность каждой функции
bookking.workinconsole()
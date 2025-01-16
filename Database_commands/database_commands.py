
class BookRepository:
    def __init__(self, cursor): #Coz mi pripomina zopakuj si dedicnost
        self.cursor = cursor

    def get_book_id_by_title(self, title):
        self.cursor.execute("SELECT BooksId FROM Books WHERE Title = ?", (title,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def is_available(self, book_id):
        self.cursor.execute("SELECT AvalaibleCopies FROM Books WHERE BooksId = ?", (book_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def update_availability(self, book_id):
        self.cursor.execute("UPDATE Books SET AvalaibleCopies = AvalaibleCopies - 1 WHERE BooksId = ?", (book_id,))


    def general_book_overview(self):
        self.cursor.execute("SELECT b.Title AS BookTitle,a.Name AS AuthorName,b.GenreId AS Genre, b.PublishedDate AS PublicationDate,CASE WHEN b.IsAvailable = 1 THEN 'Available' ELSE 'Not available' END AS Availabilit FROM  Ownership o JOIN Books b ON o.BooksId = b.BooksId JOIN  Authors a ON o.AuthorsId = a.AuthId  ORDER BY b.Title; ")
        result = self.cursor.fetchall()
        return result

class BorrowerRepository:
    def __init__(self, cursor):
        self.cursor = cursor
    def get_borrower_id_by_username(self, username):
        self.cursor.execute("SELECT BorrowersId FROM Borrowers WHERE Username = ?", (username,))
        result = self.cursor.fetchone()
        return result[0] if result else None

class TransactionRepository:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert_transaction(self, book_id, borrower_id, date_of_creation, date_of_return, fine):
        self.cursor.execute("INSERT INTO Transactions(BooksId, BorrowersId,DateOfCreation,DateToReturn, Fine)VALUES(?,?,?,?,?)",(book_id,borrower_id,date_of_creation,date_of_return,fine))

    def genre_by_book_id(self, book_id):
        self.cursor.execute("SELECT * FROM Books where GenreId", (book_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None




CREATE DATABASE eta;

USE eta;

CREATE TABLE Authors(
AuthId INT PRIMARY KEY IDENTITY(1,1),
Name VARCHAR(30),
Surname VARCHAR(30),
BirthDate DATE,
Bio VARCHAR(300)
);

CREATE TABLE Books(
Title VARCHAR(30),
ISBN VARCHAR(13), 
PublishedDate DATE,
AvalaibleCopies INT,
Available Int check(Available>=0),
BooksId INT PRIMARY KEY IDENTITY(1,1),
GenreId INT FOREIGN KEY REFERENCES Genres(GenreId)
);



alter table Books 
add IsAvailable bit not null;
select*from Borrowers;
select*from Books;
CREATE TABLE Genres(
GenreId INT PRIMARY KEY, 
GenreName VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Borrowers(
Name VARCHAR(30),
Surname VARCHAR(30),
Registration DATE,
IsActive BIT,
BorrowersId INT PRIMARY KEY IDENTITY(1,1),
Email varchar(30) CHECK(Email LIKE '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
'),
Username varchar(40) check(Username like '^[a-zA-Z][0-9]')
)

CREATE TABLE Ownership(
DateOfCreation DATE DEFAULT GETDATE(),
AuthorsId INT FOREIGN KEY REFERENCES Authors(AuthId),
BooksId INT FOREIGN KEY REFERENCES Books(BooksId)
);

ALTER TABLE Ownership
ADD CONSTRAINT DF_Date
DEFAULT GETDATE() FOR DateofCreation;

CREATE TABLE Transactions(
DateOfCreation DATE,
Fine FLOAT(2),
DateToReturn DATE,
BooksId INT FOREIGN KEY REFERENCES Books(BooksId),
BorrowersId INT FOREIGN KEY REFERENCES Borrowers(BorrowersId)
);



CREATE TRIGGER trg_UpdateIsAvailable
ON Books
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE b
    SET IsAvailable = CASE 
                          WHEN i.AvalaibleCopies = 0 THEN 0
                          ELSE 1
                      END
    FROM Books b
    INNER JOIN inserted i ON b.BooksId = i.BooksId
    WHERE b.AvalaibleCopies <> i.AvalaibleCopies; -- Ensure we only update if there's a change
END;

SELECT 
    b.Title AS BookTitle,
    a.Name AS AuthorName,
    b.GenreId AS Genre,
    b.PublishedDate AS PublicationDate,
    CASE 
        WHEN b.IsAvailable = 1 THEN 'Dostupná'
        ELSE 'Nedostupná'
    END AS Availability
FROM 
    Ownership o
JOIN 
    Books b ON o.BooksId = b.BooksId
JOIN 
    Authors a ON o.AuthorsId = a.AuthId 
ORDER BY 
    b.Title;  -- You can order by any other column as needed


CREATE TRIGGER trg_SetUsername
ON Borrowers
INSTEAD OF INSERT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Borrowers (Name, Surname, Registration, IsActive, Username)
    SELECT 
        i.Name,
        i.Surname,
        i.Registration,  -- Ensure Registration is provided
        ISNULL(i.IsActive, 1),  -- Default to active if not specified
        CASE 
            WHEN i.Username IS NULL OR i.Username = '' THEN 
                -- Generate a username based on Name and Surname
                LEFT(i.Name, 3) + LEFT(i.Surname, 3) + CAST(NEWID() AS VARCHAR(36))  -- Adding uniqueness
            ELSE 
                i.Username 
        END
    FROM inserted i;
END;


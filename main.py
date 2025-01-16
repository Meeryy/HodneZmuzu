import os
import pyodbc
import pandas as pd
import configparser
from datetime import datetime, timedelta
from Database_commands.database_commands import BookRepository, BorrowerRepository, TransactionRepository
from Configuration.configuration import load_user_config, get_final_config, load_default_config

def connect_to_database(final_config):
    connection_string = (
        f"SERVER={final_config.get('server', '46.13.167.200,20500')};"
        f"DATABASE={final_config.get('database', 'eta')};"
        f"UID={final_config.get('username', 'ShelfSniffer')};"
        f"PWD={final_config.get('password', '123123')};"
        f"DRIVER={final_config.get('driver', '{ODBC Driver 17 for SQL Server}')};"
    )
    return pyodbc.connect(connection_string)

def borrow_book(cursor, book_repo, borrower_repo, transaction_repo):
    book_name = input("Enter the book name: ")
    book_id = book_repo.get_book_id_by_title(book_name)
    if book_id is None:
        print("Book not found.")
        return

def see_authors(cursor):
    cursor.execute("SELECT * FROM dbo.Authors")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def load_config():
    user_config = load_user_config()
    if user_config is None:
        return load_default_config()
    return user_config


def load_data_from_csv(cursor, csv_file_path, table_name):
    try:
        data = pd.read_csv(csv_file_path)

        # Check the columns and insert data accordingly
        if table_name == "authors":
            if 'Name' not in data.columns:
                raise ValueError("CSV file for authors should contain a 'Name' column.")
            for index, row in data.iterrows():
                cursor.execute("INSERT INTO Authors (Name) VALUES (?)", (row['Name'],))
            print("Data successfully loaded into Authors table.")

        elif table_name == "genres":
            if 'GenreName' not in data.columns:
                raise ValueError("CSV file for genres should contain a 'GenreName' column.")
            for index, row in data.iterrows():
                cursor.execute("INSERT INTO Genres (GenreName) VALUES (?)", (row['GenreName'],))
            print("Data successfully loaded into Genres table.")
        else:
            print("Invalid table name. Choose 'authors' or 'genres'.")

    except Exception as e:
        print(f"Error loading datas from CSV: {e}")
        return False  # Indicate failure
    return True  # Indicate success


def insert_data_manually(cursor, table_name):
    if table_name == "authors":
        name = input("Enter author name: ")
        cursor.execute("INSERT INTO Authors (Name) VALUES (?)", (name,))
        print("Author added successfully.")

    elif table_name == "genres":
        genre_name = input("Enter genre name: ")
        cursor.execute("INSERT INTO Genres (GenreName) VALUES (?)", (genre_name,))
        print("Genre added successfully.")
    else:
        print("Invalid choice. Please choose 'authors' or 'genres'.")


def load_data_into_table(cursor):
    config = load_config()
    csv_file_path = config.get('csv_file_path', None)

    if csv_file_path is None or not os.path.exists(csv_file_path):
        print("CSV file path is not set or the file doesn't exist. Please check the configuration.")
        return

    # Ask the user if they want to insert data manually or load from CSV
    choice = input("Would you like to (1) Manually insert data or (2) Load data from CSV? (1/2): ").strip()

    # If the user chooses to load from CSV
    if choice == '2':
        table_choice = input(
            "Which table would you like to load data into? \n1. Authors \n2. Genres \nPlease enter 1 or 2: ").strip()
        if table_choice == "1":
            if not load_data_from_csv(cursor, csv_file_path, "authors"):
                print("Error loading data into the Authors table.")
        elif table_choice == "2":
            if not load_data_from_csv(cursor, csv_file_path, "genres"):
                print("Error loading data into the Genres table.")
        else:
            print("Invalid choice. Please choose 1 for Authors or 2 for Genres.")
    # If the user chooses to insert data manually
    elif choice == '1':
        table_choice = input(
            "Which table would you like to insert data into? \n1. Authors \n2. Genres \nPlease enter 1 or 2: ").strip()
        if table_choice == "1":
            insert_data_manually(cursor, "authors")
        elif table_choice == "2":
            insert_data_manually(cursor, "genres")
        else:
            print("Invalid choice. Please choose 1 for Authors or 2 for Genres.")
    else:
        print("Invalid choice. Please enter '1' to manually insert or '2' to load from CSV.")


def main():
    default_config_obj = load_config()
    final_config = get_final_config(default_config_obj, default_config_obj)

    try:
        conn = connect_to_database(final_config)
        print("Connection successful, thanks for using my app.")

        cursor = conn.cursor()
        book_repo = BookRepository(cursor)
        borrower_repo = BorrowerRepository(cursor)
        transaction_repo = TransactionRepository(cursor)
        general_book_overview = BookRepository(cursor)

        choice = ''
        options = ["a", "b", "c", "d", "e", "f"]
        while choice != 'e':
            choice = input(
                "You can: \n See Current authors (a) \n Make borrowing transaction (b) \n View Overview (c) \n Load data (f) \n Exit (e): ")

            if choice == "a":
                see_authors(cursor)
            elif choice == "b":
                borrow_book(cursor, book_repo, borrower_repo, transaction_repo)
            elif choice == "c":
                gen_or_spec = input("General (g) or specific book (s)? Back (b): ").lower()
                while gen_or_spec != "b":
                    if gen_or_spec == "g":
                        try:
                            general_overview = general_book_overview.general_book_overview()
                            if general_overview is None or not general_overview:
                                print("There are no books to give overview on.")
                            else:
                                for book in general_overview:
                                    print(book)
                        except Exception as e:
                            print("Error during general book overview: ", e)
                    elif gen_or_spec == "s":
                        print("In progress")  # Placeholder for specific book overview
                    else:
                        print("Invalid option. Please select 'g', 's', or 'b'.")
                    gen_or_spec = input("General (g) or specific book (s)? Back (b): ").lower()
            elif choice == "f":
                load_data_into_table(cursor)
            else:
                print("Invalid option, try again.")

        cursor.close()
        exit()

    except Exception as e:
        print("Error: ", e)
    finally:
        if 'conn' in locals():
            conn.close()
            print("Connection closed")


if __name__ == "__main__":
    main()

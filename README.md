# Library Management System

## Project Overview

This project is a Library Management System built with Flask for the backend and SQLite for the database. The system allows users to manage books, reading history, and reading plans. It also provides features to search books by category and name. The frontend is developed using HTML, Bootstrap, and JavaScript.

## Database Schema

The database contains three tables:

1. **Book**
    - `id`: Integer, Primary Key
    - `ISBN`: Text, Not Null
    - `book_title`: Text, Not Null
    - `author`: Text, Not Null
    - `price`: Integer, Not Null
    - `category`: Text, Not Null
    - `edition`: Text, Not Null
    - `current_page`: Integer, Not Null

2. **ReadingHistory**
    - `id`: Integer, Primary Key
    - `time_stamp`: Text, Not Null
    - `book_id`: Integer, Foreign Key (references `Book(id)`), Not Null
    - `bookpage`: Integer, Not Null
    - `note`: Text, Not Null

3. **ReadingPlan**
    - `id`: Integer, Primary Key
    - `book_id`: Integer, Foreign Key (references `Book(id)`), Not Null
    - `expired_date`: Text, Not Null
    - `is_complete`: Integer, Not Null

## Backend Features

- **Check Book**: Check if a book with the same title already exists.
- **Add Book**: Add a new book to the library. If a book with the same title exists, the user will be prompted to confirm adding a duplicate.
- **Add Reading History**: Add a new reading history record.
- **Add or Update Reading Plan**: Add a new reading plan or update an existing one for a book.
- **Update Current Page**: Update the current page of a book.
- **Delete Data**: Delete records from the specified table (Book, ReadingHistory, or ReadingPlan).
- **Search by Category**: Search books by category.
- **Search by Name**: Search books by name.
- **View Data**: View data from the specified table.

## Running the Project

### Prerequisites

- Python 3.x
- Flask
- SQLite

### Setting Up the Project

1. **Clone the Repository**

   ```bash
   git clone https://github.com/ChenTim1011/DB-Final-Project.git
   cd <your-repository-name>
   
Install Dependencies

    pip install Flask

Create and Initialize the Database

Ensure that you have SQLite installed and then run the create_tables() function to create the necessary tables in the database. You can do this by running the Flask application which includes the create_tables() call.


    if __name__ == '__main__':
        create_tables()  # Create tables
        app.run(debug=True)
You can use SQL query to insert multiple Data

For example:

Use the provided insert.sql script to populate the database with initial data. Execute the script using SQLite command line tool or a database browser.
    
    sqlite3 library.db < insert.sql
    
Run the Flask Application

    python app.py
    
Using the Application

Open your browser and navigate to http://127.0.0.1:5000/.

Use the tabs to navigate through different functionalities:

Add Book: Add a new book to the library.

Add Reading History: Add a new reading history record.

Add Reading Plan: Add or update a reading plan.

Delete Data: Delete a record from the specified table.

Search by Category: Search books by category.

Search by Name: Search books by name.

View Data in the tables to see the records for books, reading history, and reading plans.

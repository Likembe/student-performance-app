# Student Performance Database Manager

This repository contains a Python application that manages student performance data using an SQLite database. It includes functionality for creating a database, inserting records, querying data, and printing formatted results.

## Features

- SQLite database connection and table creation
- Data insertion and conflict resolution with `INSERT OR REPLACE`
- Data querying and result fetching
- Average grade calculation and letter grade assignment
- Object-relational mapping (ORM) with SQLAlchemy for Pythonic database interaction
- Command-line interface for interacting with the database and printing results

## Prerequisites

- Python 3.6 or higher
- SQLite3
- SQLAlchemy

To install SQLAlchemy, run:

```bash
pip install sqlalchemy

## Usage
-Clone the repository
-navigate into the repo directory
-Initialize it and populate using sample data run

## To qury and print studnet performance you can use

# For all students
python main.py --all

# For a specific student
python main.py --student 'Alpha Likembe'


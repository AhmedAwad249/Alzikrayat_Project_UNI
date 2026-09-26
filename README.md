# Alzikrayat

A simple photo sharing website where members can post memories, tag people, like photos, and comment.

## Technologies

Python, Flask, MySQL, PyMySQL, HTML, CSS, JavaScript, and Bootstrap.

## How to run

1. Install Python 3 and MySQL, then create the database:

   ```bash
   mysql -u root -p -e "CREATE DATABASE alzikrayat;"
   mysql -u root -p alzikrayat < database/schema.sql
   ```

2. Install dependencies and set your database login:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   export DB_USER=root
   export DB_PASSWORD='your_mysql_password'
   export SECRET_KEY='change-this-to-a-random-value'
   ```

3. Start the app with `python run.py`, then open <http://localhost:3000>.

## Student name

Ahmad Awad


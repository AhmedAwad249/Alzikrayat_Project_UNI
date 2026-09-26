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

## Demo image credits

The following local demo images were resized for the gallery:

- `demo-nile-sunset.webp`: [Blue Nile sunset and El-Mak Nimr Bridge](https://commons.wikimedia.org/wiki/File:%D9%83%D8%A8%D8%B1%D9%8A_%D8%A7%D9%84%D9%85%D9%83_%D9%86%D9%85%D8%B1_%D9%85%D8%B4%D9%87%D8%AF_%D9%84%D9%84%D8%BA%D8%B1%D9%88%D8%A8_%D9%88%D9%82%D8%A7%D8%B1%D8%A8_%D9%8A%D8%B9%D8%A8%D8%B1_%D8%B9%D9%84%D9%89_%D8%A7%D9%84%D9%86%D9%8A%D9%84_%D8%A7%D9%84%D8%A3%D8%B2%D8%B1%D9%82.jpg) by Mojtaba Abdlbagi, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Resized and converted to WebP.
- `3eaa6670732c4d2d97476b1f7acbff7e.png`: [Laptop and coffee on a desk](https://commons.wikimedia.org/wiki/File:Coffee-desk-laptop-notebook_(24244320481).jpg) by www.Pixel.la Free Stock Photos, [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Resized and converted to PNG.
- `demo-campus-walk.webp`, `demo-study-desk.webp`, and `demo-market-day.webp`: photos supplied by the project owner, resized and converted to WebP.

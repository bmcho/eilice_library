import csv
import pymysql
import os

from datetime import datetime

conn = pymysql.connect(
            user = os.environ.get('DBuser'),
            passwd = os.environ.get('DBpw'),
            host = 'localhost',
            port = 3306,
            db = os.environ.get('DBname'),
            charset = 'utf8mb4'
)

cursor = conn.cursor(pymysql.cursors.DictCursor)

with open('data.csv', 'r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        # published_at = datetime.strptime(
				# 		row['publication_date'], '%Y-%m-%d')
        # print(row['publication_date'])
        image_path = f"/static/src/img/{row['id']}"
        try:
            open(f'app/{image_path}.png')
            image_path += '.png'
        except:
            image_path += '.jpg'

        cursor.execute(
                    'INSERT INTO book (id, book_name, publisher, author, publication_date, page, isbn, description, image_url, stock) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (int(row['id']), row['book_name'], row['publisher'], row['author'], row['publication_date'], int(row['pages']), str(row['isbn']), row['description'], image_path, 1)
                )

        print("삽입")

    conn.commit()

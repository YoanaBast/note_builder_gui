import json
import os

import psycopg2

with open("updated_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

connect_db = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432")
)

cur = connect_db.cursor()

#mapping of category name -> id
cur.execute("SELECT id, name FROM nav_categories")
category_map = {name: cid for cid, name in cur.fetchall()}

#insert notes
for topic, details in data.items():
    category_name = details.get("category")
    content = details.get("content")

    category_id = category_map.get(category_name)
    if category_id is None:
        #create the category if it doesn't exist
        cur.execute(
            "INSERT INTO nav_categories (name) VALUES (%s) RETURNING id",
            (category_name,)
        )
        category_id = cur.fetchone()[0]
        category_map[category_name] = category_id

    cur.execute(
        "INSERT INTO notes (topic, content, category_id) VALUES (%s, %s, %s)",
        (topic, content, category_id)
    )

connect_db.commit()
cur.close()
connect_db.close()
print("All notes imported successfully!")
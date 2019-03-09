select_cats_query = """SELECT *
                           FROM cats
                           ORDER BY {} {}
                           LIMIT {}
                           OFFSET {}"""

insert_cat_query = """INSERT INTO cats (name, color, tail_length, whiskers_length)
                          VALUES (:name, :color, :tail_length, :whiskers_length)"""

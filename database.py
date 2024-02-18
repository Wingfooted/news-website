'''import mysql.connector
import time
import json
from mysql.connector import Error'''

import mysql.connector
from mysql.connector import pooling, Error
from functions import hash_string

import time
import json
import ast

#USER CLASSES
class Database:
    def __init__(self, host, user, password, database):
        self.pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            pool_reset_session=True,
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.operations = DataOperations(self.pool)
        self.strings = Strings()

    def write_article(self, title, summary, content, author_id, author_name, category_id, article_thumbnail, tags, views=1):
        #INSERT INTO articles (article_id, title, summary, content, views, author_id, author_name, category_id, publication_date, article_thumbnail, tags)
        try:
            article_id = self.operations.create(
                table="articles",
                columns=['article_id', 'title', 'summary', 'content', 'views', 'author_id', 'author_name', 'category_id', 'article_thumbnail', 'tags'],
                values=[hash_string(title), title, summary, content, views, author_id, author_name, category_id, article_thumbnail, str(tags)]
            )

            print(f"Sucsessfully create article {title}")
        except Error as e:
            print("Error:", e)

    ###This is the one
    def get_article(self, article_id):
        try:
            content = self.operations.read(
                table="articles",
                where_columns=["article_id"],
                where_values=[article_id]
            ) 
            return content
        except Error as e:
            print("Error:", e)
            return None

    def get_author(self, author_id):
        try:
            content = self.operations.read(
                table="authors",
                where_columns=["author_id"],
                where_values=[author_id]
            )
            
            return content
        except Error as e:
            print("Error:", e)
            return None
    
    def get_homepage(self):
        try:
            query2 = """

            (
                SELECT
                    'latest' AS section, 
                    `article_id`, `title`, `summary`, `content`, `views`, `author_id`, `author_name`, `category_id`, `publication_date`, `article_thumbnail`, `tags`, 
                    NULL AS `view_time_ratio`
                FROM articles
                ORDER BY `publication_date` DESC
                LIMIT 4
            )
            UNION ALL
            (
                SELECT
                    'featured' AS section,
                    `article_id`, `title`, `summary`, `content`, `views`, `author_id`, `author_name`, `category_id`, `publication_date`, `article_thumbnail`, `tags`, 
                    `views` / TIMESTAMPDIFF(HOUR, `publication_date`, NOW()) AS `view_time_ratio`
                FROM articles
                ORDER BY `view_time_ratio` DESC
                LIMIT 5
            )
            UNION ALL
            (
                SELECT
                    'carousel' AS section,
                    `article_id`, `title`, `summary`, `content`, `views`, `author_id`, `author_name`, `category_id`, `publication_date`, `article_thumbnail`, `tags`, 
                    `views` / TIMESTAMPDIFF(HOUR, `publication_date`, NOW()) AS `view_time_ratio`
                FROM articles 
                ORDER BY `view_time_ratio`
                LIMIT 4
            )
            UNION ALL
            (
                SELECT
                    CAST(category_id AS CHAR) AS section,
                    `article_id`, `title`, `summary`, `content`, `views`, `author_id`, `author_name`, `category_id`, `publication_date`, `article_thumbnail`, `tags`,
                    `views` / TIMESTAMPDIFF(HOUR, `publication_date`, NOW()) AS `view_time_ratio`
                FROM (
                    SELECT
                        `article_id`, `title`, `summary`, `content`, `views`, `author_id`, `author_name`, `category_id`, `publication_date`, `article_thumbnail`, `tags`,
                        ROW_NUMBER() OVER (PARTITION BY `category_id` ORDER BY `views` DESC) AS `category_rank`
                    FROM articles
                ) ranked_articles
                WHERE `category_rank` <= 4 -- this limits the ammount per category. Category rank is a metric of articles position in the category. 
            );
            
            """
            content = self.operations.raw(query2)
            return content
        except Error as e:
            print("Error:", e)
            return None

    def delete_publication(self, publication):
        try:
            # First, delete all articles with the specified publication
            self.operations.destroy(table="articles", where_columns=["publication"], where_values=[publication])

            # Then, delete the publication itself
            self.operations.destroy(table="publications", where_columns=["publication"], where_values=[publication])

            print(f"Successfully deleted publication: {publication}")
        except Error as e:
            print("Error:", e)
            
    def create_publication(self, publication_string, categories):
        try:
            # Create a new publication in the publications table
            publication_id = self.operations.create(
                table="publications",
                columns=["publication", "categories", "header", "body", "footer"],
                values=[publication_string, json.dumps(categories),
                    self.strings.generic_header(publication_string, categories),
                    self.strings.generic_body(),
                    self.strings.generic_footer() 
                ]
            )
            print(f"Successfully created publication '{publication_string}' with ID: {publication_id}")
        except Error as e:
            print("Error:", e)

    def create_article(self, publication, title, summary, author, category, content, url=None, sub_title=None, live=False, tags=None):
        try:
            url=title.replace(" ", "-")
            time = 0
            
            if tags:
                input_tags = json.dumps(tags)
            else:
                input_tags = '[]'
            
            article_id = self.operations.create(
                table="articles",
                columns=[
                    "publication"
                    , "title"
                    , "sub_title"
                    , "summary"
                    , "author"
                    , "publish_date"
                    , "category"
                    , "content"
                    , "url"
                    , "live"
                    , "tags"
                ],
                values=[
                    publication
                    , title
                    , sub_title
                    , summary
                    , author
                    , time
                    , category
                    , content
                    , url
                    , live
                    , input_tags
                ]
            )

            print(f"Successfully created article '{title}' with ID: {article_id}")
        except Error as e:
            print("Error:", e)

    def update_publication_style(self, publication, stylesheet):
        try:
            self.operations.update(
                table="publications",
                columns=["stylesheet"],
                values=[stylesheet],
                where_columns=["publication"],
                where_values=[publication]
            )
            print(f"Stylesheet for {publication} updated successfully.")
        except Error as e:
            print("Error:", e)

    def update_publication_header(self, publication, new_header):
        try:
            self.operations.update(
                table="publications",
                columns=["header"],
                values=[new_header],
                where_columns=["publication"],
                where_values=[publication]
            )
            print(f"header for {publication} updated successfully.")
        except Error as e:
            print("Error:", e)
    
    def get_articles_url(self, publication, url_s):
        try:
            articles = self.operations.read()
            #TODO WIP FInish, takes a list of urls and finds their articles thumbnails?

        except Error as e:
            print("Error:", e)

#METHOD CLASSES
class DataOperations:
    def __init__(self, pool):
        self.pool = pool

    def create(self, table, columns, values):
        try:
            connection = self.pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()

                columns_str = ", ".join(columns)
                placeholders = ", ".join(["%s"] * len(values))
                sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
                
                cursor.execute(sql, values)
                connection.commit()
                
                return cursor.lastrowid  # Return the ID of the newly inserted row

            else:
                print("Failed to establish connection.")
        except Error as e:
            print("Error:", e)
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def update(self, table, columns, values, where_columns, where_values):
        try:
            connection = self.pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()

                set_values = ", ".join([f"{col} = %s" for col in columns])
                where_clause = " AND ".join([f"{col} = %s" for col in where_columns])
                
                sql = f"UPDATE {table} SET {set_values} WHERE {where_clause}"
                cursor.execute(sql, values + where_values)
                
                connection.commit()
                
            else:
                print("Failed to establish connection.")
        except Error as e:
            print("Error:", e)
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def read(self, table, where_columns, where_values):
        print(where_columns, where_values)
        try:
            connection = self.pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)

                where_clause = " AND ".join([f"{col} = %s" for col in where_columns])
                sql = f"SELECT * FROM {table} WHERE {where_clause}"
                #print(sql)
                cursor.execute(sql, where_values)
                
                result = cursor.fetchall()
                return result

            else:
                print("Failed to establish connection.")
        except Error as e:
            print("Error:", e)
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def destroy(self, table, where_columns, where_values):
        try:
            connection = self.pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()

                where_clause = " AND ".join([f"{col} = %s" for col in where_columns])
                sql = f"DELETE FROM {table} WHERE {where_clause}"
                cursor.execute(sql, where_values)
                
                connection.commit()
                
            else:
                print("Failed to establish connection.")
        except Error as e:
            print("Error:", e)
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def raw(self, sql):
        try:
            connection = self.pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor(dictionary=True, buffered=True)
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
            else:
                print("Failed to establish connection.")
        except Error as e:
            print("Error:", e)
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
        

#OUTPUT CLASSES
class Article:
    def __init__(self, ID, title, sub_title, summary, category, content, publication, publish_date, author, url, tags, live):
        self.ID = ID
        self.title = title
        self.sub_title = sub_title
        self.content = content
        self.category = category
        self.summary = summary
        self.publication = publication
        self.publish_date = publish_date
        self.author = author
        self.url = url
        self.tags = tags
        self.live = live

class Publication:
    def __init__(self, ID, publication, stylesheet, categories, header, landing, body, footer, logo_html):
        self.ID = ID
        self.publication = publication
        self.stylesheet = stylesheet
        self.categories = json.loads(categories)
        self.header = header
        self.landing = landing
        self.body = body
        self.footer = footer
        self.logo_html = logo_html

        sample = {'ID': 1,
        'publication': 'AIO Reporting',
        'stylesheet': 'reporting.css',
        'categories': '["Technology", "Science", "Education"]',
        'header': None, 'landing': None, 'body': None, 'footer': None}

class Strings:
    def __init__(self):
        pass
    
    def generic_header(self, publication, categories):
        return f"""
            <a href="/{publication}">
                <div class="logo">
                    <p>{publication}</p>
                </div>
            </a>
            <hr class="header-line">
            <div id="categories-section">
                <ul id="categories-list">
                    {''.join([f'<a class="category-link" href="/{publication}/{category}">{category}</a>' for category in categories])}
                </ul>
            </div>
            <hr class="header-line">
        """
    
    def generic_footer(self):
        return None
    
    def generic_body(self):
        return "<div id='content' class='content'></div>"
CREATE DATABASE anthropologie;
USE anthropologie; 
-- DROP DATABASE anthropologie;

CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    summary VARCHAR(255) NOT NULL
);
SELECT * FROM authors;
SELECT * FROM articles;
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
UPDATE articles
SET author_id = 1;
/*For the purposes of article storage, it is actually possible to not keep the images within the articles text content.
this is because articles will be rendered when clicked on, and image data is not needed immediately*/
CREATE TABLE articles (
    article_id VARCHAR(10) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    summary TEXT, 
    content LONGTEXT NOT NULL, 
    views INT DEFAULT 0,
    author_id INT,
    author_name VARCHAR(255), 
    category_id INT REFERENCES categories(category_id),
    publication_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    article_thumbnail VARCHAR(255) DEFAULT 'static/static_images/blank.png', 
    tags VARCHAR(255)
);

/*implement file storage system on a later date*/
CREATE TABLE article_images (
    image_id SERIAL PRIMARY KEY,
    article_id INT REFERENCES articles(article_id),
    image_url VARCHAR(255) NOT NULL
);

CREATE TABLE feature (
    position VARCHAR(255) PRIMARY KEY,
    article_id SERIAL
);
SET SQL_SAFE_UPDATES = 1;
CREATE TABLE articles (
    article_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    summary TEXT, 
    content LONGTEXT NOT NULL, 
    views INT DEFAULT 0,
    author_id INT REFERENCES authors(author_id),
    author_name VARCHAR(255), 
    category_id INT REFERENCES categories(category_id),
    publication_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    article_thumbnail VARCHAR(255) DEFAULT 'static/static_images/blank.png', 
    tags VARCHAR(255)
);

INSERT INTO articles (article_id, title, summary, content, views,author_id, author_name, category_id, tags) VALUES 
(
1, 'test 1', 'this is a test article', '<div class="text">This is some text for the article</div><div class="text">this is somre more text</div>',0,1,'Alexander Wells',1,""
);
SELECT * FROM authors;
INSERT INTO authors (author_id, name, email, password, summary) VALUES (1, 'Alexander Wells', 'alexanderjwells04@gmail.com', 'Wells', "L'anthropologie Founder. I like journalism and attend USYD");
SELECT * FROM categories;
SELECT- * FROM articles;

--DELETE FROM articles WHERE article_id ='40839a3b2';
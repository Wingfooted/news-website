(
    SELECT
        'Latest Articles' AS section,
        article_id, title, summary, content, views, author_id, category_id, publication_date, article_thumbnail, tags, NULL AS view_time_ratio
    FROM articles
    ORDER BY publication_date DESC
    LIMIT 4
)
UNION ALL
(
    SELECT
        'Top View/Time Ratio Articles' AS section,
        article_id, title, summary, content, views, author_id, category_id, publication_date, article_thumbnail, tags,
        COALESCE(views / GREATEST(TIMESTAMPDIFF(SECOND, publication_date, CURRENT_TIMESTAMP), 1), RAND()) AS view_time_ratio
    FROM articles
    WHERE TIMESTAMPDIFF(SECOND, publication_date, CURRENT_TIMESTAMP) > 0
    ORDER BY view_time_ratio DESC
    LIMIT 4
)
UNION ALL
(
    SELECT
        'Category Articles' AS section,
        article_id, title, summary, content, views, author_id, category_id, publication_date, article_thumbnail, tags, NULL AS view_time_ratio
    FROM articles
    WHERE category_id IN (1, 2, 3, 4, 5)
    LIMIT 4
)
UNION ALL
(
    SELECT
        'Top View/Time Ratio in Categories' AS section,
        article_id, title, summary, content, views, author_id, category_id, publication_date, article_thumbnail, tags, NULL AS view_time_ratio
    FROM (
        SELECT
            a.*,
            RANK() OVER (PARTITION BY a.category_id ORDER BY a.views / GREATEST(TIMESTAMPDIFF(SECOND, a.publication_date, CURRENT_TIMESTAMP), 1) DESC) AS rnk
        FROM articles a
        WHERE a.category_id IN (1, 2, 3, 4)
    ) AS ranked_categories
    WHERE rnk = 1
)
UNION ALL
(
    SELECT
        'Top Views in Categories' AS section,
        article_id, title, summary, content, views, author_id, category_id, publication_date, article_thumbnail, tags, NULL AS view_time_ratio
    FROM (
        SELECT
            a.*,
            RANK() OVER (PARTITION BY a.category_id ORDER BY a.views DESC) AS rnk
        FROM articles a
        WHERE a.category_id IN (1, 2, 3, 4)
    ) AS ranked_views
    WHERE rnk = 1
);

INSERT INTO articles (
    article_id,
    title,
    summary,
    content,
    views,
    author_id,
    category_id,
    publication_date,
    article_thumbnail,
    tags
) VALUES (
    2,
    'Caravaggio: Baroque Artistry',
    'An exploration of the life and works of the Baroque artist Caravaggio.',
    'Caravaggio, born Michelangelo Merisi, was an Italian Baroque painter known for his revolutionary approach to art...',
    4,  -- Assuming initial views are zero
    1,  -- Replace with the actual author_id
    3,  -- Replace with the actual category_id for art history or a related category
    CURRENT_TIMESTAMP,  -- Current timestamp for publication date
    '/static/images/caravaggio_thumbnail.jpg',  -- Replace with the actual path to the thumbnail image
    'art, Baroque, Caravaggio'  -- Replace with relevant tags
);

SELECT * FROM articles;


(
    -- Latest articles
    SELECT
        'Latest' AS section, 
        article_id, title, summary, content, views, author_id, category_id, publication_date, article_thumbnail, tags, 
        NULL AS view_time_ratio
    FROM articles
    ORDER BY publication_date DESC
    LIMIT 4
)
UNION ALL
(
	-- featured
    SELECT
		'Featured' AS section,
		article_id, title, summary, content, views, author_id, category_id, publication_date, article_thumbnail, tags, 
		views / TIMESTAMPDIFF(HOUR, publication_date, NOW()) AS view_time_ratio
	FROM articles
    ORDER BY view_time_ratio DESC
    LIMIT 5
)
UNION ALL
(
	-- carousel
	SELECT
		'Carousel' AS section,
		article_id, title, summary, content, views, author_id, category_id, publication_date, article_thumbnail, tags, 
		views / TIMESTAMPDIFF(HOUR, publication_date, NOW()) AS view_time_ratio
	FROM articles 
    ORDER BY view_time_ratio
    LIMIT 4
)
UNION ALL
(
    -- Top 4 most viewed articles in each category
    SELECT
        CAST(category_id AS CHAR) AS section,
        article_id, title, summary, content, views, author_id, category_id, publication_date, article_thumbnail, tags,
        views / TIMESTAMPDIFF(HOUR, publication_date, NOW()) AS view_time_ratio
    FROM (
        SELECT
            article_id, title, summary, content, views, author_id, category_id, publication_date, article_thumbnail, tags,
            ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY views DESC) AS category_rank
        FROM articles
    ) ranked_articles
    WHERE category_rank <= 4 -- this limits the ammount per category. Category rank is a metric of articles position in the category. 
);

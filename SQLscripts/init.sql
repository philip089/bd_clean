
CREATE USER postgres WITH PASSWORD 'admin';
ALTER USER postgres WITH SUPERUSER;

CREATE TABLE filtered_DE (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(255),
    title VARCHAR(255),
    publishedAt TIMESTAMP,
    categoryId INT,
    trending_date TIMESTAMP,
    tags TEXT,
    view_count INT,
    likes INT,
    dislikes INT,
    comment_count INT,
    comments_disabled BOOLEAN,
    ratings_disabled BOOLEAN,
    country VARCHAR(255)
);


CREATE TABLE edge_table (
    Source VARCHAR(255),
    Target VARCHAR(255),
    Weight INT
);


CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    country VARCHAR(255)
);


CREATE TABLE node_data (
    tag VARCHAR(255),
    category_id INT,
    count INT,
    color VARCHAR(255),
    category_name VARCHAR(255)
);

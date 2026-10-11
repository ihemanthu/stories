
-- Application Database DDL Script (Base).
-- Using Actual names of the entities used in the application, 
-- helps in understanding the meaning without any explanation for developers

CREATE TABLE authors (
    author_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255),
    email VARCHAR(254) NOT NULL UNIQUE,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    password_hash TEXT NOT NULL, -- choose text so any hashing algorithm can be applied.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_role CHECK  (role IN ('user', 'admin'))
);


CREATE TABLE stories (
    story_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    author_id BIGINT NOT NULL REFERENCES authors(author_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'in_draft',
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_status CHECK  (status IN ('in_draft', 'published', 'archived'))
);

-- These are the most quried in the application.
CREATE INDEX idx_author ON stories(author_id);

CREATE TABLE tags (
    tag_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE story_tags (
    tag_id BIGINT NOT NULL REFERENCES tags(tag_id) ON DELETE CASCADE,
    story_id BIGINT NOT NULL REFERENCES stories(story_id) ON DELETE CASCADE,
    PRIMARY KEY (tag_id, story_id)
);

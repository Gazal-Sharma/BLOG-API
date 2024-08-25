CREATE TABLE IF NOT EXISTS Users(
    u_id SERIAL PRIMARY KEY,
    u_name VARCHAR(20) NOT NULL,
    u_email VARCHAR(20) NOT NULL UNIQUE,
    u_username VARCHAR(20) NOT NULL UNIQUE,
    u_password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS BlogPost(
    b_id SERIAL PRIMARY KEY,
    username_post VARCHAR(20) REFERENCES Users(u_username),
    Post_Title VARCHAR(10) NOT NULL UNIQUE,
    Post_Content TEXT NOT NULL,
    Post_Author VARCHAR(20) NOT NULL,
    Post_Time_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Post_Time_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Comments(
    c_id SERIAL PRIMARY KEY, 
    post_title VARCHAR(10),
    username_post VARCHAR(20),
    c_Content TEXT NOT NULL,
    c_Author VARCHAR(20) NOT NULL,
    c_Time_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    c_Time_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_title) REFERENCES BlogPost(Post_Title), 
    FOREIGN KEY (username_post) REFERENCES Users(u_username)
);

CREATE INDEX IF NOT EXISTS idx_post ON BlogPost(b_id);
CREATE INDEX IF NOT EXISTS idx_user_email ON Users(u_email);


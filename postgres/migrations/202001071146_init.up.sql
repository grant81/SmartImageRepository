create TABLE image_info (
    image_id bigserial,
    image_url text NOT NULL UNIQUE,
    PRIMARY KEY (image_id));

create TABLE image_tag (
    image_id BIGINT,
    tag text,
    FOREIGN KEY (image_id) REFERENCES image_info(image_id));
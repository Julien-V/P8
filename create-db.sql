CREATE TABLE pb_categories (
    id SERIAL PRIMARY KEY,
    category_name varchar(500) NOT NULL UNIQUE
);
CREATE TABLE pb_products(
	id SERIAL PRIMARY KEY,
	product_name text NOT NULL,
	brands text,
	code bigint NOT NULL UNIQUE,
	categories text NOT NULL,
	nutrition_grades varchar(1) NOT NULL,
	stores text,
	url text NOT NULL,
	added_timestamp int NOT NULL,
	updated_timestamp int
);
CREATE TABLE pb_user (
	id SERIAL PRIMARY KEY,
	name text NOT NULL,
	email text NOT NULL,
	password text NOT NULL
);
CREATE TABLE pb_favorite(
	user_id int NOT NULL REFERENCES pb_user(id),
	product_id int NOT NULL REFERENCES pb_products(id),
	updated_timestamp int NOT NULL,
	PRIMARY KEY (user_id, product_id)
);
CREATE TABLE pb_categories_products (
	category_id int NOT NULL REFERENCES pb_categories(id), 
	product_id int NOT NULL REFERENCES pb_products(id),
	PRIMARY KEY (category_id, product_id)
);
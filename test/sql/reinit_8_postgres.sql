DROP table IF EXISTS table8;

CREATE TABLE table8 (
	column_id SERIAL PRIMARY KEY NOT NULL,
	column_2 TEXT
);

INSERT INTO table8
(
    column_2
)
VALUES (
	'test'
);

INSERT INTO table8
(
    column_2
)
VALUES (
	'test2'
);
DROP table IF EXISTS table11;

CREATE TABLE table11 (
	column_id INTEGER PRIMARY KEY,
    column_to_filter_1 TEXT,
    column_to_filter_2 TEXT
);

INSERT INTO table11
(
	column_id,
    column_to_filter_1,
    column_to_filter_2
)
VALUES (
	1, 
	'test',
    'test'
);

INSERT INTO table11
(
	column_id,
    column_to_filter_1,
    column_to_filter_2
)
VALUES (
	2, 
	'test2',
    'test2'
);
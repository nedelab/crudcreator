DROP table IF EXISTS table12;

CREATE TABLE table12 (
	column_id INTEGER PRIMARY KEY,
    column_date timestamp
);

INSERT INTO table12
(
	column_id,
    column_date
)
VALUES (
	1, 
	'2023-03-25T00:00:00'
);

INSERT INTO table12
(
	column_id,
    column_date
)
VALUES (
	2, 
	'2023-03-20T00:00:00'
);
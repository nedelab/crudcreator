DROP table IF EXISTS table16;

CREATE TABLE table16 (
	column_id INTEGER PRIMARY KEY,
    column_test TEXT
);

INSERT INTO table16
(
	column_id,
    column_test
)
VALUES (
	1, 
	'test'
);

INSERT INTO table16
(
	column_id,
    column_test
)
VALUES (
	2, 
	'test2'
);

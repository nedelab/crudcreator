DROP table IF EXISTS table5;

CREATE TABLE table5 (
	column_id INTEGER,
	is_deleted boolean
);

INSERT INTO table5
(
	column_id,
    is_deleted
)
VALUES (
	1,  
	false
);

INSERT INTO table5
(
	column_id,
    is_deleted
)
VALUES (
	2,  
	true
);

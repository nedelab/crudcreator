DROP table IF EXISTS table18;

CREATE TABLE table18 (
	column_to_join INTEGER PRIMARY KEY NOT NULL,
	column_id INTEGER
);

INSERT INTO table18
(
    column_to_join,
	column_id
)
VALUES (
    1,
	1
);


INSERT INTO table18
(
    column_to_join,
	column_id
)
VALUES (
    2,
	2
);
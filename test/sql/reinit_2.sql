DROP table IF EXISTS table2;

CREATE TABLE table2 (
	column_pk_becomes_not_pk INTEGER PRIMARY KEY,
    column_not_pk_becomes_pk INTEGER
);

INSERT INTO table2
(
	column_pk_becomes_not_pk,
    column_not_pk_becomes_pk
)
VALUES (
	1, 
	1
);

INSERT INTO table2
(
	column_pk_becomes_not_pk,
    column_not_pk_becomes_pk
)
VALUES (
	2, 
	2
);
DROP table IF EXISTS table9;

CREATE TABLE table9 (
	column_pk_becomes_not_pk INTEGER PRIMARY KEY,
    column_not_pk_becomes_pk INTEGER,
    column_not_pk_becomes_pk_default INTEGER DEFAULT 0
);

INSERT INTO table9
(
	column_pk_becomes_not_pk,
    column_not_pk_becomes_pk,
    column_not_pk_becomes_pk_default
)
VALUES (
	1, 
	1,
    1
);

INSERT INTO table9
(
	column_pk_becomes_not_pk,
    column_not_pk_becomes_pk,
    column_not_pk_becomes_pk_default
)
VALUES (
	2, 
	2,
    2
);
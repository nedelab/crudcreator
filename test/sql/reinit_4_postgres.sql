DROP table IF EXISTS table4;

CREATE TABLE table4 (
    column_id int,
	column_byte BYTEA
);

INSERT INTO table4
(
    column_id,
	column_byte
)
VALUES ( 
    1,
	'some bytes'
);

DROP table IF EXISTS table25;

CREATE TABLE table25 (
	username TEXT,
	column_id INTEGER,
	other INTEGER
);

INSERT INTO table25
(
	username,
	column_id,
	other
)
VALUES (
	'user1',
	1,
	1
);

INSERT INTO table25
(
	username,
	column_id,
	other
)
VALUES (
	'user1',
	10,
	10
);


INSERT INTO table25
(
	username,
	column_id,
	other
)
VALUES (
	'user2',
	2,
	1
);
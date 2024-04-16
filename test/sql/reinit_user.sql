DROP table IF EXISTS table_user;

CREATE TABLE table_user (
	user_id INTEGER,
	username TEXT,
	column_id INTEGER,
	other TEXT
);

INSERT INTO table_user
(
	user_id,
	username,
	column_id,
	other
)
VALUES (
	1,
	'user1',
	10,
	'1'
);


INSERT INTO table_user
(
	user_id,
	username,
	column_id,
	other

)
VALUES (
	2,
	'user2',
	20,
	'2'
);
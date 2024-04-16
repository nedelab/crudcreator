DROP table IF EXISTS table3;

CREATE TABLE table3 (
	column_to_be_joined INTEGER,
	column_test VARCHAR(100),
	column_text_oui_non_bis VARCHAR(3)
);

INSERT INTO table3
(
	column_to_be_joined,
    column_test,
	column_text_oui_non_bis
)
VALUES (
	1,  
	'test_join',
	'oui'
);

INSERT INTO table3
(
	column_to_be_joined,
    column_test,
	column_text_oui_non_bis
)
VALUES (
	2,  
	'test_join_2',
	'non'
);

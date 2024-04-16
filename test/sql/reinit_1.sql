DROP table IF EXISTS table1;

CREATE TABLE table1 (
	column_to_join INTEGER,
	column_int INTEGER,
	column_text_primary_not_null_no_default VARCHAR(100) PRIMARY KEY NOT NULL,
	column_text_not_null_default TEXT NOT NULL DEFAULT 'default_value_not_null',
	column_text_default TEXT DEFAULT 'default_value',
	column_text_no_default VARCHAR(100),
	column_text_overwritten_default VARCHAR(100),
	column_text_not_writable TEXT DEFAULT 'default_value_not_writable',
	column_text_not_writable_no_default VARCHAR(100),
	column_text_creatable_not_updatable VARCHAR(100),
	column_text_updatable_not_creatable VARCHAR(100),
	column_text_oui_non VARCHAR(3) DEFAULT 'oui',
	column_text_not_readable TEXT,
	column_invisible TEXT
);

INSERT INTO table1
(
	column_to_join,
	column_int, 
	column_text_primary_not_null_no_default, 
	column_text_not_null_default, 
	column_text_default,
	column_text_no_default,
	column_text_overwritten_default,
	column_text_not_writable,
	column_text_not_writable_no_default,
	column_text_creatable_not_updatable,
	column_text_updatable_not_creatable,
	column_text_oui_non,
	column_invisible,
	column_text_not_readable
)
VALUES (
	1,
	1, 
	'pk1', 
	'test',
	'other_test',
	'no_default',
	'overwritten_default',
	'not_writable',
	'not_writable_no_default',
	'creatable_not_updatable_no_default',
	'updatable_not_creatable_no_default',
	'oui',
	'invisible',
	'not_readable'
);



INSERT INTO table1
(
	column_to_join,
	column_int, 
	column_text_primary_not_null_no_default, 
	column_text_not_null_default, 
	column_text_default,
	column_text_no_default,
	column_text_overwritten_default,
	column_text_not_writable,
	column_text_not_writable_no_default,
	column_text_creatable_not_updatable,
	column_text_updatable_not_creatable,
	column_text_oui_non,
	column_invisible,
	column_text_not_readable
)
VALUES (
	2,
	2, 
	'pk2', 
	'test2',
	'other_test_2',
	'no_default_2',
	'overwritten_default_2',
	'not_writable_2',
	'not_writable_no_default_2',
	'creatable_not_updatable_no_default_2',
	'updatable_not_creatable_no_default_2',
	'non',
	'invisible_2',
	'not_readable_2'
);
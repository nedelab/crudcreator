DROP table IF EXISTS table6;

CREATE TABLE table6 (
	column_id INTEGER,
	is_deleted boolean,
    is_active VARCHAR(3) DEFAULT 'oui'
);

INSERT INTO table6
(
	column_id,
    is_deleted,
    is_active
)
VALUES (
	1,  
	false,
    'oui'
);

INSERT INTO table6
(
	column_id,
    is_deleted,
    is_active
)
VALUES (
	2,  
	true,
    'non'
);

INSERT INTO table6
(
	column_id,
    is_deleted,
    is_active
)
VALUES (
	3,  
	false,
    'non'
);

INSERT INTO table6
(
	column_id,
    is_deleted,
    is_active
)
VALUES (
	3,  
	true,
    'oui'
);

DROP table IF EXISTS book;

CREATE TABLE book (
	book_id INTEGER,
	title VARCHAR(100),
    public_domain BOOLEAN DEFAULT 0
);

INSERT INTO book
(
	book_id,
	title, 
	public_domain
)
VALUES (
	1,
	"Cyrano de Bergerac", 
	1
);


INSERT INTO book
(
	book_id,
	title, 
	public_domain
)
VALUES (
	2,
	"We the Living", 
	0
);
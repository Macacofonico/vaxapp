CREATE TABLE cocktail (
	cocktail_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL UNIQUE ,
	instructions TEXT NOT NULL,
	author TEXT NOT NULL
	);


CREATE TABLE ingridients (
  ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	size TEXT NOT NULL,
	cocktail INTEGER NOT NULL,
  FOREIGN KEY(cocktail) REFERENCES cocktail(cocktail_id) ON DELETE CASCADE
);

CREATE TABLE suggested_spirits (
  spirits_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	cocktail INTEGER NOT NULL,
	FOREIGN KEY(cocktail) REFERENCES cocktail(cocktail_id) ON DELETE CASCADE
);


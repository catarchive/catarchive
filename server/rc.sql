CREATE SCHEMA IF NOT EXISTS main;

CREATE TABLE IF NOT EXISTS main.images (
	id serial,
	url text,
	ts timestamp,
	hits int,
	vid int,
	fid int,
	fc int
);

/* adding this table to nfldb to facilitate searching for rookies */


CREATE TABLE IF NOT EXISTS drafts
(
pkid SERIAL NOT NULL,
player_id character varying(10) NOT NULL,
draft_year INT NOT NULL,
draft_round INT NOT NULL,
overall_pick INT NOT NULL
PRIMARY KEY (pkid)
);

ALTER TABLE drafts
	ADD CONSTRAINT drafts_player_id_fkey
		FOREIGN KEY (player_id) REFERENCES player (player_id);
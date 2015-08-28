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
		
ALTER TABLE drafts
   ADD COLUMN team_id character varying(3) NOT NULL;
   
 ALTER TABLE drafts
  ADD CONSTRAINT drafts_team_id_fkey FOREIGN KEY (team_id)
      REFERENCES team (team_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE drafts
  ADD CONSTRAINT unique_draft_result UNIQUE(player_id);
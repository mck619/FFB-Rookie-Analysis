SELECT 	t1.*, t2.rec_yds_regular, t2.rec_tds_regular, t2.catches_regular, t2.targets_regular, t2.rush_yds_regular, t2.rush_tds_regular,
	t2.rush_att_regular
FROM 
	(	SELECT 	
			player.full_name, SUM(pp.receiving_yds) as "rec_yds", SUM(pp.receiving_tds) as "rec_tds", 
			SUM(pp.receiving_rec) as "catches", SUM(pp.receiving_tar) as "targets", SUM(pp.rushing_yds) as "rush_yds",
			SUM(pp.rushing_tds) as "rush_tds", SUM(pp.rushing_att) AS "rush_att"
		FROM
			player 	INNER JOIN play_player AS pp ON player.player_id = pp.player_id
				INNER JOIN game ON pp.gsis_id = game.gsis_id
		WHERE
			game.season_year = 2011 AND
			game.season_type = 'Preseason' 	
		GROUP BY
			player.full_name	) AS t1
	INNER JOIN
	(	SELECT 	
			player.full_name, SUM(pp.receiving_yds) as "rec_yds_regular", SUM(pp.receiving_tds) as "rec_tds_regular" , 
			SUM(pp.receiving_rec) as "catches_regular", SUM(pp.receiving_tar) as "targets_regular" , 
			SUM(pp.rushing_yds) as "rush_yds_regular", SUM(pp.rushing_tds) as "rush_tds_regular", 
			SUM(pp.rushing_att) AS "rush_att_regular"
		FROM
			player 	INNER JOIN play_player AS pp ON player.player_id = pp.player_id
				INNER JOIN game ON pp.gsis_id = game.gsis_id
		WHERE
			game.season_year = 2011 AND
			game.season_type = 'Regular' 	
		GROUP BY
			player.full_name	) AS t2
	ON t1.full_name = t2.full_name
	
WHERE rec_yds_regular != 0 OR rush_yds_regular != 0;
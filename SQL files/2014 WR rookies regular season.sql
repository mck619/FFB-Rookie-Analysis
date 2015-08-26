SELECT t1.full_name, player.team, player.college, player.position,
       t1.rec_yds as "receiving yds", t1.rec_tds as "receiving tds", t1.yds as "rush yds", t1.tds as "rush tds"
FROM player,
	    (SELECT player.full_name,SUM(play_player.rushing_yds) as yds, SUM(play_player.rushing_tds) as tds,
		    SUM(play_player.receiving_yds) as "rec_yds", SUM(play_player.receiving_tds) as "rec_tds"
	     FROM player, play_player, game 
	     WHERE player.years_pro = 2
	     AND game.season_type = 'Regular'
	     AND game.gsis_id = play_player.gsis_id 
	     AND (player.position = 'RB' OR player.position = 'WR') 
	     AND play_player.player_id = player.player_id
	     GROUP BY player.full_name) AS t1

WHERE player.full_name = t1.full_name
AND player.position = 'WR'
ORDER BY full_name;

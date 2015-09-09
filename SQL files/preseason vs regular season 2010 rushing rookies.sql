SELECT t2.full_name, t2.yds as p_yds, t2.tds as p_tds, t2.pts as p_pts, t4.yds as r_yds, t4.tds as r_tds, t4.pts as r_pts FROM
(SELECT t1.full_name, SUM(pp.rushing_yds) as yds, SUM(pp.rushing_tds) as tds, (.1*SUM(pp.rushing_yds) + 6*SUM(pp.rushing_tds)) as pts
FROM play_player AS pp
INNER JOIN 
(Select player.full_name, player.player_id FROM player INNER JOIN drafts ON player.player_id = drafts.player_id WHERE drafts.draft_year = 2010) as t1
ON pp.player_id = t1.player_id
INNER JOIN game as g
ON pp.gsis_id = g.gsis_id
WHERE g.season_type = 'Preseason'
AND g.season_year = 2010
GROUP BY t1.full_name) as t2
INNER JOIN
(SELECT t3.full_name, SUM(pp.rushing_yds) as yds, SUM(pp.rushing_tds) as tds, (.1*SUM(pp.rushing_yds) + 6*SUM(pp.rushing_tds)) as pts
FROM play_player AS pp
INNER JOIN 
(Select player.full_name, player.player_id FROM player INNER JOIN drafts ON player.player_id = drafts.player_id WHERE drafts.draft_year = 2010) as t3
ON pp.player_id = t3.player_id
INNER JOIN game as g
ON pp.gsis_id = g.gsis_id
WHERE g.season_type = 'Regular'
AND g.season_year = 2010
GROUP BY t3.full_name) as t4
ON t2.full_name = t4.full_name
INNER JOIN 
(SELECT player.full_name FROM drafts INNER JOIN player ON drafts.player_id = player.player_id
WHERE drafts.draft_year = 2010) as d1
ON t2.full_name = d1.full_name
WHERE t2.pts > 0 OR t4.pts > 0
ORDER BY t4.pts DESC;
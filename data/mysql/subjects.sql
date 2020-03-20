SELECT 'tibEntry', 'engEntry', 'sktEntry', 'newTibEntry', 'newEngEntry', 'newSktEntry', 'recID'
UNION ALL
SELECT tibEntry, engEntry, sktEntry, newTibEntry, newEngEntry, newSktEntry, recID
FROM 
	acipmaintenance.subjitems
GROUP BY tibEntry, engEntry, sktEntry, newTibEntry, newEngEntry, newSktEntry, recID
-- INTO 
-- 	outfile '/var/lib/mysql-files/etext_subjects_with_headers.csv' 
--     fields terminated by ',' enclosed by '"' lines terminated by '\n';
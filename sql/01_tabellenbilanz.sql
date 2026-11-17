
SELECT 'gemeinden' AS tabelle, COUNT(*) AS anzahl
FROM gemeinden

UNION ALL

SELECT 'tarife' AS tabelle, COUNT(*) AS anzahl
FROM tarife

UNION ALL

SELECT 'gemeindewerte' AS tabelle, COUNT(*) AS anzahl
FROM gemeindewerte;

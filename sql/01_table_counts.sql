
SELECT 'municipalities' AS table_name, COUNT(*) AS count
FROM municipalities

UNION ALL

SELECT 'tariffs' AS table_name, COUNT(*) AS count
FROM tariffs

UNION ALL

SELECT 'municipality_values' AS table_name, COUNT(*) AS count
FROM municipality_values;

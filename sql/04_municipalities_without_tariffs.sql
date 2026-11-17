
SELECT
    g.municipality_number,
    g.municipality_name,
    g.canton,
    g.municipality_type

FROM municipalities AS g

LEFT JOIN municipality_values AS w
    ON g.municipality_number = w.municipality_number

WHERE w.municipality_number IS NULL

ORDER BY g.municipality_number;

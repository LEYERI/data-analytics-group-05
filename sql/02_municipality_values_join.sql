
SELECT
    g.municipality_number,
    g.municipality_name,
    g.canton_id,
    g.canton,
    g.municipality_type_code,
    g.municipality_type,
    w.municipality_tariff

FROM municipality_values AS w

INNER JOIN municipalities AS g
    ON w.municipality_number = g.municipality_number

ORDER BY g.municipality_number;

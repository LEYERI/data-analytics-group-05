
SELECT
    g.municipality_type_code,
    g.municipality_type,
    COUNT(*) AS municipality_count,
    ROUND(AVG(w.municipality_tariff), 3) AS mean_rp_kwh,
    ROUND(MIN(w.municipality_tariff), 3) AS min_rp_kwh,
    ROUND(MAX(w.municipality_tariff), 3) AS max_rp_kwh

FROM municipality_values AS w

INNER JOIN municipalities AS g
    ON w.municipality_number = g.municipality_number

GROUP BY
    g.municipality_type_code,
    g.municipality_type

ORDER BY g.municipality_type_code;


SELECT
    g.gemeindenummer,
    g.gemeindename,
    g.kanton,
    g.gemeindetyp

FROM gemeinden AS g

LEFT JOIN gemeindewerte AS w
    ON g.gemeindenummer = w.gemeindenummer

WHERE w.gemeindenummer IS NULL

ORDER BY g.gemeindenummer;

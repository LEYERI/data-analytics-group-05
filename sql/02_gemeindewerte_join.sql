
SELECT
    g.gemeindenummer,
    g.gemeindename,
    g.kanton_id,
    g.kanton,
    g.gemeindetyp_code,
    g.gemeindetyp,
    w.tarif_gemeinde

FROM gemeindewerte AS w

INNER JOIN gemeinden AS g
    ON w.gemeindenummer = g.gemeindenummer

ORDER BY g.gemeindenummer;


SELECT
    g.gemeindetyp_code,
    g.gemeindetyp,
    COUNT(*) AS anzahl_gemeinden,
    ROUND(AVG(w.tarif_gemeinde), 3) AS mittelwert_rp_kwh,
    ROUND(MIN(w.tarif_gemeinde), 3) AS minimum_rp_kwh,
    ROUND(MAX(w.tarif_gemeinde), 3) AS maximum_rp_kwh

FROM gemeindewerte AS w

INNER JOIN gemeinden AS g
    ON w.gemeindenummer = g.gemeindenummer

GROUP BY
    g.gemeindetyp_code,
    g.gemeindetyp

ORDER BY g.gemeindetyp_code;

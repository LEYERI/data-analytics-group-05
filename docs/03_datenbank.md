# 3. Datenspeicherung und SQL-Abfragen

## Ziel

Wir speichern die aufbereiteten Daten in einer SQLite-Datenbank
und führen SQL-Abfragen direkt aus Python aus.

Die Umsetzung erfolgt im Notebook:
`notebooks/03_datenbank.ipynb`

## 3.1 Datenbank erstellen

Die Datenbank liegt unter:
`data/stromtarife.sqlite`

Wir verwenden die in Python enthaltene Bibliothek sqlite3.
Die Speicherung der pandas-Tabellen erfolgt mit to_sql().

| Tabelle | Inhalt | Zeilen |
|---|---|---:|
| gemeinden | Gemeindestammdaten mit Kanton und Gemeindetyp | 2’110 |
| tarife | Bereinigte einzelne Tarifwerte | 2’255 |
| gemeindewerte | Ein Tarifvergleichswert je Gemeinde | 2’108 |

Alle Tabellen verwenden die Gemeindenummer als gemeinsamen
Verknüpfungsschlüssel.

Gemeindename, Kanton und Gemeindetyp speichern wir zentral
in der Tabelle gemeinden.

Vor der Speicherung prüfen wir die Eindeutigkeit der
Gemeindenummern in den Stammdaten und Gemeindewerten sowie
die Zugehörigkeit der Tarifdaten zum Gemeindebestand.

Diese Prüfungen erfolgen im Python-Code. Es wurden keine
PRIMARY-KEY- oder FOREIGN-KEY-Constraints in SQLite definiert.

Beim erneuten Ausführen werden die drei Datenbanktabellen
aus den gespeicherten aufbereiteten CSV-Dateien neu erstellt.
Die CSV-Dateien und Rohdaten bleiben unverändert.

## 3.2 SQL-Abfragen aus Python

Die Abfragen werden mit pd.read_sql_query() ausgeführt.
Das Ergebnis steht anschliessend als pandas-Tabelle zur Verfügung.

Wir haben folgende Abfragen umgesetzt:

| Abfrage | Zweck |
|---|---|
| COUNT(*) und UNION ALL | Zeilenzahlen der drei Tabellen kontrollieren |
| INNER JOIN | Gemeindewerte mit den Gemeindestammdaten verbinden |
| GROUP BY mit AVG, MIN und MAX | Tarifvergleichswerte nach Gemeindetyp zusammenfassen |
| LEFT JOIN mit IS NULL | Gemeinden ohne Tarifvergleichswert ermitteln |

Der INNER JOIN liefert 2’108 Gemeinden.
Wir prüfen, dass die Anzahl der Gemeindewerte erhalten bleibt
und jede Gemeindenummer im Ergebnis einmal vorkommt.

Für die Gruppenzusammenfassung verwenden wir die Tabelle
gemeindewerte, damit jede Gemeinde einmal zählt.

Die Zusammenfassung ist ein unbereinigter Vergleich.
Der Kanton wird dabei noch nicht statistisch berücksichtigt.
Die Kantonskontrolle erfolgt später im Regressionsmodell.

ROUND() rundet lediglich die Ausgabe auf drei Nachkommastellen.
Die gespeicherten Tarifwerte bleiben unverändert.

## 3.3 Gemeinden ohne Tarifvergleichswert

Mit einem LEFT JOIN und IS NULL ermitteln wir:
- Augst im Kanton Basel-Landschaft,
- Nürensdorf im Kanton Zürich.

Damit stimmt die Datenbankauswertung mit der vorherigen
Datenaufbereitung überein.

Die 2’108 Gemeinden mit Tarifvergleichswert und die zwei
Gemeinden ohne Tarifvergleichswert ergeben zusammen
den vollständigen BFS-Bestand von 2’110 Gemeinden.

## 3.4 Gespeicherte Abfragen und Ergebnisse

Die SQL-Abfragen liegen unter:

- sql/01_tabellenbilanz.sql
- sql/02_gemeindewerte_join.sql
- sql/03_tarife_nach_gemeindetyp.sql
- sql/04_gemeinden_ohne_tarif.sql

Die gespeicherten Zusammenfassungen liegen unter:

- results/sql/tabellenbilanz.csv
- results/sql/tarife_nach_gemeindetyp.csv
- results/sql/gemeinden_ohne_tarif.csv

Die Datenbank wird aus den aufbereiteten Daten reproduzierbar
durch das Notebook erstellt.

## 3.5 KI-Unterstützung

ChatGPT unterstützte bei der Erstellung und Erklärung des
Python- und SQL-Codes sowie der Dokumentation.

Die Gruppe führte die Abfragen aus und prüfte die Zeilenzahlen,
die Gruppenzusammenfassung und die Gemeinden ohne Tarifwert.

Die Kontrolle erfolgte durch den Vergleich der
Datenbankergebnisse mit den Ergebnissen der Datenaufbereitung.
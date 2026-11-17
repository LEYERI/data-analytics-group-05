# 2. Datenaufbereitung und Integration

## Ziel

Wir verknüpfen die ElCom-Stromtarife mit den BFS-Gemeindedaten,
damit jeder Tarif einer Gemeinde, einem Kanton und einem
Stadt/Land-Typ zugeordnet werden kann.

Grundlage sind die gespeicherten Rohdaten aus der Datenerhebung.
Die Rohdateien bleiben unverändert.

## 2.1 Vorbereitung

Die Datenaufbereitung erfolgt im Notebook:

`notebooks/02_datenaufbereitung.ipynb`

Wir haben:
- die Gemeindenummer aus der ElCom-Gemeinde-URI extrahiert,
- die Gemeindenummer in beiden Tabellen als Int64 gespeichert,
- den Gesamttarif in einen numerischen Datentyp umgewandelt,
- die benötigten BFS-Spalten ausgewählt und verständlich benannt,
- die Stadt/Land-Codes um lesbare Bezeichnungen ergänzt.

Die Vorbereitung veränderte die Zeilenzahlen nicht.
Der bereits bekannte fehlende Gesamttarif blieb erhalten.

## 2.2 Erste Verknüpfung

Die Verknüpfung erfolgte über die Gemeindenummer als Left Join.
Damit blieben alle ElCom-Tarifzeilen zunächst erhalten.

Mit `validate="many_to_one"` prüften wir, dass jede Gemeindenummer
in der BFS-Tabelle höchstens einmal vorkommt.

Mit `indicator=True` kennzeichneten wir erfolgreiche und
nicht erfolgreiche Zuordnungen.

| Prüfung | Ergebnis |
|---|---:|
| ElCom-Tarifzeilen vor dem Join | 2’268 |
| Tarifzeilen nach dem Join | 2’268 |
| Erfolgreich zugeordnete Tarifzeilen | 2’251 |
| Nicht zugeordnete Tarifzeilen | 17 |
| BFS-Gemeinden ohne direkte ElCom-Zuordnung | 5 |

Der Join führte zu keinem Zeilenverlust und keiner
unbeabsichtigten Vervielfachung.

## 2.3 Gemeindenummern harmonisieren

Die nicht zugeordneten Nummern wurden anhand amtlicher
BFS-Mutationsmeldungen geprüft.

Für 17 Tarifzeilen wurde eine Zuordnungsnummer zum Gemeindestand
01.01.2026 ergänzt. Die ursprüngliche ElCom-Gemeindenummer blieb
erhalten.

Die Änderungen betreffen Gemeindefusionen, Eingemeindungen
und den Kantonswechsel von Moutier.

Beispiel: Moutier erscheint im ElCom-Abruf unter Nummer 700.
Zum 01.01.2026 wechselte die Gemeinde vom Kanton Bern zum
Kanton Jura und erhielt die Nummer 6831.

Die vollständige Zuordnungstabelle enthält:
- ursprüngliche Gemeindenummer,
- Gemeindenummer zum Stand 2026,
- BFS-Mutationsnummer,
- Link zur amtlichen Quelle.

Nach der Harmonisierung konnten alle 2’268 Tarifzeilen
einer BFS-Gemeinde zugeordnet werden.

### Fachliche Bedeutung

Bei fusionierten Gemeinden wird der Tarif eines früheren
Gemeindegebiets der heutigen Gemeinde zugeordnet.
Das bedeutet nicht automatisch, dass im gesamten heutigen
Gemeindegebiet ein einheitlicher Tarif gilt.

Wir verwenden für die spätere Gruppierung die BFS-Typologie
der aktuellen Gemeinde zum gewählten Gemeindestand.

## 2.4 Wiederholungen behandeln

Nach der Harmonisierung gehörten 23 Zeilen zu mehrfach
vorkommenden aktuellen Gemeinde-Betreiber-Kombinationen.

Wir unterschieden:
- gleiche aktuelle Gemeinde, gleicher Betreiber, gleicher Tarif:
  einmal in der weiteren Tariftabelle berücksichtigen;
- gleiche aktuelle Gemeinde und gleicher Betreiber, aber
  unterschiedliche Tarife: getrennt erhalten.

Dadurch wurden 12 Wiederholungen zusammengefasst.
Es verblieben 2’256 Tarifzeilen.

Die vollständigen Herkunftszeilen wurden separat aufbewahrt.

Beispiel: Für Root blieben die unterschiedlichen Tarifwerte
25.414 und 25.153 Rp./kWh erhalten.

## 2.5 Fehlenden Gesamttarif behandeln

Bei einer Zeile fehlte der Gesamttarif.
Diese Zeile wurde aus der Tarifanalyse ausgeschlossen,
weil die Zielvariable fehlt.

Wir ersetzten den Wert weder durch null noch durch einen
geschätzten Tarif.

Die ausgeschlossene Zeile wurde mit dem Grund
„Gesamttarif fehlt“ separat gespeichert.
Die betroffene Gemeinde besitzt weiterhin einen anderen
gültigen Tarif im Datensatz.

## 2.6 Abschliessende Mengenbilanz

| Schritt | Anzahl Tarifzeilen |
|---|---:|
| ElCom-Rohdaten | 2’268 |
| Nach Harmonisierung der Gemeindenummern | 2’268 |
| Zusammengefasste Wiederholungen | −12 |
| Nach Zusammenfassung | 2’256 |
| Ausschluss wegen fehlendem Gesamttarif | −1 |
| Verbleibende Analysezeilen | 2’255 |

| Abdeckung | Anzahl Gemeinden |
|---|---:|
| BFS-Gemeinden insgesamt | 2’110 |
| Gemeinden mit mindestens einem gültigen Tarif | 2’108 |
| Gemeinden ohne passenden Tarif im Datenbestand | 2 |

Für Augst und Nürensdorf liegt im abgefragten Bestand keine
passende Tarifzeile vor. Daraus folgt nicht, dass diese Gemeinden
keinen Stromtarif haben.

Beide Gemeinden bleiben in den BFS-Stammdaten erhalten,
gehen vorerst aber nicht in die Tarifanalyse ein.

## 2.7 Gespeicherte Ergebnisse

Die aufbereiteten Tabellen liegen unter `data/processed/`.

| Datei | Inhalt |
|---|---|
| tarife_bereinigt.csv | Verknüpfte Tarifzeilen mit vorhandenem Gesamttarif |
| bfs_gemeinden_2026.csv | Ausgewählte BFS-Stammdaten |
| gemeindenummern_zuordnung.csv | Dokumentierte Nummernänderungen mit Quellen |
| tarife_herkunft.csv | Vollständige harmonisierte Herkunftszeilen |
| ausgeschlossene_tarife.csv | Ausgeschlossene Zeile mit Begründung |
| gemeinden_ohne_tarif.csv | BFS-Gemeinden ohne gültigen Tarif im Bestand |
| bereinigungsbilanz.csv | Mengenbilanz der Aufbereitung |

## 2.8 Grenzen und weitere Verarbeitung

Die Analysetabelle enthält weiterhin mehrere Tarifzeilen je
Gemeinde. Sie ist noch keine Tabelle mit einem Wert je Gemeinde.

Vor dem statistischen Gemeindevergleich legen wir fest,
wie Gemeinden mit mehreren Betreibern oder Tarifwerten
berücksichtigt werden.

Ohne Kundenzahlen oder Verbrauchsanteile können wir keinen
tatsächlich von den Haushalten bezahlten Durchschnittstarif
berechnen.

## 2.9 KI-Unterstützung

ChatGPT unterstützte bei der Erstellung und Erklärung des
Aufbereitungscodes, der Recherche amtlicher Mutationsmeldungen
und der Formulierung der Dokumentation.

Die Gruppe führte den Code aus und kontrollierte die
ausgegebenen Tabellen, Zuordnungen und Zeilenzahlen.

Die Prüfung nach der Harmonisierung zeigte, dass mehrere
frühere Gemeindegebiete zur gleichen aktuellen
Gemeinde-Betreiber-Kombination gehören können.
Ein pauschales Entfernen solcher Zeilen hätte unterschiedliche
Tarifwerte verlieren können. Deshalb wurden gleiche und
unterschiedliche Tarifwerte getrennt behandelt.

## Quellen

- BFS-Gemeindedaten zum Stand 01.01.2026:
  https://www.agvchapp.bfs.admin.ch/api/communes/levels?date=01-01-2026
- Amtliche BFS-Mutationsmeldungen:
  Die einzelnen Quellenlinks sind in
  `data/processed/gemeindenummern_zuordnung.csv` dokumentiert.
- ElCom-Datenzugang:
  https://www.elcom.admin.ch/de/tarifdaten-und-visualisierungen
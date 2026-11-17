# 1. Datenerhebung

## Ziel und Bezug zur Forschungsfrage

Unser Projekt untersucht die Stromtarife zwischen städtischen,
intermediären und ländlichen Schweizer Gemeinden unter
Berücksichtigung des Kantons.

Dafür erheben wir zwei Datenquellen:
1. ElCom-Stromtarife für die Tarifinformationen.
2. BFS-Gemeindedaten für Kanton und Stadt/Land-Typologie.

Die Datenerhebung erfolgt mit Python über offizielle Web-APIs.
Wir verwenden keine fertigen Fremddatensätze als primäre Datenquelle.

## 1.1 ElCom-Stromtarife

### Quelle und Zugang

- Herausgeber: Eidgenössische Elektrizitätskommission ElCom
- Datenzugang: LINDAS-SPARQL-Schnittstelle
- Endpunkt: https://ld.admin.ch/query
- Informationsseite:
  https://www.elcom.admin.ch/de/tarifdaten-und-visualisierungen
- Abrufdatum: 17.11.2026
- Methode: HTTP-POST mit einer SPARQL-Abfrage
- Antwortformat: JSON

SPARQL ist eine Abfragesprache für verknüpfte Daten.
Die vollständige verwendete Abfrage steht im Notebook und
in den gespeicherten Metadaten.

### Abgrenzung

Wir filtern die Daten auf:
- Tarifjahr 2026
- Haushaltsprofil H4 mit 4’500 kWh Jahresverbrauch
- Standardprodukt

### Erhobene Felder

| Feld | Bedeutung |
|---|---|
| gemeinde | Eindeutige Gemeinde-URI |
| betreiber | Eindeutige Betreiber-URI |
| gesamttarif | Gesamttarif in Rp./kWh |

Eine URI ist eine eindeutige Kennung in Form einer Webadresse.
Die Gemeinde-URI enthält die Gemeindenummer.

Eine Zeile entspricht einer Kombination aus Gemeinde und Betreiber
für das festgelegte Tarifjahr, Haushaltsprofil und Produkt.

Eine Gemeinde kann mehrere Betreiber und damit mehrere Tarifzeilen
haben. Diese Zeilen sind nicht automatisch Dubletten.

### Ergebnisse der ersten Qualitätsprüfung

| Prüfung | Ergebnis |
|---|---:|
| Tarifzeilen | 2’268 |
| Unterschiedliche Gemeinde-URIs | 2’122 |
| Unterschiedliche Betreiber-URIs | 551 |
| Fehlende Gemeinde-URIs | 0 |
| Fehlende Betreiber-URIs | 0 |
| Fehlende Gesamttarife | 1 |
| Vollständig identische Zeilen | 0 |
| Doppelte Gemeinde-Betreiber-Kombinationen | 0 |

Der fehlende Gesamttarif betrifft die Gemeinde-URI mit der
Nummer 3218 und die Betreiber-URI mit der Nummer 326.

Der fehlende Wert bleibt zunächst erhalten.
Wir ersetzen ihn nicht durch null.

## 1.2 BFS-Gemeindedaten

### Quelle und Zugang

- Herausgeber: Bundesamt für Statistik BFS
- Datenzugang: Applikation der Schweizer Gemeinden
- URL:
  https://www.agvchapp.bfs.admin.ch/api/communes/levels?date=01-01-2026
- Abrufdatum: 17.11.2026
- Methode: HTTP-GET
- Antwortformat: CSV
- Gewählter Gemeindestand: 01.01.2026

Wir speichern die vollständige Antwort mit 29 Spalten.
Für unser Projekt wählen wir zunächst fünf Felder aus.

### Ausgewählte Felder

| Feld | Bedeutung |
|---|---|
| BfsCode | BFS-Gemeindenummer |
| Name | Gemeindename |
| CantonId | Kantonskennung |
| Canton | Kantonsname |
| STALAN2020 | Stadt/Land-Typologie 2020 |

Die Typologieversion 2020 und der Gemeindestand 01.01.2026
bezeichnen unterschiedliche Dinge: die fachliche Klassifikation
und den zeitlichen Stand des Gemeindeverzeichnisses.

Für die spätere Verknüpfung verwenden wir BfsCode,
nicht HistoricalCode.

### Ergebnisse der ersten Qualitätsprüfung

Der Datensatz enthält 2’110 Gemeinden.
In den fünf ausgewählten Feldern fehlen keine Werte.
Die BFS-Gemeindenummer kommt jeweils genau einmal vor.

| STALAN2020 | Gemeindetyp | Anzahl |
|---|---|---:|
| 1 | Städtisch | 509 |
| 2 | Intermediär | 580 |
| 3 | Ländlich | 1’021 |
| Gesamt | | 2’110 |

## 1.3 Speicherung und Nachvollziehbarkeit

Das Notebook zur Datenerhebung liegt unter:

`notebooks/01_datenerhebung.ipynb`

Die unveränderten API-Antworten liegen unter:

`data/raw/`

Wir speichern:
- ElCom-Rohantwort als JSON.
- ElCom-Metadaten als JSON, einschliesslich SPARQL-Abfrage.
- BFS-Rohantwort als CSV.
- BFS-Metadaten als JSON.

Die Metadaten dokumentieren unter anderem die Quelle,
den Abrufzeitpunkt, die Auswahlbedingungen und die Zeilenanzahl.
Die Dateinamen enthalten einen Zeitstempel in UTC.

Die gespeicherten Rohdateien bilden den Datenstand unserer
weiteren Analyse. Spätere API-Abrufe können abweichende
Ergebnisse liefern.

## 1.4 Offene Punkte für die Datenaufbereitung

Die Datenerhebung und die ersten Qualitätsprüfungen sind
abgeschlossen. Bisher wurden keine Tarifzeilen ausgeschlossen.

In der Datenaufbereitung prüfen wir:
- die Umwandlung der Tarifwerte in einen numerischen Datentyp,
- die Extraktion der Gemeindenummer aus der ElCom-URI,
- die Behandlung des fehlenden Gesamttarifs,
- die Übereinstimmung der Gemeindenummern beider Quellen,
- nicht zuordenbare Datensätze und mögliche Gemeindemutationen.

ElCom enthält 2’122 unterschiedliche Gemeinde-URIs,
der BFS-Datensatz enthält 2’110 Gemeinden.
Die Ursache dieser Abweichung ist noch nicht abschliessend geklärt.

Die Verknüpfung und ihre Mengenbilanz gehören zu Anforderung 2.

## 1.5 KI-Unterstützung

## 1.5 KI-Unterstützung

Wir verwendeten ChatGPT zur Unterstützung bei der Formulierung
der API-Abfragen, der Erstellung und Erklärung des Python-Codes
sowie der Dokumentation der Arbeitsschritte.

Die Gruppe führte den Code in VS Code aus und kontrollierte
die Ergebnisse auf Zeilenzahlen, fehlende Werte und Dubletten.

Ein konkreter Anwendungsfall war die Behebung eines NameError:
Die Variable elcom_raw war noch nicht definiert. Nach Ausführung
der vorhergehenden Abrufzelle funktionierte die Umwandlung
in eine Tabelle.

Die Unterstützung erleichterte den Einstieg in die Schnittstellen
und das Verständnis des Codes. Gleichzeitig zeigte sich, dass
Codevorschläge allein keine erfolgreiche Ausführung garantieren:
Die Reihenfolge der Notebook-Zellen und die tatsächlichen
Ergebnisse mussten durch die Gruppe geprüft werden.
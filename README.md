# Wohnort und Stromrechnung

Eine Analyse der Haushaltstarife in Schweizer Gemeinden im Rahmen
des Moduls Data Analytics.

## Forschungsfrage

Wie unterscheiden sich die Stromtarife zwischen städtischen,
intermediären und ländlichen Schweizer Gemeinden unter
Berücksichtigung des Kantons?

## Untersuchungsumfang

- Tarifjahr: 2026
- Haushaltsprofil: H4 mit 4’500 kWh Jahresverbrauch
- Produkt: Standardprodukt
- Zielvariable: Tarifvergleichswert in Rp./kWh
- Untersuchungseinheit: Gemeinde
- Gruppierung: Stadt/Land-Typologie 2020
- Gemeindestand: 01.01.2026
- Weitere erklärende Variable: Kanton

Wir untersuchen beschreibende und statistische Zusammenhänge.
Aus den Ergebnissen können keine kausalen Wirkungen des
Gemeindetyps auf den Stromtarif abgeleitet werden.

## Datenquellen

### ElCom

Die Stromtarife werden mit Python über die offizielle
LINDAS-SPARQL-Schnittstelle abgerufen.

- Endpunkt: https://ld.admin.ch/query
- Informationen:
  https://www.elcom.admin.ch/de/tarifdaten-und-visualisierungen

### Bundesamt für Statistik

Die Gemeindedaten enthalten Gemeindenummer, Gemeindename,
Kanton und Stadt/Land-Typologie.

- Datenzugang:
  https://www.agvchapp.bfs.admin.ch/api/communes/levels?date=01-01-2026

Die unveränderten API-Antworten und Angaben zu den Abrufen
werden unter data/raw gespeichert.

## Vorgehen und Projektstand

| Schritt | Status |
|---|---|
| Datenerhebung über offizielle APIs | Umgesetzt |
| Datenaufbereitung und Integration | Umgesetzt |
| Speicherung in SQLite und SQL-Abfragen | Umgesetzt |
| Explorative Datenanalyse | Ausstehend |
| Regression und Modellbewertung | Ausstehend |
| Abschliessende Interpretation und Präsentation | Ausstehend |

Die Daten werden über die BFS-Gemeindenummer verknüpft.
Gemeindeänderungen sind anhand amtlicher Mutationsmeldungen
dokumentiert.

Für den Gemeindevergleich bilden wir zunächst den Mittelwert
der unterschiedlichen Tarifwerte je Gemeinde und Betreiber.
Anschliessend mitteln wir die Betreiberwerte je Gemeinde.
Dadurch erhält jede Gemeinde einen Tarifvergleichswert.

Dieser Wert ist ungewichtet und entspricht keinem beobachteten
durchschnittlich bezahlten Haushaltstarif. Kunden- und
Verbrauchsanteile stehen nicht zur Verfügung.

## Bisherige Datenbasis

Der gespeicherte ElCom-Abruf enthält 2’268 Tarifzeilen.

Nach Harmonisierung der Gemeindenummern, Zusammenfassung
identischer Tarifkombinationen und Ausschluss eines fehlenden
Gesamttarifs verbleiben:

- 2’255 einzelne Tarifwerte,
- 2’108 Gemeinden mit einem Tarifvergleichswert.

Die BFS-Stammdaten enthalten 2’110 Gemeinden.
Für Augst und Nürensdorf liegt im abgefragten Bestand keine
passende Tarifzeile vor.

Diese Angaben beschreiben den Datenbestand.
Sie sind noch keine abschliessenden Ergebnisse zur Forschungsfrage.

## Projektstruktur

| Pfad | Inhalt |
|---|---|
| notebooks/ | Ausführbare Jupyter-Notebooks mit Erklärungen |
| data/raw/ | Unveränderte Rohdaten und Abrufmetadaten |
| data/processed/ | Aufbereitete Daten und Bereinigungsnachweise |
| data/stromtarife.sqlite | SQLite-Datenbank |
| sql/ | Gespeicherte SQL-Abfragen |
| results/sql/ | Ergebnisse der SQL-Auswertungen |
| docs/ | Ausführliche Dokumentation der Arbeitsschritte |

## Ausführung in VS Code

### Voraussetzungen

- Python 3
- VS Code mit den Erweiterungen Python und Jupyter
- Python-Bibliotheken requests und pandas

Die benötigten Bibliotheken können in einer Notebook-Codezelle
installiert werden:

```python
%pip install requests pandas
```

sqlite3 sowie die verwendeten Hilfsmittel für Dateipfade und
JSON-Verarbeitung gehören zur Python-Standardbibliothek.

### Reihenfolge der Notebooks

1. notebooks/01_datenerhebung.ipynb
2. notebooks/02_datenaufbereitung.ipynb
3. notebooks/03_datenbank.ipynb

Das Repository als Projektordner in VS Code öffnen.
Im jeweiligen Notebook den Python-Kernel auswählen und
die Zellen von oben nach unten ausführen.

Notebook 1 ruft die offiziellen Schnittstellen ab und benötigt
Internetzugang. Jeder erneute Abruf erstellt Dateien mit
einem neuen Zeitstempel.

Notebook 2 verarbeitet die gespeicherten Rohdateien.
Bei mehreren vorhandenen Abrufen muss der gewünschte
Datenstand bewusst ausgewählt werden.

Notebook 3 erstellt die Datenbank aus den aufbereiteten CSV-Dateien.
Beim erneuten Ausführen werden die drei Datenbanktabellen ersetzt.

## Dokumentation

1. [Datenerhebung](docs/01_datenerhebung.md)
2. [Datenaufbereitung und Integration](docs/02_datenaufbereitung.md)
3. [SQLite-Datenbank und SQL-Abfragen](docs/03_datenbank.md)

## KI-Unterstützung

ChatGPT wurde unterstützend für Codevorschläge,
Erklärungen, Fehlerbehebung und Dokumentation verwendet.

Die konkrete Verwendung, die durchgeführten Kontrollen
und die festgestellten Grenzen sind in den jeweiligen
Dokumentationsdateien beschrieben.

## Projektteam

Die Namen aller Gruppenmitglieder werden hier vor der Abgabe ergänzt.
# Map: household electricity tariffs 2026 by municipality

- Notebook: `05_map.ipynb` (run it from this folder)
- Output: `map_tariffs_2026.png` (used on slide 3 of the concept presentation)
- Tariffs: `data/processed/municipality_values.csv`, H4 2026, Rp./kWh excl. VAT
- Boundaries: generalised municipality boundaries 2026, Bundesamt für Statistik (BFS), GEOSTAT,
  taken from the npm package swiss-maps 4.7.0 (https://www.npmjs.com/package/swiss-maps)
- Join: BFS municipality number; 2,108 of 2,113 areas have a tariff, 5 are shown in grey
- The boundary files are downloaded automatically into `maps/geodata/` and are not committed.

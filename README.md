# Web-Scraper für Chronik von antisemitischen Vorfällen veröffentlicht von der Amadeu Antonio Stiftung 

September 2020, Markus Konrad <markus.konrad@wzb.eu> / [Wissenschaftszentrum Berlin für Sozialforschung](https://www.wzb.eu/en)


## Beschreibung

Lädt sämtliche Einträge, welche von [Amadeu Antonio Stiftung (AAS)](https://www.amadeu-antonio-stiftung.de/) unter
https://www.amadeu-antonio-stiftung.de/chronik/ veröffentlicht wurden, herunter und speichert diese als strukturierten
Datensatz in der CSV-Datei `collected_data.csv` ab. Der Datensatz in dieser Datei enthält folgende Spalten:

- `url`: URL zum vollständigen Eintrag
- `title`: Titel des Eintrags
- `author`: Autor des Eintrags (falls angegeben)
- `author_url`: Link zum Autor des Eintrags (falls angegeben)
- `date`: Veröffentlichungsdatum (ISO 8601 Format)
- `location`: Ortsverweis (falls angegeben) 
- `text`: Vollständiger Text des Eintrags
- `sources_urls`: Links zu Quellenangaben (falls mehrere Quellen sind diese mit ";" getrennt)
- `sources_texts`: Titel der Quellenangaben analog zu `sources_urls`

**Der Webscraper wurde am 2. September 2020 programmiert. Änderungen der Webseite nach diesem Datum können den Scraper
unbenutzbar machen bzw. Änderungen am Skript erfordern.** 


## Installation

- benötigt Python 3
- Installation von Python Paketen aus `requirements.txt` via pip: `pip install -r requirements.txt`


## Nutzung

- eventuell `MAX_PAGES` in `aas_chronik_scraper.py` setzen, um nur die ersten *N* Seiten zu laden
- ausführen des Skripts bspw. via `python3 aas_chronik_scraper.py`
- erneutes Ausführen des Skripts lädt schon vorhandene Daten aus `rawdata` und `collected_data.csv` – sollen die Daten
  also "frisch" geladen werden, sollten die Dateien in `rawdata` sowie `collected_data.csv` gelöscht werden


## Lizenz / License


Lizenziert unter [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). Siehe `LICENSE.txt`-Datei.

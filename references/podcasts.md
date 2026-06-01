# Podcasts

Quelle der ursprünglichen Sammlung:

- Google Sheet: <https://docs.google.com/spreadsheets/d/16EGIIIXWbNr8DwaGZWbUqnYHg_LgpgM7NECzTbUWgW4/edit?gid=0#gid=0>

Diese Referenz ist ein eingebetteter Snapshot der im Skill gepflegten Podcast-Aliasse.

## Verwendung

Ein Agent kann einen Podcast auf zwei Arten angeben:

1. über einen bekannten Alias aus dieser Liste
2. über eine direkte `http(s)`-RSS-Feed-URL

Beispiele:

```bash
python3 scripts/tonie_sync.py assign --tonie benjamin-kreativ --podcast pumuckl
python3 scripts/tonie_sync.py assign --tonie benjamin-kreativ --podcast https://example.org/feed.xml
```

## Häufige Aliasse

- `maus` -> Sendung mit der Maus - zum Hören
- `maus-live` -> Sendung mit der Maus - live
- `maus-gute-nacht` -> Gute Nacht mit der Maus
- `checker-tobi` -> Checker Tobi Podcast
- `pumuckl` -> Pumuckl
- `lachlabor` -> Das Lachlabor Podcast
- `ohrenbaer` -> Ohrenbär-Podcast
- `kakadu` -> Kakadu
- `mikado` -> Mikado - der Kinder-Podcast (NDR)
- `unser-sandmaennchen` -> Unser Sandmännchen

## Eingebettete Podcast-Tabelle

| Alias | Podcast | Feed | Hinweise |
|---|---|---|---|
| maus | Sendung mit der Maus - zum Hören | https://www1.wdr.de/mediathek/podcast/podcast-die-maus-100.podcast | |
| maus-live | Sendung mit der Maus - live | wdr-diemaus-live.icecastssl.wdr.de/wdr/diemaus/live/mp3/128/stream.mp3 | Live-Stream |
| pumuckl | Pumuckl | https://feeds.br.de/pumuckl/feed.xml | |
| checker-tobi | Checker Tobi Podcast | https://feeds.br.de/checkpod-der-podcast-mit-checker-tobi/feed.xml | |
| anna-und-die-wilden-tiere | Anna und die wilden Tiere | https://feeds.br.de/anna-und-die-wilden-tiere/feed.xml | |
| geschichten-fuer-kinder-br | Geschichten für Kinder BR | https://feeds.br.de/geschichten-fuer-kinder/feed.xml | |
| maus-gute-nacht | Gute Nacht mit der Maus | https://kinder.wdr.de/radio/diemaus/audio/gute-nacht-mit-der-maus/diemaus-gute-nacht-104.podcast | Gute Einschlafwahl |
| betthupferl | Betthupferl - Gute-Nacht-Geschichten für Kinder BR | https://feeds.br.de/betthupferl/feed.xml | |
| tigerenten-club | Tigerenten Club | https://www.kindernetz.de/~podcast/sendungen/hoerspielshow/podcast-hoerspielshow-100.xml | letzter bekannter Eintrag 2024-05-10 |
| lachlabor | Das Lachlabor Podcast | https://feeds.br.de/lachlabor/feed.xml | |
| figarinos-fahrradladen | figarinos Fahrradladen | https://www.mdr.de/tweens/podcast/figarino/fahrradladen102-podcast.xml | |
| was-ist-was | "Was ist was" der Podcast | https://feeds.megaphone.fm/KBBF5520541713 | letzter bekannter Eintrag 2024-06-27 |
| geolino-spezial | Geolino spezial | https://proxyfeed.svmaudio.com/aa/geolino-spezial | |
| eric-erforscht | Eric erforscht | https://ericerforscht.libsyn.com/rss | |
| erlebnis-erde | Erlebnis Erde | https://www1.wdr.de/mediathek/audio/wdr/erlebnis-erde/erlebnis-erde-110.podcast | |
| das-geheimnis | Das Geheimnis - Musikalische Rätsel und Krimis zum Mitraten | https://feeds.br.de/do-re-mikro-die-musiksendung-fuer-kinder/feed.xml | |
| quatsch-weisheit | Quatsch & Weisheit: Kinder reden. Über die Welt | https://feeds.br.de/quatsch-weisheit-kinder-reden-ueber-die-welt-und-ueberhaupt/feed.xml | |
| soko-kinderkrimi | Soko Kinderkrimi | https://cdn.stationista.com/feeds/soko-kinderkrimi | |
| ohrenbaer | Ohrenbär-Podcast | https://www.ohrenbaer.de/podcast/podcast.feed.podcast.xml | |
| mikado | Mikado - der Kinder-Podcast (NDR) | https://www.ndr.de/nachrichten/info/sendungen/mikado/mikado_am_morgen/podcast4223.xml | |
| kakadu | Kakadu - Ein Kinderpodcast von Deutschlandfunk Kultur mit Geschichten, Rätseln und Wissenswertem für Kinder. | https://www.kakadu.de/kakadu-104.xml | |
| unser-sandmaennchen | Unser Sandmännchen | https://www.antennebrandenburg.de/programm/hoeren/podcasts/Zappelduster_Podcast/podcast.xml/feed=podcast.xml | |
| weisst-du-schon | Weißt du's schon? – Das Quiz für Kids | https://weisstdusschon.podigee.io/feed/mp3 | |
| flipsi-findets-raus | Flipsi findet's raus – auf Expedition durch den Körper | https://flipsi-findets-raus.podigee.io/feed/mp3 | |

## Hinweise

- `maus` steht für **Sendung mit der Maus - zum Hören**.
- `maus-gute-nacht` ist oft eine gute Wahl für Einschlaf-Tonies.
- Zusätzlich zu diesen Aliassen können direkte RSS-Feed-URLs verwendet werden.

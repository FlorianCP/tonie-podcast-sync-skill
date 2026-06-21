# `tonies.toml`

Die lokale Skill-Konfiguration lebt standardmäßig unter:

- `~/.config/tonie-podcast-sync-skill/tonies.toml`

Optional kann ein anderer Pfad gesetzt werden über:

- `TONIE_SYNC_SKILL_CONFIG=/pfad/zur/tonies.toml`

## Ziel

Diese Datei beschreibt die *haushaltsspezifischen* Tonies und deren gewünschte Inhaltsquelle.

Der Skill übernimmt daraus die Defaults und schreibt sie in die `settings.toml` des Upstream-Projekts.

## Grundregel

Jeder `[tonies.<slug>]`-Eintrag braucht:

- `id`
- `name`
- optional `aliases`
- **genau eine** Quelle:
  - `podcast`
  - `audio_folder`
  - `audio_files`

Die Quellen sind gegenseitig exklusiv.

## Podcast-Quelle

```toml
[tonies.abend]
id = "..."
name = "Abend-Tonie"
podcast = "https://example.com/feed.xml"
episode_sorting = "random"
maximum_length = 60
wipe = true
```

Hinweise:

- `podcast` soll direkt die Feed-URL enthalten.
- Beim CLI-Befehl `assign --podcast pumuckl` darf weiterhin ein Katalog-Alias verwendet werden; der Skill löst ihn dann in die echte Feed-URL auf und persistiert diese.
- `excluded_title_strings` und `pinned_episode_names` sind nur für Podcast-Quellen sinnvoll.

## Lokaler Ordner als Quelle

```toml
[tonies.schlaflieder]
id = "..."
name = "Schlaflieder"
audio_folder = "/Users/flo/Audio/Schlaflieder"
episode_sorting = "alphabetical"
maximum_length = 45
wipe = false
```

Hinweise:

- Der Ordnerpfad wird mit `~`-Expansion gespeichert.
- Sinnvolle Sortierungen für lokale Audioquellen sind:
  - `alphabetical`
  - `manual` (vor allem bei `audio_files`)

## Explizite Dateiliste als Quelle

```toml
[tonies.favoriten]
id = "..."
name = "Favoriten"
audio_files = [
  "/Users/flo/Audio/01-intro.mp3",
  "/Users/flo/Audio/02-geschichte.mp3",
]
episode_sorting = "manual"
maximum_length = 35
wipe = true
```

Hinweise:

- Reihenfolge der Liste bleibt erhalten.
- `manual` ist hier meist die beste Wahl.

## Unterstützte Felder

Pflicht:

- `id`: Tonie-ID aus Tonie Cloud
- `name`: Menschlich lesbarer Name

Optional:

- `aliases`: Zusätzliche Bezeichner für `assign --tonie ...`
- `podcast`: RSS-Feed-URL
- `audio_folder`: Lokaler Ordner mit Audiodateien
- `audio_files`: Explizite Liste lokaler Audiodateien
- `episode_sorting`: `by_date_newest_first`, `by_date_oldest_first`, `random`, `alphabetical`, `manual`
- `maximum_length`: Maximale Gesamtdauer in Minuten
- `episode_min_duration_sec`: Mindestdauer pro Track
- `episode_max_duration_sec`: Maximaldauer pro Track
- `volume_adjustment`: Lautstärkeanpassung
- `excluded_title_strings`: Nur für Podcasts
- `pinned_episode_names`: Nur für Podcasts
- `wipe`: Vor dem Upload leeren oder nicht

## Legacy-Kompatibilität

Ältere Skill-Konfigurationen mit:

```toml
default_podcast = "pumuckl"
```

werden weiterhin gelesen. Der Skill wandelt das intern in die passende Feed-URL um.

Für neue Einträge soll aber direkt `podcast = "https://..."` verwendet werden.

## Wichtige Trennung

- `tonies.toml` = Wunschzustand des Haushalts
- `~/.toniepodcastsync/settings.toml` = operative Upstream-Konfiguration
- `~/.toniepodcastsync/.secrets.toml` = Zugangsdaten

`tonies.toml` gehört nicht mit echten IDs ins öffentliche Repo.
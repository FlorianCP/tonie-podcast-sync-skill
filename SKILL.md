---
name: tonie-podcast-sync
summary: Richte tonie-podcast-sync lokal ein, verwalte Kreativ-Tonies über tonies.toml und synchronisiere Podcasts oder lokale Audiodateien auf Tonieboxen.
---

# tonie-podcast-sync

Nutze diesen Skill, wenn ein Kreativ-Tonie mit Podcast-Folgen oder lokalen Audiodateien befüllt, repariert oder neu zugeordnet werden soll.

## Was dieser Skill kann

- lokales `tonie-podcast-sync`-Setup aufbauen
- vorhandene Tonie-Zugangsdaten in `.secrets.toml` bootstrapen
- Kreativ-Tonies entdecken
- eine lokale `tonies.toml` als Wunschzustand pflegen
- Podcasts, Audio-Ordner oder explizite Audio-Dateien pro Tonie zuweisen
- einzelne oder alle Tonies synchronisieren
- lokale Installation und Config mit `doctor` prüfen

## Wichtige lokale Pfade

- Skill-Repo: `/Users/flo/Projects/agent-skills/tonie-podcast-sync-skill`
- Upstream-Arbeitskopie: `~/.local/share/tonie-podcast-sync`
- Skill-Konfiguration: `~/.config/tonie-podcast-sync-skill/tonies.toml`
- Operative Settings: `~/.toniepodcastsync/settings.toml`
- Secrets: `~/.toniepodcastsync/.secrets.toml`

## Aktueller Sonderfall: harter Fork/Branch

Bis die lokalen Audio-Erweiterungen upstream integriert sind, muss dieser Skill absichtlich Florians Fork und Branch verwenden:

- Primäres Repo: `git@github.com:FlorianCP/tonie-podcast-sync.git`
- HTTPS-Fallback: `https://github.com/FlorianCP/tonie-podcast-sync.git`
- Branch: `feature/local-mp3-sync`

`setup-local` stellt genau diesen Stand her. Der Skill versucht zuerst SSH und fällt bei fehlendem GitHub-SSH-Zugriff automatisch auf HTTPS zurück. Nicht stillschweigend auf PyPI oder das alte Upstream-Repo zurückfallen.

## Regeln

1. Erst `doctor` oder Dateistand prüfen, dann ändern.
2. Keine echten IDs oder Secrets ins Repository schreiben.
3. In `tonies.toml` pro Tonie **genau eine** Quelle verwenden:
   - `podcast`
   - `audio_folder`
   - `audio_files`
4. Podcast-Katalog behalten und für Alias-Auflösung nutzen.
5. Die operative `settings.toml` soll das Upstream-nahe Schema enthalten, nicht eine zweite proprietäre Skill-Sonderlogik.

## Standardablauf

### 1. Diagnose

Führe zuerst aus:

```bash
python3 scripts/tonie_sync.py doctor
```

Wenn das Setup fehlt, richte es ein.

### 2. Lokales Projekt einrichten

```bash
python3 scripts/tonie_sync.py setup-local
```

Das Kommando soll:

- das erwartete Repo klonen oder aktualisieren
- den erwarteten Branch auschecken
- eine lokale venv anlegen
- das Projekt editable installieren

### 3. Secrets bootstrapen

```bash
python3 scripts/tonie_sync.py bootstrap-secrets
```

Der Skill sucht Zugangsdaten in:

- `~/.env`
- `~/.hermes/.env`
- `~/.openclaw/.env`
- oder explizit `TONIE_SYNC_SKILL_ENV_FILE`

### 4. Lokale Wunschkonfiguration anlegen

Falls noch nicht vorhanden:

```bash
python3 scripts/tonie_sync.py init-config
```

Dann `~/.config/tonie-podcast-sync-skill/tonies.toml` mit echten lokalen Werten befüllen.

### 5. Tonies entdecken

```bash
python3 scripts/tonie_sync.py discover-tonies
```

### 6. Defaults und Zuordnungen prüfen

```bash
python3 scripts/tonie_sync.py show-config
```

## Zuordnungen

### Podcast

```bash
python3 scripts/tonie_sync.py assign --tonie benjamin --podcast pumuckl
```

Oder direkte Feed-URL:

```bash
python3 scripts/tonie_sync.py assign --tonie benjamin --podcast https://example.com/feed.xml
```

### Lokaler Audio-Ordner

```bash
python3 scripts/tonie_sync.py assign --tonie schlaflieder --audio-folder ~/Audio/Schlaflieder --episode-sorting alphabetical
```

### Explizite Dateiliste

```bash
python3 scripts/tonie_sync.py assign \
  --tonie favoriten \
  --audio-file ~/Audio/01-intro.mp3 \
  --audio-file ~/Audio/02-geschichte.mp3 \
  --episode-sorting manual
```

### Sofort zuweisen und synchronisieren

```bash
python3 scripts/tonie_sync.py assign-and-sync --tonie benjamin --podcast maus-gute-nacht
```

## Synchronisieren

Alle:

```bash
python3 scripts/tonie_sync.py sync --tonie all
```

Einzelnen Tonie:

```bash
python3 scripts/tonie_sync.py sync --tonie benjamin
```

## Wichtige Felder

Für alle Quellen möglich:

- `episode_sorting`
- `maximum_length`
- `episode_min_duration_sec`
- `episode_max_duration_sec`
- `volume_adjustment`
- `wipe`

Nur für Podcasts sinnvoll:

- `excluded_title_strings`
- `pinned_episode_names`

Empfohlene Sortierungen:

- Podcasts: `by_date_newest_first`, `by_date_oldest_first`, `random`
- Lokale Dateien: `alphabetical`, `manual`

## Doctor-Interpretation

`doctor` soll mindestens sichtbar machen:

- Skill-Pfad
- Projektordner/Venv/CLI vorhanden oder nicht
- Settings/Secrets/Tonie-Config vorhanden oder nicht
- ob Credentials gefunden werden
- erwartetes Repo und erwarteter Branch
- tatsächlicher Git-Remote, Branch, Commit und Dirty-Status
- ob die lokale CLI `sync-local-files` unterstützt
- welche Quellen aktuell in `tonies.toml` konfiguriert sind

## Legacy-Kompatibilität

Wenn in älteren lokalen Dateien noch `default_podcast = "pumuckl"` steht, darf der Skill das noch lesen. Für neue Einträge aber direkt `podcast = "https://..."` verwenden.

## Wenn etwas schiefgeht

1. `doctor` ausführen
2. `show-config` prüfen
3. prüfen, ob `~/.local/share/tonie-podcast-sync` wirklich auf Florians Fork/Branch steht
4. prüfen, ob `settings.toml` die erwartete Quelle enthält (`podcast`, `audio_folder` oder `audio_files`)
5. bei lokalen Audiodateien nach dem Sync den echten Cloud-Zustand prüfen (nicht nur die Erfolgszeile vertrauen): `tonie-podcast-sync list-tonies` oder direkt Kapitelzahl/Kapitelnamen per Python prüfen
6. erst dann erneut synchronisieren

## Bekannte Falle: lange lokale Dateititel

Bei lokalen Audiodateien kann ein zu langer Kapitelname in der Tonie-Cloud stillschweigend scheitern. Praktisch relevant:

- für lokale MP3s wird der Kapitelname bevorzugt aus dem ID3-Tag `TIT2` gelesen, **nicht** aus dem Dateinamen
- die Tonie-API-Library meldet fehlgeschlagene `add_chapter`-Aufrufe derzeit nicht sauber nach oben; die CLI kann also `Successfully uploaded` ausgeben, obwohl ein Kapitel am Tonie fehlt
- Symptom: nach einem Sync mit mehreren lokalen Dateien ist nur der letzte/kurze Track auf dem Tonie sichtbar

Workaround:

1. den problematischen MP3-Track in eine lokale Kopie mit **kurzem** `title`-Metadatum umschreiben, z. B. per `ffmpeg -c:a copy -metadata title='Kurzer Titel'`
2. diese vorbereitete Datei statt der Originaldatei synchronisieren
3. danach per Kapitelzahl/Kapitelnamen verifizieren, dass wirklich alle gewünschten Tracks vorhanden sind

Lange Titel sind nur eine mögliche Ursache: Ein Kapitel kann auch trotz kurzem, zuvor funktionierendem Titel fehlen.

Wenn nur das letzte Kapitel fehlt und alle vorherigen Kapitel korrekt, vollständig verarbeitet und in der richtigen Reihenfolge vorhanden sind:

1. nicht sofort alles wipen und neu hochladen
2. den Tonie per ID frisch abrufen und prüfen, dass die vorhandenen Kapitel exakt dem erwarteten Anfang der Liste entsprechen
3. nur die fehlende Datei anhängen, z. B. per `tps._api.upload_file_to_tonie(tonie, pfad, titel)`
4. danach mit einem frischen Client erneut Kapitelzahl, Reihenfolge und verarbeitete Dauer (`seconds > 0`) prüfen

## Verwandte Referenzen

- `README.md`
- `references/tonies.md`
- `references/tonies.example.toml`
- `references/podcasts.md`
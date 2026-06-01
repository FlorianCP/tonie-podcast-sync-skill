---
name: tonie-podcast-sync
description: Use when a user wants an agent to set up or operate a local tonie-podcast-sync workflow for Kreativ-Tonies: check prerequisites, install the upstream tool locally, discover creative tonie IDs, maintain a local tonies.toml with household-specific names and aliases, assign podcasts from the built-in German catalog or a direct RSS feed URL, and sync one or more configured Tonies.
version: 1.0.0
author: FlorianCP / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [toniebox, tonies, podcast, rss, audio, family, automation]
    related_skills: []
---

# Tonie Podcast Sync

## Overview

Dieser Skill hilft einem KI-Agenten dabei, ein lokales Setup auf Basis von `tonie-podcast-sync` zu prüfen, einzurichten und zu bedienen.

Der Skill shippt **keine** echten Tonie-IDs und **keine** Zugangsdaten. Stattdessen arbeitet er mit:

- Umgebungsvariablen für Tonie-Cloud-Zugangsdaten
- einer lokalen `tonies.toml` pro Haushalt
- einer lokalen Installation des Upstream-Projekts
- einem eingebauten deutschsprachigen Podcast-Katalog
- optional direkten RSS-Feed-URLs

## When to Use

Nutze diesen Skill, wenn der Nutzer zum Beispiel sagt:

- "Richte meine Kreativ-Tonies mit Podcasts ein"
- "Finde heraus, welche Kreativ-Tonies auf meinem Konto sind"
- "Lege Pumuckl auf Benjamins Kreativ-Tonie"
- "Synchronisiere neue Folgen auf alle Tonies"
- "Hilf mir, die Tonie-IDs sauber in einer lokalen Mapping-Datei zu pflegen"

Nicht verwenden für:

- normale Tonies ohne Kreativ-Tonie-Workflow
- direkte Cloud- oder API-Integrationen außerhalb des Upstream-Projekts
- Fälle, in denen echte Haushaltsdaten ins Repository geschrieben werden sollen

## Resources

- Operatives Skript: `scripts/tonie_sync.py`
- Tonie-Discovery und lokale Zuordnung: `references/tonies.md`
- Beispielkonfiguration: `references/tonies.example.toml`
- Podcast-Katalog: `references/podcasts.md`
- README für Menschen: `README.md`

## Operating Principles

- **Nie Tonie-IDs raten.** Immer echte Discovery verwenden.
- **Keine privaten Haushaltsdaten ins Repository schreiben.**
- **Erst prüfen, dann einrichten, dann syncen.**
- **Namen und Aliasse gehören in die lokale `tonies.toml`.**
- **Secrets nur lokal aus Env/Env-Datei übernehmen.**
- **Wenn ein Podcast-Alias nicht passt, ist eine direkte RSS-URL erlaubt.**

## Local Paths and Defaults

Standardpfade:

- Upstream-Projekt: `~/.local/share/tonie-podcast-sync`
- lokale Tonie-Zuordnung: `~/.config/tonie-podcast-sync-skill/tonies.toml`
- Upstream-Settings: `~/.toniepodcastsync/settings.toml`
- Upstream-Secrets: `~/.toniepodcastsync/.secrets.toml`

Override-Variablen:

- `TONIE_PODCAST_SYNC_PROJECT_DIR`
- `TONIE_SYNC_SKILL_CONFIG`
- `TONIE_PODCAST_SYNC_SETTINGS_DIR`
- `TONIE_SYNC_SKILL_ENV_FILE`

## Credentials

Unterstützte Zugangsdaten-Paare:

- `TPS_TONIE_CLOUD_ACCESS_USERNAME` + `TPS_TONIE_CLOUD_ACCESS_PASSWORD`
- `TONIE_CLOUD_ACCESS_USERNAME` + `TONIE_CLOUD_ACCESS_PASSWORD`
- `TONIE_CLOUD_USERNAME` + `TONIE_CLOUD_PASSWORD`
- `TONIE_USERNAME` + `TONIE_PASSWORD`

Wenn `TONIE_SYNC_SKILL_ENV_FILE` gesetzt ist, wird **nur diese Datei** durchsucht.

Wenn `TONIE_SYNC_SKILL_ENV_FILE` **nicht** gesetzt ist, sucht der Skill in:

- `~/.env`
- `~/.hermes/.env`
- `~/.openclaw/.env`

## Recommended Workflow

### 1) Diagnose zuerst

```bash
python3 scripts/tonie_sync.py doctor
```

Wenn etwas fehlt, benenne die fehlenden Teile konkret:

- Projektordner
- Venv
- CLI
- Settings
- Secrets
- lokale Tonie-Konfiguration
- Env-Zugangsdaten

### 2) Upstream lokal einrichten, falls nötig

```bash
python3 scripts/tonie_sync.py setup-local --python python3
```

Das installiert das Upstream-Projekt standardmäßig nach:

```text
~/.local/share/tonie-podcast-sync
```

### 3) Secrets aus Env übernehmen

```bash
python3 scripts/tonie_sync.py bootstrap-secrets
```

Wenn keine passenden Variablen gefunden werden, erkläre dem Nutzer klar:

- welche Variablenpaare unterstützt werden
- welche Env-Dateien durchsucht wurden
- dass Zugangsdaten lokal gesetzt werden müssen, bevor Discovery oder Sync funktionieren

### 4) Starter-Datei für die lokale Tonie-Zuordnung erzeugen

```bash
python3 scripts/tonie_sync.py init-config
```

Die erzeugte Datei ist ein anonymes Template. Der Agent muss danach die echten Tonies des Haushalts eintragen.

### 5) Echte Kreativ-Tonies finden

```bash
python3 scripts/tonie_sync.py discover-tonies
```

Diese Discovery soll die Upstream-CLI durchreichen. Nicht heuristisch aus alten Dateien ableiten.

### 6) Lokale `tonies.toml` befüllen

Jetzt wird die eigentliche Haushaltszuordnung gepflegt.

Für jeden Kreativ-Tonie sollen typischerweise eingetragen werden:

- `id` – echte Kreativ-Tonie-ID aus der Discovery
- `name` – sprechender Anzeigename, z. B. `Benjamins Kreativ-Tonie`
- `aliases` – natürliche Alternativnamen, z. B. `benjamin`, `schlaf tonie`, `blauer tonie`
- `default_podcast` – optionaler Katalog-Alias
- weitere Sync-Optionen bei Bedarf

Wichtig:

- Die **Section** wie `tonies.benjamin-kreativ` ist der kanonische interne Slug.
- `name` ist der lesbare Anzeigename.
- `aliases` sind die Wörter, mit denen der Nutzer den Tonie wahrscheinlich erwähnt.
- Der Agent darf diese Datei lokal schreiben oder ergänzen, aber nicht ins Repository committen.

Siehe dazu:

- `references/tonies.md`
- `references/tonies.example.toml`

### 7) Podcasts zuweisen

Bekannten Katalog-Alias verwenden:

```bash
python3 scripts/tonie_sync.py assign --tonie benjamin-kreativ --podcast pumuckl
```

Direkte RSS-URL verwenden:

```bash
python3 scripts/tonie_sync.py assign --tonie benjamin-kreativ --podcast https://example.org/feed.xml
```

### 8) Zuweisen und sofort synchronisieren

```bash
python3 scripts/tonie_sync.py assign-and-sync --tonie benjamin-kreativ --podcast maus-gute-nacht
```

### 9) Bereits konfigurierte Tonies synchronisieren

Ein Tonie:

```bash
python3 scripts/tonie_sync.py sync --tonie benjamin-kreativ
```

Alle Tonies:

```bash
python3 scripts/tonie_sync.py sync --tonie all
```

### 10) Aktuellen Stand prüfen

```bash
python3 scripts/tonie_sync.py list-tonies
python3 scripts/tonie_sync.py list-podcasts
python3 scripts/tonie_sync.py show-config
```

## Intent Mapping

- "Welche Kreativ-Tonies gibt es auf dem Konto?" → `discover-tonies`
- "Mach bitte eine Starter-Datei für die Tonies" → `init-config`
- "Trag Benjamins Tonie mit seiner ID ein" → lokale `tonies.toml` editieren
- "Was kann ich auf den Tonie legen?" → `list-podcasts` oder `references/podcasts.md`
- "Nimm statt Katalog bitte diesen Feed" → `assign --podcast <https://...>`
- "Sync alles" → `sync --tonie all`

## Common Pitfalls

1. **Tonie-IDs geraten statt entdeckt**
   - Immer zuerst `discover-tonies`.

2. **Haushaltsdaten ins Repo schreiben**
   - Echte IDs, Namen und Aliasse gehören nur in die lokale `tonies.toml`.

3. **Secrets im Repo oder in Commit-Historie speichern**
   - Secrets nur lokal über Env oder Env-Datei.

4. **Discovery-Ergebnis nicht in sprechende Namen übersetzen**
   - Die rohe ID allein ist für den Nutzer unpraktisch. Immer `name` und `aliases` sinnvoll pflegen.

5. **Alias mit Feed-URL verwechseln**
   - Katalog-Alias oder direkte `http(s)`-RSS-URL verwenden. Wenn ein Alias unbekannt ist, `list-podcasts` prüfen.

6. **Sync ohne funktionierendes Upstream-Setup starten**
   - Erst `doctor`, dann `setup-local`/`bootstrap-secrets`, erst danach synchronisieren.

## Response Behavior

Nach erfolgreicher Arbeit soll der Agent knapp, aber konkret sagen:

- welcher Tonie betroffen war
- unter welchem Namen/Alias er lokal geführt wird
- welcher Podcast oder welche Feed-URL jetzt gilt
- ob nur die Zuordnung geändert wurde oder auch ein Sync lief

Wenn Sync technisch erfolgreich war, kurz erwähnen, dass die Toniebox die Inhalte noch aus der Tonie-Cloud ziehen muss.

## Verification Checklist

- [ ] `doctor` wurde ausgeführt
- [ ] Upstream-Projekt ist vorhanden oder installiert
- [ ] Zugangsdaten wurden lokal gefunden oder klar als fehlend benannt
- [ ] `discover-tonies` wurde genutzt, keine IDs geraten
- [ ] lokale `tonies.toml` enthält sinnvolle `name`- und `aliases`-Einträge
- [ ] keine Haushaltsdaten wurden ins Repository geschrieben
- [ ] Podcast-Zuordnung verwendet Katalog-Alias oder direkte RSS-URL
- [ ] Sync wurde nur nach erfolgreichem Setup ausgeführt

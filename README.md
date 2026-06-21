# tonie-podcast-sync-skill

Ein Skill-Repository für Hermes/OpenClaw-artige Agenten, das das Python-Projekt `tonie-podcast-sync` lokal einrichtet und eine haushaltsspezifische Tonie-Zuordnung verwaltet.

Der Skill unterstützt jetzt drei Quelltypen pro Kreativ-Tonie:

- Podcasts / RSS-Feeds
- lokale Audio-Ordner
- explizite lokale Dateilisten

Der bestehende Podcast-Katalog bleibt erhalten und kann weiterhin über Aliase wie `pumuckl` oder `maus-gute-nacht` verwendet werden.

## Aktueller Setup-Modus

Bis die lokalen Audio-Erweiterungen upstream gemerged und released sind, arbeitet dieser Skill absichtlich gegen Florians Fork und einen fest verdrahteten Branch:

- Primäres Repo: `git@github.com:FlorianCP/tonie-podcast-sync.git`
- HTTPS-Fallback: `https://github.com/FlorianCP/tonie-podcast-sync.git`
- Branch: `feature/local-mp3-sync`

`setup-local` richtet genau diesen Checkout ein und installiert ihn editable (`pip install -e .`). Der Ablauf versucht zuerst SSH und fällt bei fehlendem GitHub-SSH-Zugriff automatisch auf HTTPS zurück. Es wird bewusst nicht auf PyPI oder das ursprüngliche Upstream-Repo zurückgefallen.

## Wichtige Dateien

- `SKILL.md` — operative Skill-Anleitung für Agenten
- `scripts/tonie_sync.py` — Helper-CLI für Setup, Config und Sync
- `references/tonies.example.toml` — anonymes Beispiel für die lokale Tonie-Konfiguration
- `references/tonies.md` — Referenz zur `tonies.toml`
- `references/podcasts.md` — Hintergrund zum Podcast-Katalog

## Typischer Ablauf

### 1. Lokales Upstream-Projekt einrichten

```bash
python3 scripts/tonie_sync.py setup-local
```

### 2. Secrets aus vorhandenen Env-Dateien bootstrapen

```bash
python3 scripts/tonie_sync.py bootstrap-secrets
```

### 3. Beispiel-Konfiguration anlegen

```bash
python3 scripts/tonie_sync.py init-config
```

### 4. Kreativ-Tonies entdecken

```bash
python3 scripts/tonie_sync.py discover-tonies
```

### 5. Tonie-Defaults prüfen

```bash
python3 scripts/tonie_sync.py show-config
```

## Beispiele

Podcast zuweisen:

```bash
python3 scripts/tonie_sync.py assign --tonie benjamin --podcast pumuckl
```

Lokalen Ordner zuweisen:

```bash
python3 scripts/tonie_sync.py assign --tonie schlaflieder --audio-folder ~/Audio/Schlaflieder --episode-sorting alphabetical
```

Explizite Dateiliste zuweisen und sofort synchronisieren:

```bash
python3 scripts/tonie_sync.py assign-and-sync \
  --tonie favoriten \
  --audio-file ~/Audio/01-intro.mp3 \
  --audio-file ~/Audio/02-geschichte.mp3 \
  --episode-sorting manual
```

Alle konfigurierten Tonies synchronisieren:

```bash
python3 scripts/tonie_sync.py sync --tonie all
```

## Doctor

```bash
python3 scripts/tonie_sync.py doctor
```

`doctor` prüft jetzt zusätzlich:

- ob das erwartete Repo/der erwartete Branch verwendet wird
- ob die lokale CLI `sync-local-files` kennt
- welche Quellen in der lokalen `tonies.toml` konfiguriert sind

## Konfigurationsmodell

Der Skill persistiert die gewählte Quelle direkt in die operative `settings.toml` des Upstream-Projekts.

Beispiele:

- `podcast = "https://..."`
- `audio_folder = "/Users/flo/..."`
- `audio_files = ["/Users/flo/...", ...]`

Damit bleibt das Skill-Modell nah am Upstream-Schema und vermeidet doppelte Sonderlogik.

## Sicherheit

- Keine echten Tonie-IDs ins Repo committen
- Keine Zugangsdaten ins Repo committen
- `tonies.toml` lokal halten
- `.secrets.toml` lokal halten

## Lizenz / Haftung

Dieses Repository ist nur eine Skill-Hülle um das separate Projekt `tonie-podcast-sync` und wird ohne Gewähr bereitgestellt.
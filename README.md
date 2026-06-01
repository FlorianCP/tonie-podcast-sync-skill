# tonie-podcast-sync-skill

![MIT License](https://img.shields.io/badge/license-MIT-green.svg)
![Python 3](https://img.shields.io/badge/python-3-blue.svg)
![Agent Skill](https://img.shields.io/badge/agent-ready-8A2BE2.svg)

Ein wiederverwendbarer Skill für KI-Agenten, damit sie Kreativ-Tonies mit Podcasts bespielen können.

Der Skill baut auf dem separaten Upstream-Projekt [`tonie-podcast-sync`](https://github.com/alexhartm/tonie-podcast-sync) auf und ergänzt darauf eine agent-freundliche Hülle für:

- Voraussetzungen prüfen
- Upstream lokal installieren
- Tonie-Zugangsdaten aus Umgebungsvariablen übernehmen
- Kreativ-Tonie-IDs ermitteln
- eine lokale `tonies.toml` mit Namen, Aliassen und IDs pflegen
- Podcasts aus einem eingebauten Katalog oder über freie RSS-URLs zuweisen
- einzelne oder alle konfigurierten Tonies synchronisieren

## Ziel

Dieses Repository ist dafür gedacht, dass ein Mensch es seinem KI-Agenten zeigt und sagt, dass er diesen Skill verwenden soll.

Kurz gesagt:

1. Gib deinem Agenten dieses Repository.
2. Sage ihm, dass du den Skill verwenden möchtest.
3. Der Agent soll dann `SKILL.md` lesen, die Voraussetzungen prüfen, das lokale Setup einrichten und gemeinsam mit dir die Tonies im Haushalt konfigurieren.

Explizit dokumentiert ist die Nutzung mit:

- **Hermes Agent**
- **OpenClaw**

## Schnellstart

Wenn du das Repository einfach einem Agenten geben willst, reicht in der Praxis oft dieser Auftrag:

```text
Hier ist ein Skill-Repository. Bitte verwende diesen Skill.
Lies zuerst SKILL.md, prüfe das Setup mit doctor,
richte tonie-podcast-sync lokal ein und hilf mir danach,
meine Kreativ-Tonies sauber zu konfigurieren.
```

Falls dein Agent kein automatisches Skill-Loading hat, sag zusätzlich explizit dazu, dass er die Datei `SKILL.md` als Hauptanleitung verwenden soll.

## Wichtige Eigenschaften

- **Keine privaten Tonie-IDs im Repository**
- **Lokale Konfiguration pro Haushalt** über `tonies.toml`
- **Klarer Discovery-Workflow**: erst Tonies finden, dann Namen/Aliasse lokal eintragen
- **Podcast-Katalog enthalten**
- **Freie RSS-URLs zusätzlich unterstützt**
- **Neutral gehalten**: keine persönlichen Referenzen auf ein konkretes Setup

## Repository-Inhalt

- `SKILL.md` – operative Anleitung für KI-Agenten
- `scripts/tonie_sync.py` – Helper-CLI für Setup, Discovery, Zuweisung und Sync
- `references/tonies.md` – detaillierte Anleitung für Tonie-ID-Findung und lokale Zuordnung
- `references/tonies.example.toml` – anonyme Beispielkonfiguration
- `references/podcasts.md` – eingebauter Podcast-Katalog
- `agents/openai.yaml` – minimales Agent-Metadatenbeispiel

## Wie ein Agent den Skill typischerweise verwendet

Der erwartete Ablauf ist:

1. `python3 scripts/tonie_sync.py doctor`
2. Falls Upstream oder virtuelle Umgebung fehlen:
   - `python3 scripts/tonie_sync.py setup-local --python python3`
3. Falls Zugangsdaten fehlen:
   - Umgebungsvariablen prüfen
   - optional `TONIE_SYNC_SKILL_ENV_FILE` setzen
   - dann `python3 scripts/tonie_sync.py bootstrap-secrets`
4. Falls noch keine lokale Tonie-Zuordnung existiert:
   - `python3 scripts/tonie_sync.py init-config`
5. Kreativ-Tonies ermitteln:
   - `python3 scripts/tonie_sync.py discover-tonies`
6. Die echten Tonies des Haushalts in die lokale `tonies.toml` eintragen:
   - ID
   - Name
   - Aliasse
   - optional Standard-Podcast und Sync-Parameter
7. Danach Podcast zuweisen oder synchronisieren.

## Lokale Pfade und Konfiguration

### Upstream-Installation

Der Skill installiert das Upstream-Projekt standardmäßig nach:

```text
~/.local/share/tonie-podcast-sync
```

Override über:

```text
TONIE_PODCAST_SYNC_PROJECT_DIR
```

### Lokale Tonie-Zuordnung

Standardpfad für die lokale Mapping-Datei:

```text
~/.config/tonie-podcast-sync-skill/tonies.toml
```

Override über:

```text
TONIE_SYNC_SKILL_CONFIG
```

### Lokale Settings/Secrets des Upstream-Projekts

Standardverzeichnis:

```text
~/.toniepodcastsync
```

Override über:

```text
TONIE_PODCAST_SYNC_SETTINGS_DIR
```

## Zugangsdaten

Der Skill erwartet Tonie-Cloud-Zugangsdaten über Umgebungsvariablen.

Unterstützte Variablen-Paare:

- `TPS_TONIE_CLOUD_ACCESS_USERNAME` + `TPS_TONIE_CLOUD_ACCESS_PASSWORD`
- `TONIE_CLOUD_ACCESS_USERNAME` + `TONIE_CLOUD_ACCESS_PASSWORD`
- `TONIE_CLOUD_USERNAME` + `TONIE_CLOUD_PASSWORD`
- `TONIE_USERNAME` + `TONIE_PASSWORD`

Optional kann zusätzlich eine Env-Datei angegeben werden über:

```text
TONIE_SYNC_SKILL_ENV_FILE
```

Wenn `TONIE_SYNC_SKILL_ENV_FILE` **nicht** gesetzt ist, sucht der Skill der Reihe nach in:

- `~/.env`
- `~/.hermes/.env`
- `~/.openclaw/.env`

Beispiel für eine lokale Env-Datei:

```dotenv
TONIE_USERNAME=dein-login@example.org
TONIE_PASSWORD=dein-passwort
```

Die Datei gehört **nur lokal** auf deinen Rechner und **nie** ins Repository.

## Tonies im Haushalt eintragen

Der Skill shippt absichtlich **keine** echten Haushaltsdaten mit.

Der Agent soll die Tonies des Haushalts nach der Discovery in die lokale `tonies.toml` eintragen. Dabei werden pro Tonie typischerweise gepflegt:

- `id` – echte Kreativ-Tonie-ID
- `name` – sprechender Name, z. B. `Benjamins Kreativ-Tonie`
- `aliases` – alternative Ansprachnamen, z. B. `benjamin`, `blauer tonie`, `einschlaf tonie`
- `default_podcast` – optionaler Podcast-Alias aus dem Katalog
- weitere Sync-Parameter wie `maximum_length`, `wipe`, `episode_sorting`

Details dazu stehen in:

- `references/tonies.md`
- `references/tonies.example.toml`

## Podcast-Zuweisung

### Eingebauter Katalog

Eine kuratierte Liste deutschsprachiger Podcasts ist eingebaut. Beispiele:

- `maus`
- `maus-gute-nacht`
- `pumuckl`
- `checker-tobi`
- `ohrenbaer`
- `kakadu`

Vollständige Liste:

- `references/podcasts.md`
- oder per CLI: `python3 scripts/tonie_sync.py list-podcasts`

### Freie RSS-URLs

Zusätzlich kann statt eines bekannten Alias auch direkt eine Feed-URL angegeben werden, zum Beispiel:

```bash
python3 scripts/tonie_sync.py assign --tonie benjamin-kreativ --podcast https://example.org/feed.xml
```

## Beispiel-Kommandos

Voraussetzungen prüfen:

```bash
python3 scripts/tonie_sync.py doctor
```

Upstream lokal einrichten:

```bash
python3 scripts/tonie_sync.py setup-local --python python3
```

Secrets aus Env übernehmen:

```bash
python3 scripts/tonie_sync.py bootstrap-secrets
```

Starter-Konfiguration schreiben:

```bash
python3 scripts/tonie_sync.py init-config
```

Kreativ-Tonies auf dem Konto anzeigen:

```bash
python3 scripts/tonie_sync.py discover-tonies
```

Bekannte lokale Tonies anzeigen:

```bash
python3 scripts/tonie_sync.py list-tonies
```

Podcast-Katalog anzeigen:

```bash
python3 scripts/tonie_sync.py list-podcasts
```

Aktuelle Zuordnungen anzeigen:

```bash
python3 scripts/tonie_sync.py show-config
```

Podcast auf einen Tonie legen:

```bash
python3 scripts/tonie_sync.py assign --tonie benjamin-kreativ --podcast pumuckl
```

Podcast zuweisen und sofort synchronisieren:

```bash
python3 scripts/tonie_sync.py assign-and-sync --tonie benjamin-kreativ --podcast maus-gute-nacht
```

Alle konfigurierten Tonies synchronisieren:

```bash
python3 scripts/tonie_sync.py sync --tonie all
```

## Nutzung mit Hermes Agent

Für Hermes genügt in der Praxis ein kurzer Auftrag wie:

- "Hier ist ein Skill-Repository. Bitte verwende diesen Tonie-Podcast-Skill."
- "Lies `SKILL.md`, richte das lokale Setup ein und hilf mir, meine Kreativ-Tonies zu konfigurieren."

Der Agent sollte dann:

- den Skill lesen
- `doctor` ausführen
- bei Bedarf das Upstream-Projekt nach `~/.local/share/tonie-podcast-sync` installieren
- deine Tonies finden
- die lokale `tonies.toml` befüllen
- danach gewünschte Podcasts zuweisen und synchronisieren

## Nutzung mit OpenClaw

Für OpenClaw gilt derselbe Ansatz:

- Repository zeigen
- sagen, dass der Skill verwendet werden soll
- den Agenten `SKILL.md` lesen lassen
- danach Setup, Discovery und lokale Konfiguration gemeinsam durchführen

## Agent-Metadaten

Unter `agents/openai.yaml` liegt ein kleines, bewusst schlichtes Metadatenbeispiel für Agent-Setups, die solche Zusatzdateien auswerten.

- `SKILL.md` bleibt die eigentliche operative Quelle.
- `README.md` ist die menschenlesbare Einführung.
- `agents/openai.yaml` ist optional und nur ein Hilfssignal für Tooling, das Skill-Repositories indexieren oder anzeigen möchte.

## Hinweise für Veröffentlichung und Betrieb

- Dieses Repository enthält **nur** anonyme Beispiele.
- Echte Tonie-IDs gehören **nicht** ins Repository.
- Zugangsdaten gehören **nicht** ins Repository.
- Die lokale `tonies.toml` ist haushaltsspezifisch.
- Die lokale `.secrets.toml` des Upstream-Projekts ist haushaltsspezifisch.

## Haftungsausschluss

Dieses Repository wird **as is** bereitgestellt, ohne Gewähr oder Zusicherung irgendeiner Art.

- Keine Garantie für Funktion, Stabilität oder Eignung für einen bestimmten Zweck
- Keine Haftung für Datenverlust, Fehlkonfigurationen oder Änderungen an Tonie-Inhalten
- Keine offizielle Verbindung zu Tonies, tonies®, Toniebox oder Boxine GmbH
- Das Upstream-Projekt `tonie-podcast-sync` bleibt separat und unter seiner eigenen Lizenz und Verantwortung

## Danksagung

Dieses Repository baut konzeptionell auf dem Upstream-Projekt [`tonie-podcast-sync`](https://github.com/alexhartm/tonie-podcast-sync) auf.

Die Podcast-Liste basiert auf einer deutschsprachigen Community-Sammlung, unter anderem aus dieser Reddit-Diskussion:

- <https://www.reddit.com/r/Eltern/comments/13g7x5i/comment/lwth5li/>

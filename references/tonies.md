# Tonies

Diese Referenz erklärt, wie ein Agent oder Mensch die echten Kreativ-Tonies eines Haushalts findet und danach sauber in die lokale `tonies.toml` übernimmt.

Der Skill enthält absichtlich **keine** echten Tonie-IDs.

## Grundidee

Der Workflow ist immer:

1. Zugangsdaten lokal verfügbar machen
2. Discovery mit dem Upstream-Tool ausführen
3. echte Kreativ-Tonie-IDs ablesen
4. diese Tonies in die lokale `tonies.toml` eintragen
5. sprechende Namen und natürliche Aliasse vergeben

## Zugangsdaten vorbereiten

Unterstützte Variablen-Paare:

- `TPS_TONIE_CLOUD_ACCESS_USERNAME` + `TPS_TONIE_CLOUD_ACCESS_PASSWORD`
- `TONIE_CLOUD_ACCESS_USERNAME` + `TONIE_CLOUD_ACCESS_PASSWORD`
- `TONIE_CLOUD_USERNAME` + `TONIE_CLOUD_PASSWORD`
- `TONIE_USERNAME` + `TONIE_PASSWORD`

Optional kann eine konkrete Env-Datei übergeben werden:

```text
TONIE_SYNC_SKILL_ENV_FILE=/pfad/zu/.env
```

Wenn `TONIE_SYNC_SKILL_ENV_FILE` nicht gesetzt ist, sucht der Skill standardmäßig in:

```text
~/.env
~/.hermes/.env
~/.openclaw/.env
```

## Kreativ-Tonies finden

Bevor IDs in die lokale Zuordnung eingetragen werden, Discovery ausführen:

```bash
python3 scripts/tonie_sync.py discover-tonies
```

Dieser Befehl reicht die Upstream-Discovery durch:

```bash
tonie-podcast-sync list-tonies
```

Erwartung:

- Du siehst die Kreativ-Tonies des Kontos
- inklusive ihrer IDs
- oft auch mit Cloud-seitigen Namen oder erkennbaren Beschriftungen

## Wie man die IDs sinnvoll übernimmt

Ein Agent soll die Ausgabe nicht blind nur als technische UUID behandeln, sondern zusammen mit dem Menschen klären:

- Welcher physische Tonie gehört zu welchem Kind?
- Welcher Tonie ist z. B. der Einschlaf-Tonie?
- Welche Namen benutzt der Haushalt im Alltag wirklich?

Dann trägt der Agent genau diese Realität in die lokale `tonies.toml` ein.

## Lokale Mapping-Datei erzeugen

Wenn noch keine Datei existiert:

```bash
python3 scripts/tonie_sync.py init-config
```

Standardpfad:

```text
~/.config/tonie-podcast-sync-skill/tonies.toml
```

Die Datei kann über `TONIE_SYNC_SKILL_CONFIG` an einen anderen Ort gelegt werden.

## Wie die lokale `tonies.toml` aufgebaut ist

Beispiel:

```toml
[tonies.benjamin-kreativ]
id = "12345678-1234-1234-1234-123456789abc"
name = "Benjamins Kreativ-Tonie"
aliases = ["benjamin", "blauer tonie", "einschlaf tonie"]
default_podcast = "maus-gute-nacht"
episode_sorting = "random"
maximum_length = 60
wipe = true
```

## Bedeutung der Felder

### Section-Key

```toml
[tonies.benjamin-kreativ]
```

- Das ist der **kanonische Slug**
- er sollte kurz, stabil und maschinenfreundlich sein
- empfohlen: Kleinbuchstaben und Bindestriche

### `id`

```toml
id = "12345678-1234-1234-1234-123456789abc"
```

- echte Kreativ-Tonie-ID aus der Discovery
- nie raten
- nie eine Beispiel-ID belassen

### `name`

```toml
name = "Benjamins Kreativ-Tonie"
```

- menschenfreundlicher Anzeigename
- darf ruhig so heißen, wie der Haushalt wirklich darüber spricht

### `aliases`

```toml
aliases = ["benjamin", "blauer tonie", "einschlaf tonie"]
```

- alternative Namen
- Dinge, die der Nutzer wahrscheinlich im Gespräch sagt
- helfen dem Agenten, denselben Tonie auch bei ungenauer Formulierung korrekt zu treffen

### `default_podcast`

```toml
default_podcast = "maus-gute-nacht"
```

- optional
- ein Alias aus dem eingebauten Podcast-Katalog
- nützlich für `restore-defaults` und als Ausgangsbelegung

## Gute Alias-Strategie

Sinnvolle Aliasse sind oft eine Mischung aus:

- Personenbezug: `benjamin`, `emma`
- Farbe/Form: `blauer tonie`, `orangener tonie`
- Funktion: `einschlaf tonie`, `geschichten tonie`
- Haushaltsinterne Kurzform: `benni tonie`

Weniger gut sind Aliasse, die:

- mehrdeutig sind
- sich mit anderen Tonies stark überschneiden
- nur technische UUID-Fragmente enthalten

## Empfohlener Gesprächsablauf mit dem Menschen

Ein Agent sollte nach der Discovery ungefähr so vorgehen:

1. Die gefundenen Kreativ-Tonies anzeigen
2. Den Menschen fragen, welcher gefundene Tonie welcher physische Tonie ist
3. Daraus einen stabilen Slug ableiten
4. Einen lesbaren `name` setzen
5. 2–4 natürliche `aliases` ergänzen
6. Alles in die lokale `tonies.toml` schreiben

## Wichtige Regel

Die lokale `tonies.toml` ist **haushaltsspezifisch**.

- Sie darf lokal geändert werden
- sie soll **nicht** mit echten Haushaltsdaten veröffentlicht werden
- sie dient genau dazu, dass ein Agent mit sprechenden Namen arbeiten kann, ohne private Daten ins Skill-Repository zu schreiben

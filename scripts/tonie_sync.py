#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_ENV_FILES = [
    Path.home() / ".env",
    Path.home() / ".hermes" / ".env",
    Path.home() / ".openclaw" / ".env",
]
DEFAULT_SETTINGS_DIR = Path.home() / ".toniepodcastsync"
DEFAULT_PROJECT_DIR = Path.home() / ".local" / "share" / "tonie-podcast-sync"
DEFAULT_CONFIG_FILE = Path.home() / ".config" / "tonie-podcast-sync-skill" / "tonies.toml"
EXAMPLE_CONFIG_FILE = SKILL_DIR / "references" / "tonies.example.toml"
GOOGLE_DOC_URL = "https://docs.google.com/spreadsheets/d/16EGIIIXWbNr8DwaGZWbUqnYHg_LgpgM7NECzTbUWgW4/edit?gid=0#gid=0"


PODCASTS: dict[str, dict[str, Any]] = {
    "maus": {
        "name": "Sendung mit der Maus - zum Hören",
        "feed": "https://www1.wdr.de/mediathek/podcast/podcast-die-maus-100.podcast",
        "aliases": ["maus", "sendung mit der maus", "maus zum hören", "maus zum hoeren", "sendung mit der maus zum hören", "sendung mit der maus zum hoeren"],
        "notes": "",
    },
    "maus-live": {
        "name": "Sendung mit der Maus - live",
        "feed": "wdr-diemaus-live.icecastssl.wdr.de/wdr/diemaus/live/mp3/128/stream.mp3",
        "aliases": ["maus live", "sendung mit der maus live"],
        "notes": "",
    },
    "pumuckl": {
        "name": "Pumuckl",
        "feed": "https://feeds.br.de/pumuckl/feed.xml",
        "aliases": ["pumuckl"],
        "notes": "",
    },
    "checker-tobi": {
        "name": "Checker Tobi Podcast",
        "feed": "https://feeds.br.de/checkpod-der-podcast-mit-checker-tobi/feed.xml",
        "aliases": ["checker tobi", "checker tobi podcast", "checkpod", "tobi"],
        "notes": "",
    },
    "anna-und-die-wilden-tiere": {
        "name": "Anna und die wilden Tiere",
        "feed": "https://feeds.br.de/anna-und-die-wilden-tiere/feed.xml",
        "aliases": ["anna und die wilden tiere", "anna wilde tiere"],
        "notes": "",
    },
    "geschichten-fuer-kinder-br": {
        "name": "Geschichten für Kinder BR",
        "feed": "https://feeds.br.de/geschichten-fuer-kinder/feed.xml",
        "aliases": ["geschichten für kinder", "geschichten fuer kinder", "br geschichten für kinder", "br geschichten fuer kinder"],
        "notes": "",
    },
    "maus-gute-nacht": {
        "name": "Gute Nacht mit der Maus",
        "feed": "https://kinder.wdr.de/radio/diemaus/audio/gute-nacht-mit-der-maus/diemaus-gute-nacht-104.podcast",
        "aliases": ["gute nacht mit der maus", "maus gute nacht", "gute nacht maus"],
        "notes": "",
    },
    "betthupferl": {
        "name": "Betthupferl - Gute-Nacht-Geschichten für Kinder BR",
        "feed": "https://feeds.br.de/betthupferl/feed.xml",
        "aliases": ["betthupferl"],
        "notes": "",
    },
    "tigerenten-club": {
        "name": "Tigerenten Club",
        "feed": "https://www.kindernetz.de/~podcast/sendungen/hoerspielshow/podcast-hoerspielshow-100.xml",
        "aliases": ["tigerenten club", "tigerenten"],
        "notes": "last episode 2024-05-10",
    },
    "lachlabor": {
        "name": "Das Lachlabor Podcast",
        "feed": "https://feeds.br.de/lachlabor/feed.xml",
        "aliases": ["lachlabor", "das lachlabor"],
        "notes": "",
    },
    "figarinos-fahrradladen": {
        "name": "figarinos Fahrradladen",
        "feed": "https://www.mdr.de/tweens/podcast/figarino/fahrradladen102-podcast.xml",
        "aliases": ["figarino", "figarinos fahrradladen"],
        "notes": "",
    },
    "was-ist-was": {
        "name": '"Was ist was" der Podcast',
        "feed": "https://feeds.megaphone.fm/KBBF5520541713",
        "aliases": ["was ist was", "was ist was podcast"],
        "notes": "last episode 2024-06-27",
    },
    "geolino-spezial": {
        "name": "Geolino spezial",
        "feed": "https://proxyfeed.svmaudio.com/aa/geolino-spezial",
        "aliases": ["geolino spezial", "geolino"],
        "notes": "",
    },
    "eric-erforscht": {
        "name": "Eric erforscht",
        "feed": "https://ericerforscht.libsyn.com/rss",
        "aliases": ["eric erforscht"],
        "notes": "",
    },
    "erlebnis-erde": {
        "name": "Erlebnis Erde",
        "feed": "https://www1.wdr.de/mediathek/audio/wdr/erlebnis-erde/erlebnis-erde-110.podcast",
        "aliases": ["erlebnis erde"],
        "notes": "",
    },
    "das-geheimnis": {
        "name": "Das Geheimnis - Musikalische Rätsel und Krimis zum Mitraten",
        "feed": "https://feeds.br.de/do-re-mikro-die-musiksendung-fuer-kinder/feed.xml",
        "aliases": ["das geheimnis", "rätsel und krimis", "raetsel und krimis"],
        "notes": "",
    },
    "quatsch-weisheit": {
        "name": "Quatsch & Weisheit: Kinder reden. Über die Welt",
        "feed": "https://feeds.br.de/quatsch-weisheit-kinder-reden-ueber-die-welt-und-ueberhaupt/feed.xml",
        "aliases": ["quatsch und weisheit", "quatsch & weisheit", "weisheit kinder reden über die welt", "weisheit kinder reden ueber die welt"],
        "notes": "",
    },
    "soko-kinderkrimi": {
        "name": "Soko Kinderkrimi",
        "feed": "https://cdn.stationista.com/feeds/soko-kinderkrimi",
        "aliases": ["soko kinderkrimi"],
        "notes": "",
    },
    "ohrenbaer": {
        "name": "Ohrenbär-Podcast",
        "feed": "https://www.ohrenbaer.de/podcast/podcast.feed.podcast.xml",
        "aliases": ["ohrenbär", "ohrenbaer", "ohrenbär podcast", "ohrenbaer podcast"],
        "notes": "",
    },
    "mikado": {
        "name": "Mikado - der Kinder-Podcast (NDR)",
        "feed": "https://www.ndr.de/nachrichten/info/sendungen/mikado/mikado_am_morgen/podcast4223.xml",
        "aliases": ["mikado", "mikado ndr"],
        "notes": "",
    },
    "kakadu": {
        "name": "Kakadu - Ein Kinderpodcast von Deutschlandfunk Kultur mit Geschichten, Rätseln und Wissenswertem für Kinder.",
        "feed": "https://www.kakadu.de/kakadu-104.xml",
        "aliases": ["kakadu"],
        "notes": "",
    },
    "unser-sandmaennchen": {
        "name": "Unser Sandmännchen",
        "feed": "https://www.antennebrandenburg.de/programm/hoeren/podcasts/Zappelduster_Podcast/podcast.xml/feed=podcast.xml",
        "aliases": ["sandmännchen", "sandmaennchen", "unser sandmännchen", "unser sandmaennchen"],
        "notes": "",
    },
    "weisst-du-schon": {
        "name": "Weißt du's schon? – Das Quiz für Kids",
        "feed": "https://weisstdusschon.podigee.io/feed/mp3",
        "aliases": ["weißt du's schon", "weisst du's schon", "weißt du schon", "weisst du schon"],
        "notes": "",
    },
    "flipsi-findets-raus": {
        "name": "Flipsi findet's raus – auf Expedition durch den Körper",
        "feed": "https://flipsi-findets-raus.podigee.io/feed/mp3",
        "aliases": ["flipsi", "flipsi findet's raus", "flipsi findets raus"],
        "notes": "",
    },
}


def env_file_override() -> Path | None:
    raw = os.environ.get("TONIE_SYNC_SKILL_ENV_FILE", "").strip()
    if not raw:
        return None
    return Path(raw).expanduser()


def env_file_candidates() -> list[Path]:
    override = env_file_override()
    if override is not None:
        return [override]
    return [path.expanduser() for path in DEFAULT_ENV_FILES]


def settings_dir() -> Path:
    return Path(os.environ.get("TONIE_PODCAST_SYNC_SETTINGS_DIR", DEFAULT_SETTINGS_DIR))


def settings_file() -> Path:
    return settings_dir() / "settings.toml"


def secrets_file() -> Path:
    return settings_dir() / ".secrets.toml"


def project_dir() -> Path:
    return Path(os.environ.get("TONIE_PODCAST_SYNC_PROJECT_DIR", DEFAULT_PROJECT_DIR))


def venv_python() -> Path:
    return project_dir() / ".venv" / "bin" / "python"


def venv_cli() -> Path:
    return project_dir() / ".venv" / "bin" / "tonie-podcast-sync"


def config_file() -> Path:
    return Path(os.environ.get("TONIE_SYNC_SKILL_CONFIG", DEFAULT_CONFIG_FILE))


def looks_like_feed_url(value: str) -> bool:
    raw = value.strip().lower()
    return raw.startswith("https://") or raw.startswith("http://")


def env_search_summary() -> str:
    override = env_file_override()
    if override is not None:
        return f"TONIE_SYNC_SKILL_ENV_FILE={override}"
    return ", ".join(str(path) for path in env_file_candidates())


def env_candidates() -> list[tuple[str, str]]:
    return [
        ("TPS_TONIE_CLOUD_ACCESS_USERNAME", "TPS_TONIE_CLOUD_ACCESS_PASSWORD"),
        ("TONIE_CLOUD_ACCESS_USERNAME", "TONIE_CLOUD_ACCESS_PASSWORD"),
        ("TONIE_CLOUD_USERNAME", "TONIE_CLOUD_PASSWORD"),
        ("TONIE_USERNAME", "TONIE_PASSWORD"),
    ]


def parse_dotenv(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith(("\"", "'")) and value.endswith(("\"", "'")) and len(value) >= 2:
            value = value[1:-1]
        data[key] = value
    return data


def find_credentials() -> tuple[str, str] | None:
    dotenv_sources = [parse_dotenv(path) for path in env_file_candidates()]
    for user_key, pass_key in env_candidates():
        username = os.environ.get(user_key)
        password = os.environ.get(pass_key)
        if username and password:
            return username, password
        for dotenv in dotenv_sources:
            username = dotenv.get(user_key)
            password = dotenv.get(pass_key)
            if username and password:
                return username, password
    return None


def credential_variable_summary() -> str:
    return ", ".join(f"{user_key}+{pass_key}" for user_key, pass_key in env_candidates())


def missing_credentials_message() -> str:
    return (
        "Keine Tonie-Zugangsdaten gefunden. "
        f"Setze eines dieser Variablen-Paare: {credential_variable_summary()}. "
        f"Gesuchte Env-Dateien: {env_search_summary()}."
    )


def ensure_secrets() -> bool:
    target = secrets_file()
    if target.exists():
        return True
    creds = find_credentials()
    if not creds:
        return False
    username, password = creds
    target.parent.mkdir(parents=True, exist_ok=True)
    content = (
        "[tonie_cloud_access]\n"
        f"username = {toml_string(username)}\n"
        f"password = {toml_string(password)}\n"
    )
    target.write_text(content, encoding="utf-8")
    return True


def toml_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def toml_bool(value: bool) -> str:
    return "true" if value else "false"


def toml_list(values: list[str]) -> str:
    return "[" + ", ".join(toml_string(v) for v in values) + "]"


def parse_value(raw: str) -> Any:
    value = raw.strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        parts = [part.strip() for part in inner.split(",")]
        return [parse_value(part) for part in parts]
    if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
        return int(value)
    return value


def load_settings_fallback(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {"creative_tonies": {}, "tonies": {}}
    current: dict[str, Any] | None = None
    current_slug: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
            current = None
            current_slug = None
            if section.startswith("creative_tonies."):
                current_slug = section.split(".", 1)[1]
                current = {}
                data["creative_tonies"][current_slug] = current
            elif section.startswith("tonies."):
                current_slug = section.split(".", 1)[1]
                current = {}
                data["tonies"][current_slug] = current
            continue
        if "=" not in line or current is None or current_slug is None:
            continue
        key, value = line.split("=", 1)
        current[key.strip()] = parse_value(value)
    return data


def load_toml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    try:
        import tomllib  # type: ignore[attr-defined]

        return tomllib.loads(text)
    except ModuleNotFoundError:
        return load_settings_fallback(text)


def load_skill_config() -> dict[str, dict[str, Any]]:
    path = config_file()
    if not path.exists():
        raise SystemExit(f"Tonie-Konfiguration fehlt: {path}\nErzeuge sie mit: python3 scripts/tonie_sync.py init-config")
    raw = load_toml(path)
    tonies = raw.get("tonies")
    if not isinstance(tonies, dict) or not tonies:
        raise SystemExit(f"Keine [tonies.*]-Einträge in {path} gefunden.")
    normalized: dict[str, dict[str, Any]] = {}
    for slug, cfg in tonies.items():
        if not isinstance(cfg, dict):
            raise SystemExit(f"Ungültige Tonie-Konfiguration für {slug}")
        tonie_id = str(cfg.get("id", "")).strip()
        name = str(cfg.get("name", slug)).strip()
        if not tonie_id:
            raise SystemExit(f"Tonie {slug} hat keine id in {path}")
        aliases = [str(item) for item in cfg.get("aliases", [])]
        normalized[str(slug)] = {
            "id": tonie_id,
            "name": name,
            "aliases": aliases,
            "default_podcast": cfg.get("default_podcast"),
            "episode_sorting": cfg.get("episode_sorting", "random"),
            "maximum_length": cfg.get("maximum_length", 90),
            "episode_min_duration_sec": cfg.get("episode_min_duration_sec", 0),
            "episode_max_duration_sec": cfg.get("episode_max_duration_sec"),
            "volume_adjustment": cfg.get("volume_adjustment", 0),
            "excluded_title_strings": cfg.get("excluded_title_strings", []),
            "pinned_episode_names": cfg.get("pinned_episode_names", []),
            "wipe": cfg.get("wipe", True),
        }
    return normalized


def load_settings() -> dict[str, Any]:
    data: dict[str, Any] = {"creative_tonies": {}}
    path = settings_file()
    if path.exists():
        parsed = load_toml(path)
        data["creative_tonies"] = dict(parsed.get("creative_tonies", {}))
    return data


def write_settings(data: dict[str, Any]) -> None:
    path = settings_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    blocks: list[str] = []
    creative_tonies = data.get("creative_tonies", {})
    for tonie_id in sorted(creative_tonies.keys()):
        cfg = creative_tonies[tonie_id]
        blocks.append(f"[creative_tonies.{tonie_id}]")
        ordered_keys = [
            "podcast",
            "name",
            "episode_sorting",
            "maximum_length",
            "episode_min_duration_sec",
            "episode_max_duration_sec",
            "volume_adjustment",
            "excluded_title_strings",
            "pinned_episode_names",
            "wipe",
        ]
        for key in ordered_keys:
            if key not in cfg or cfg[key] is None:
                continue
            value = cfg[key]
            if isinstance(value, bool):
                rendered = toml_bool(value)
            elif isinstance(value, int):
                rendered = str(value)
            elif isinstance(value, list):
                rendered = toml_list([str(v) for v in value])
            else:
                rendered = toml_string(str(value))
            blocks.append(f"{key} = {rendered}")
        blocks.append("")
    path.write_text("\n".join(blocks).rstrip() + "\n", encoding="utf-8")


def resolve_podcast(value: str) -> dict[str, Any]:
    raw = value.strip().lower()
    if looks_like_feed_url(value):
        return {
            "slug": None,
            "name": value.strip(),
            "feed": value.strip(),
            "notes": "custom feed url",
        }
    for slug, podcast in PODCASTS.items():
        if raw == slug or raw in [alias.lower() for alias in podcast["aliases"]]:
            return {
                "slug": slug,
                "name": str(podcast["name"]),
                "feed": str(podcast["feed"]),
                "notes": str(podcast.get("notes", "")),
            }
    raise SystemExit(
        f"Unbekannter Podcast oder Feed: {value}\n"
        "Nutze einen bekannten Podcast-Alias aus `list-podcasts` oder gib eine direkte http(s)-RSS-Feed-URL an."
    )


def resolve_tonie(value: str, tonies: dict[str, dict[str, Any]]) -> str:
    raw = value.strip().lower()
    for slug, tonie in tonies.items():
        aliases = [alias.lower() for alias in tonie.get("aliases", [])]
        if raw == slug.lower() or raw == tonie["id"].lower() or raw in aliases:
            return slug
    raise SystemExit(f"Unbekannter Tonie: {value}")


def apply_defaults(*, overwrite: bool) -> dict[str, Any]:
    skill_tonies = load_skill_config()
    data = load_settings()
    creative_tonies = data.setdefault("creative_tonies", {})
    for slug, tonie in skill_tonies.items():
        podcast_slug = tonie.get("default_podcast")
        if not podcast_slug:
            continue
        if podcast_slug not in PODCASTS:
            raise SystemExit(f"Unbekannter default_podcast {podcast_slug!r} für Tonie {slug}")
        existing = dict(creative_tonies.get(tonie["id"], {}))
        defaults = {
            "podcast": PODCASTS[podcast_slug]["feed"],
            "name": tonie["name"],
            "episode_sorting": tonie["episode_sorting"],
            "maximum_length": tonie["maximum_length"],
            "episode_min_duration_sec": tonie["episode_min_duration_sec"],
            "volume_adjustment": tonie["volume_adjustment"],
            "wipe": tonie["wipe"],
        }
        if tonie.get("episode_max_duration_sec") is not None:
            defaults["episode_max_duration_sec"] = tonie["episode_max_duration_sec"]
        if tonie.get("excluded_title_strings"):
            defaults["excluded_title_strings"] = tonie["excluded_title_strings"]
        if tonie.get("pinned_episode_names"):
            defaults["pinned_episode_names"] = tonie["pinned_episode_names"]
        for key, value in defaults.items():
            if overwrite or key not in existing:
                existing[key] = value
        creative_tonies[tonie["id"]] = existing
    write_settings(data)
    return data


def ensure_defaults() -> dict[str, Any]:
    return apply_defaults(overwrite=False)


def restore_defaults() -> dict[str, Any]:
    return apply_defaults(overwrite=True)


def assign_podcast(
    tonie_slug: str,
    podcast_feed: str,
    *,
    episode_sorting: str | None,
    maximum_length: int | None,
    episode_min_duration_sec: int | None,
    episode_max_duration_sec: int | None,
    volume_adjustment: int | None,
    wipe: bool | None,
) -> dict[str, Any]:
    skill_tonies = load_skill_config()
    data = ensure_defaults()
    tonie = skill_tonies[tonie_slug]
    cfg = dict(data["creative_tonies"].get(tonie["id"], {}))
    cfg["podcast"] = podcast_feed
    cfg["name"] = tonie["name"]
    if episode_sorting is not None:
        cfg["episode_sorting"] = episode_sorting
    if maximum_length is not None:
        cfg["maximum_length"] = maximum_length
    if episode_min_duration_sec is not None:
        cfg["episode_min_duration_sec"] = episode_min_duration_sec
    if episode_max_duration_sec is not None:
        cfg["episode_max_duration_sec"] = episode_max_duration_sec
    if volume_adjustment is not None:
        cfg["volume_adjustment"] = volume_adjustment
    if wipe is not None:
        cfg["wipe"] = wipe
    data["creative_tonies"][tonie["id"]] = cfg
    write_settings(data)
    return cfg


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def check_runtime(require_package: bool = False) -> list[str]:
    problems: list[str] = []
    if not project_dir().exists():
        problems.append(f"Projektordner fehlt: {project_dir()}")
    if not venv_python().exists():
        problems.append(f"Venv-Python fehlt: {venv_python()}")
    if require_package and not venv_cli().exists():
        problems.append(f"CLI fehlt: {venv_cli()}")
    return problems


def sync_one(tonie_slug: str) -> None:
    skill_tonies = load_skill_config()
    problems = check_runtime(require_package=True)
    if problems:
        raise SystemExit("\n".join(problems))
    if not ensure_secrets():
        raise SystemExit(missing_credentials_message())
    ensure_defaults()
    tonie_id = skill_tonies[tonie_slug]["id"]
    code = r'''
import sys
from tonie_podcast_sync.cli import _create_podcast_from_config, _create_tonie_podcast_sync
from tonie_podcast_sync.config import settings

tonies = settings.CREATIVE_TONIES
try:
    cfg = tonies[sys.argv[1]]
except Exception:
    raise SystemExit(f"Tonie-ID nicht in settings.toml gefunden: {sys.argv[1]}")

tps = _create_tonie_podcast_sync()
if not tps:
    raise SystemExit("Konnte ToniePodcastSync nicht initialisieren")
podcast = _create_podcast_from_config(cfg)
wipe = cfg.get("wipe", True)
tps.sync_podcast_to_tonie(podcast, sys.argv[1], cfg.maximum_length, wipe=wipe)
'''
    run([str(venv_python()), "-c", code, tonie_id])


def sync_all() -> None:
    problems = check_runtime(require_package=True)
    if problems:
        raise SystemExit("\n".join(problems))
    if not ensure_secrets():
        raise SystemExit(missing_credentials_message())
    ensure_defaults()
    run([str(venv_cli()), "update-tonies"])


def list_configured_tonies() -> None:
    tonies = load_skill_config()
    for slug, tonie in tonies.items():
        default_podcast = tonie.get("default_podcast") or "-"
        print(f"{slug}: {tonie['name']} ({tonie['id']}) default={default_podcast}")


def list_podcasts() -> None:
    for slug, podcast in PODCASTS.items():
        note = f" | {podcast['notes']}" if podcast["notes"] else ""
        print(f"{slug}: {podcast['name']} -> {podcast['feed']}{note}")
    print(f"\nQuelle: {GOOGLE_DOC_URL}")


def show_config() -> None:
    tonies = load_skill_config()
    data = ensure_defaults()
    creative_tonies = data.get("creative_tonies", {})
    for slug, tonie in tonies.items():
        cfg = creative_tonies.get(tonie["id"], {})
        print(f"[{slug}] {tonie['name']}")
        for key in [
            "podcast",
            "episode_sorting",
            "maximum_length",
            "episode_min_duration_sec",
            "episode_max_duration_sec",
            "volume_adjustment",
            "excluded_title_strings",
            "pinned_episode_names",
            "wipe",
        ]:
            if key in cfg:
                print(f"  {key}: {cfg[key]}")


def doctor() -> None:
    print(f"Skill: {SKILL_DIR}")
    print(f"Projektordner: {'OK' if project_dir().exists() else 'FEHLT'} {project_dir()}")
    print(f"Venv-Python: {'OK' if venv_python().exists() else 'FEHLT'} {venv_python()}")
    print(f"CLI: {'OK' if venv_cli().exists() else 'FEHLT'} {venv_cli()}")
    print(f"Settings: {'OK' if settings_file().exists() else 'FEHLT'} {settings_file()}")
    print(f"Secrets: {'OK' if secrets_file().exists() else 'FEHLT'} {secrets_file()}")
    print(f"Tonie-Config: {'OK' if config_file().exists() else 'FEHLT'} {config_file()}")
    creds = find_credentials()
    print(f"Env credentials: {'OK' if creds else 'FEHLT'} {env_search_summary()}")
    print(f"Credential keys: {credential_variable_summary()}")


def setup_local(python_bin: str = "python3") -> None:
    python_path = shutil.which(python_bin)
    if not python_path:
        raise SystemExit(f"Python nicht gefunden: {python_bin}")
    target = project_dir()
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        run(["git", "clone", "https://github.com/alexhartm/tonie-podcast-sync", str(target)])
    run([python_path, "-m", "venv", str(target / ".venv")])
    run([str(target / ".venv" / "bin" / "python"), "-m", "pip", "install", "--upgrade", "pip"])
    run([str(target / ".venv" / "bin" / "python"), "-m", "pip", "install", "tonie-podcast-sync"])


def init_config(force: bool = False) -> None:
    target = config_file()
    if target.exists() and not force:
        raise SystemExit(f"Tonie-Konfiguration existiert bereits: {target}\nVerwende --force zum Überschreiben.")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(EXAMPLE_CONFIG_FILE.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Beispiel-Konfiguration geschrieben: {target}")


def discover_tonies() -> None:
    problems = check_runtime(require_package=True)
    if problems:
        raise SystemExit("\n".join(problems))
    if not ensure_secrets():
        raise SystemExit(missing_credentials_message())
    run([str(venv_cli()), "list-tonies"])


def parse_bool(value: str) -> bool:
    raw = value.strip().lower()
    if raw in {"1", "true", "yes", "y", "ja"}:
        return True
    if raw in {"0", "false", "no", "n", "nein"}:
        return False
    raise argparse.ArgumentTypeError(f"Ungültiger Bool-Wert: {value}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generic helper CLI for tonie-podcast-sync based automation")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor")
    setup = sub.add_parser("setup-local")
    setup.add_argument("--python", default="python3")
    init_cmd = sub.add_parser("init-config")
    init_cmd.add_argument("--force", action="store_true")
    sub.add_parser("bootstrap-secrets")
    sub.add_parser("discover-tonies")
    sub.add_parser("list-tonies")
    sub.add_parser("list-podcasts")
    sub.add_parser("show-config")
    sub.add_parser("restore-defaults")

    assign = sub.add_parser("assign")
    assign.add_argument("--tonie", required=True)
    assign.add_argument("--podcast", required=True)
    assign.add_argument("--episode-sorting", choices=["by_date_newest_first", "by_date_oldest_first", "random"])
    assign.add_argument("--maximum-length", type=int)
    assign.add_argument("--episode-min-duration-sec", type=int)
    assign.add_argument("--episode-max-duration-sec", type=int)
    assign.add_argument("--volume-adjustment", type=int)
    assign.add_argument("--wipe", type=parse_bool)

    sync = sub.add_parser("sync")
    sync.add_argument("--tonie", default="all")

    assign_sync = sub.add_parser("assign-and-sync")
    assign_sync.add_argument("--tonie", required=True)
    assign_sync.add_argument("--podcast", required=True)
    assign_sync.add_argument("--episode-sorting", choices=["by_date_newest_first", "by_date_oldest_first", "random"])
    assign_sync.add_argument("--maximum-length", type=int)
    assign_sync.add_argument("--episode-min-duration-sec", type=int)
    assign_sync.add_argument("--episode-max-duration-sec", type=int)
    assign_sync.add_argument("--volume-adjustment", type=int)
    assign_sync.add_argument("--wipe", type=parse_bool)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "doctor":
        doctor()
        return
    if args.command == "setup-local":
        setup_local(args.python)
        print(f"Lokales Setup bereit: {project_dir()}")
        return
    if args.command == "init-config":
        init_config(force=args.force)
        return
    if args.command == "bootstrap-secrets":
        if ensure_secrets():
            print(f"Secrets bereit: {secrets_file()}")
            return
        raise SystemExit(missing_credentials_message())
    if args.command == "discover-tonies":
        discover_tonies()
        return
    if args.command == "list-tonies":
        list_configured_tonies()
        return
    if args.command == "list-podcasts":
        list_podcasts()
        return
    if args.command == "show-config":
        show_config()
        return
    if args.command == "restore-defaults":
        restore_defaults()
        print(f"Standardeinstellungen geschrieben: {settings_file()}")
        return
    if args.command in {"assign", "assign-and-sync"}:
        tonies = load_skill_config()
        tonie_slug = resolve_tonie(args.tonie, tonies)
        podcast = resolve_podcast(args.podcast)
        assign_podcast(
            tonie_slug,
            podcast["feed"],
            episode_sorting=args.episode_sorting,
            maximum_length=args.maximum_length,
            episode_min_duration_sec=args.episode_min_duration_sec,
            episode_max_duration_sec=args.episode_max_duration_sec,
            volume_adjustment=args.volume_adjustment,
            wipe=args.wipe,
        )
        label = podcast["name"]
        if podcast["slug"]:
            label = f"{label} ({podcast['slug']})"
        print(f"{tonies[tonie_slug]['name']} -> {label}")
        print(f"Settings aktualisiert: {settings_file()}")
        if args.command == "assign-and-sync":
            sync_one(tonie_slug)
        return
    if args.command == "sync":
        if args.tonie == "all":
            sync_all()
            return
        tonie_slug = resolve_tonie(args.tonie, load_skill_config())
        sync_one(tonie_slug)
        return

    parser.error("Unbekannter Befehl")


if __name__ == "__main__":
    main()

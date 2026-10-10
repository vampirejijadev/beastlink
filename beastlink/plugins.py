"""
Beastlink plugin loader.
Author: VampireDev
"""
from __future__ import annotations

import importlib.util
import sys
import traceback
from pathlib import Path
from typing import Any

PLUGIN_API_VERSION = "1.0"


class Plugin:
    """Base class — plugins can optionally subclass this."""
    name = "unnamed"
    version = "0.0.0"
    api_version = PLUGIN_API_VERSION

    def on_load(self, node: Any) -> None: ...
    def on_unload(self, node: Any) -> None: ...
    def on_track_start(self, node: Any, track: Any) -> None: ...
    def on_track_end(self, node: Any, track: Any) -> None: ...
    def on_track_exception(self, node: Any, track: Any, error: Exception) -> None: ...
    def register_filters(self) -> dict: return {}


def load_plugins(plugins_dir: Path, node: Any) -> list[Plugin]:
    """Load every .py file in plugins_dir (skipping _*.py and README)."""
    loaded: list[Plugin] = []

    if not plugins_dir.exists():
        return loaded

    for file in sorted(plugins_dir.glob("*.py")):
        if file.name.startswith("_"):
            continue

        try:
            spec = importlib.util.spec_from_file_location(
                f"beastlink_plugin_{file.stem}", file
            )
            if not spec or not spec.loader:
                continue
            mod = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = mod
            spec.loader.exec_module(mod)

            # Find a Plugin subclass, else instantiate Plugin-compatible object
            plugin_obj = None
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name)
                if (isinstance(attr, type)
                        and issubclass(attr, Plugin)
                        and attr is not Plugin):
                    plugin_obj = attr()
                    break

            # Fallback: module-level `setup(node)` function
            if plugin_obj is None and hasattr(mod, "setup"):
                mod.setup(node)
                plugin_obj = Plugin()
                plugin_obj.name = file.stem

            if plugin_obj:
                plugin_obj.on_load(node)
                loaded.append(plugin_obj)
                print(f"  ✔ Plugin loaded: {plugin_obj.name} v{plugin_obj.version}")
            else:
                print(f"  ⚠ Skipped {file.name}: no Plugin subclass or setup()")

        except Exception as exc:
            print(f"  ✘ Plugin failed: {file.name} — {exc}")
            traceback.print_exc()

    return loaded
#!/usr/bin/env python3
"""ram-nurvalue - show used RAM as a bare number in the Budgie panel.

Displays e.g. "4,9 GiB" next to the clock and refreshes every 2 seconds.

Used memory is computed as MemTotal - MemAvailable, the same figure modern
`free` prints under "used". See the README for why that is the honest number.

License: MIT
"""

import os

import gi

gi.require_version("Budgie", "1.0")
gi.require_version("Gtk", "3.0")

from gi.repository import Budgie, GLib, GObject, Gtk

REFRESH_SECONDS = 2

# German output when the session is German, English otherwise.
GERMAN = (os.environ.get("LC_ALL") or os.environ.get("LC_MESSAGES")
          or os.environ.get("LANG") or "").startswith("de")
TOOLTIP = ("Arbeitsspeicher belegt: %s von %s GiB (%d %%)" if GERMAN
           else "Memory in use: %s of %s GiB (%d %%)")


def read_memory():
    """Return (used, total) in GiB, read from /proc/meminfo."""
    values = {}
    with open("/proc/meminfo", "r") as handle:
        for line in handle:
            parts = line.split()
            if parts[0] in ("MemTotal:", "MemAvailable:"):
                values[parts[0]] = int(parts[1])  # KiB
                if len(values) == 2:
                    break
    total = values["MemTotal:"] / 1024 / 1024
    available = values["MemAvailable:"] / 1024 / 1024
    return total - available, total


def fmt(value):
    """1.5 -> "1,5" in German locales, "1.5" elsewhere."""
    text = "%.1f" % value
    return text.replace(".", ",") if GERMAN else text


class RamNurvalue(GObject.GObject, Budgie.Plugin):
    """Plugin entry point: Budgie asks here for the panel widget."""

    __gtype_name__ = "RamNurvalue"

    def do_get_panel_widget(self, uuid):
        return RamNurvalueApplet(uuid)


class RamNurvalueApplet(Budgie.Applet):
    """The widget itself: a label that refreshes every few seconds."""

    def __init__(self, uuid):
        Budgie.Applet.__init__(self)
        self.uuid = uuid
        self.timer_id = 0

        self.label = Gtk.Label(label="…")
        self.label.set_margin_start(4)
        self.label.set_margin_end(4)

        # Own style class so a GTK stylesheet can colour this widget.
        self.get_style_context().add_class("ram-nurvalue")

        self.add(self.label)
        self.show_all()

        self.refresh()
        self.timer_id = GLib.timeout_add_seconds(REFRESH_SECONDS, self.refresh)
        self.connect("destroy", self.cleanup)

    def refresh(self, *_):
        try:
            used, total = read_memory()
        except Exception:
            # Never take the panel down if /proc misbehaves for a moment.
            return GLib.SOURCE_CONTINUE

        self.label.set_text("%s GiB" % fmt(used))
        self.set_tooltip_text(
            "Arbeitsspeicher used: %s von %s GiB (%d %%)"
            % (fmt(used), fmt(total), round(used / total * 100))
        )
        return GLib.SOURCE_CONTINUE

    def cleanup(self, *_):
        if self.timer_id:
            GLib.source_remove(self.timer_id)
            self.timer_id = 0

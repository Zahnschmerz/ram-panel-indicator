# ram-panel-indicator

Show **used memory as a bare number** in your panel — `6,8 GiB`, nothing else.
No bar, no graph, no label. Refreshes every two seconds.

Two desktops are covered, each with the smallest thing that works there:

| Desktop | How | File |
|---|---|---|
| **Xfce** | `xfce4-genmon-plugin` runs a tiny awk script | [`xfce/`](xfce/) |
| **Budgie** | a small native applet in Python | [`budgie/`](budgie/) |

Both print the same figure and behave identically.
Tooltip and decimal separator follow your locale (German or English).

### Xfce: two looks

| Script | Look |
|---|---|
| `xfce/ram-nurzahl` | the bare number in the panel font |
| `xfce/ram-pille` | the number in a rounded, tinted pill — blue while there is room, **orange from 80 %** — with a richer tooltip (free, used %, swap) |

![The pill, normal and above 80 %](xfce/pill.png)

genmon cannot style its label, so `ram-pille` draws the pill as a small SVG in
`$XDG_RUNTIME_DIR` on every run and shows it through genmon's `<img>` tag.
It is drawn in [Outfit](https://fonts.google.com/specimen/Outfit) when that font
is installed, otherwise in a plain sans.

---

## Which number is this, and why

Used memory is computed as:

```
used = MemTotal - MemAvailable
```

This is the honest figure. It answers the question a person actually asks —
*how much can I still start without closing anything?* — because the kernel
already accounts for the part of the page cache it can hand back.

It matches what modern `free` prints under **used**, and what Conky reports
with `no_buffers = true`.

### Three figures, one machine, same moment

If two programs on your desktop disagree about memory, this is usually why.
Measured on one machine with 15.4 GiB of RAM, all in the same instant:

| | Formula | Result | Who reports it |
|---|---|---|---|
| **A** | `MemTotal - MemAvailable` | **7.5 GiB** | this indicator, modern `free`, Conky (`no_buffers=true`), KDE, Cinnamon, Budgie |
| **B** | `MemTotal - MemFree - Buffers - Cached - SReclaimable` | **6.1 GiB** | the *old* `free` formula, still quoted in older guides |
| **C** | `MemTotal - MemFree` | **14.7 GiB** | Conky with `no_buffers=false`, some system monitors |

**C is the trap.** It reads *95 % full* on an idle machine. Almost all of it is
page cache that the kernel returns the moment a program needs it. Linux
deliberately keeps almost nothing empty — free memory is wasted memory.

`tools/memory-compare` prints all three for your machine:

```sh
./tools/memory-compare
```

It reads `/proc/meminfo` **exactly once**. Two separate reads sample two
different moments, and then identical formulas look like they disagree —
an easy way to chase a bug that isn't there.

---

## Install

See [`xfce/INSTALL.md`](xfce/INSTALL.md) or [`budgie/INSTALL.md`](budgie/INSTALL.md).
Neither needs root; nothing outside your home directory is touched.

---

## Requirements

* **Xfce:** `xfce4-genmon-plugin` (ships with most Xfce spins), `awk`, `xfconf-query`;
  for the pill also the SVG image loader (`librsvg2-common` on Debian/Ubuntu, usually present)
* **Budgie:** `budgie-desktop`, `python3`, `python3-gi`, `gir1.2-budgie-1.0`
* **tools/memory-compare:** `python3` only

No third-party libraries. No network access. Reads one file: `/proc/meminfo`.

---

## Notes and known quirks

### Xfce: three ways to make genmon show nothing at all

All three produce the *same* symptom — the plugin loads, its process runs, the
command runs, and the panel stays completely empty. Not even genmon's own `XXX`
error marker appears. Each of these cost real time to find:

1. **`Font=(Default)`** — an invalid font string makes genmon draw *nothing*.
   Leave the `Font=` line exactly as genmon wrote it (e.g. `Font=Noto Sans 10.5`).
2. **A `[Configuration]` group header** — genmon 4.1.x writes a *flat* rc file
   with no group header. Adding one silently voids every setting.
3. **`UpdatePeriod` is in milliseconds.** `UpdatePeriod=2` means *2 ms*, not
   2 seconds. Measured: **1735 invocations in 10 seconds**, and the display
   never settles long enough to paint. Use `2000`.

**The reliable way to configure it:** add the plugin, quit the panel so genmon
writes its own default rc file, then replace only the values you need. Do not
hand-write the file from guessed key names.

If something "runs but shows nothing", **count how often it runs** before
looking anywhere else.

### genmon 4.2.0 and later

From 4.2.0 genmon stores its settings in **xfconf** instead of rc files, and
existing settings are not migrated. The instructions here are for **4.1.x**
(check with `dpkg -l xfce4-genmon-plugin` or your package manager). For 4.2.0+
see the upstream migration script.

### Panel order

The panel writes its state back when it exits, so change plugin order **while
the panel is stopped**, or your change is overwritten.

---

## Deutsch

**Zeigt den belegten Arbeitsspeicher als nackte Zahl in der Leiste** — `6,8 GiB`,
sonst nichts. Kein Balken, keine Kurve, keine Beschriftung. Erneuert sich alle
zwei Sekunden. Für **Xfce** (über `xfce4-genmon-plugin`) und **Budgie** (kleines
eigenes Applet). Sprache und Komma richten sich nach der Systemsprache.

**Für Xfce gibt es zwei Aussehen:** `ram-nurzahl` (nur die Zahl) oder `ram-pille`
— die Zahl in einer farbigen Kapsel, **blau** im Normalfall, **orange ab 80 %**,
dazu eine ausführlichere Sprechblase (frei, belegt in Prozent, Auslagerung).

**Die Zahl** ist `MemTotal − MemAvailable` — dieselbe, die `free` unter „benutzt"
zeigt. Sie beantwortet die Frage, die man wirklich stellt: *Wie viel kann ich noch
starten, ohne etwas zu schliessen?*

⚠️ **Warum andere Programme andere Zahlen zeigen:** `MemTotal − MemFree` ergibt auf
demselben Rechner im selben Moment **14,7 statt 7,5 GiB** — das sieht aus wie
„Speicher voll", ist aber fast nur Zwischenspeicher, den der Kernel sofort
zurückgibt. `tools/memory-compare` zeigt alle drei Rechenwege nebeneinander.

**Einbau:** siehe `xfce/INSTALL.md` bzw. `budgie/INSTALL.md`. Keine
Administratorrechte nötig, es wird nichts ausserhalb des eigenen Ordners verändert.

---

## Author

Gilbert Rikus

## License

MIT — see [LICENSE](LICENSE).

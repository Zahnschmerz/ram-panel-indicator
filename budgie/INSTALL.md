# Budgie

Tested on Budgie 10.9.x on X11.

## Install

```sh
mkdir -p ~/.local/share/budgie-desktop/plugins/ram-nurzahl
cp ram_nurzahl.py ram-nurzahl.plugin ~/.local/share/budgie-desktop/plugins/ram-nurzahl/
```

Then: right-click the panel → *Panel settings* → *Applets* → **+** →
**RAM (number only)**, and drag it next to the clock.

If the applet does not appear in the list, restart the panel:

```sh
nohup budgie-panel --replace >/dev/null 2>&1 &
```

## Requirements

`python3`, `python3-gi`, `gir1.2-budgie-1.0`. On Debian and Ubuntu:

```sh
sudo apt install python3-gi gir1.2-budgie-1.0
```

## Styling

The widget carries the CSS class `ram-nurzahl`, so you can colour it from your
own GTK stylesheet:

```css
.ram-nurzahl label { color: #ffffff; font-weight: bold; }
```

## Check it worked

```sh
free -h | awk 'NR==2 {print "free says used:", $3}'
```

That figure must match the number in your panel.

## Remove

Remove the applet from the panel, then delete
`~/.local/share/budgie-desktop/plugins/ram-nurzahl`.

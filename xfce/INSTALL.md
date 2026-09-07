# Xfce

Tested on Xfce 4.20 with `xfce4-genmon-plugin` **4.1.1**.
For genmon 4.2.0+ see the note in the main README — settings moved to xfconf.

## 1. Install the script

```sh
install -Dm755 ram-nurzahl ~/.local/bin/ram-nurzahl
~/.local/bin/ram-nurzahl /proc/meminfo      # should print <txt>...</txt><tool>...</tool>
```

## 2. Add the plugin

```sh
xfce4-panel --add=genmon
```

Note the id it gets — it is the last number in:

```sh
xfconf-query -c xfce4-panel -p /panels/panel-1/plugin-ids -v
```

The examples below use **13**; substitute yours.

## 3. Configure it

Stop the panel first, otherwise it writes its old state back over your change:

```sh
xfce4-panel --quit
sleep 2
```

genmon has now written its own default settings file. Edit **only** these two
lines in `~/.config/xfce4/panel/genmon-13.rc` — leave `Font=` and the file's
layout exactly as they are:

```sh
sed -i -e 's|^Command=.*|Command='"$HOME"'/.local/bin/ram-nurzahl /proc/meminfo|' \
       -e 's|^UpdatePeriod=.*|UpdatePeriod=2000|' \
       -e 's|^UseLabel=.*|UseLabel=0|' \
       ~/.config/xfce4/panel/genmon-13.rc
```

The result should look like `genmon.rc.example` in this directory.

## 4. Put it where you want it

To place it directly left of the clock, list the current order, move your id in
front of the clock's id, and write the whole list back:

```sh
xfconf-query -c xfce4-panel -p /panels/panel-1/plugin-ids -v      # read
# then write the full list back, e.g.:
xfconf-query -c xfce4-panel -p /panels/panel-1/plugin-ids \
  -t int -s 20 -t int -s 6 -t int -s 7 -t int -s 13 -t int -s 1
```

## 5. Start the panel

```sh
nohup xfce4-panel >/dev/null 2>&1 &
```

## Check it worked

```sh
free -h | awk 'NR==2 {print "free says used:", $3}'
```

That figure must match the number in your panel. If it does not, run
`../tools/memory-compare` — you are probably comparing against a different
formula, not seeing a bug.

## Remove

Right-click the number → *Remove*. Then `rm ~/.local/bin/ram-nurzahl`.

## If the panel stays empty

The plugin process runs and the command runs, but nothing is drawn. Check, in
this order — see the main README for the full explanation:

1. `Font=` — must be a real font string, not `(Default)`
2. no `[Configuration]` header in the rc file
3. `UpdatePeriod` is in **milliseconds** (`2000`, not `2`)

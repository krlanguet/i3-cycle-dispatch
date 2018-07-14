# i3-cycle-dispatch
Enables modifying i3 focus and move behavior depending on the focused window.

The goal of this tool is to control tabs and windows using the same commands, whether the program manages its own or not,
and to enforce a sharp distinction between tabs and windows with different cycling behavior.

It is a fork of [i3-dispatch](https://github.com/teto/i3-dispatch), borrowing inspiration from [i3-cycle](https://github.com/mota/i3-cycle).

## Supported applications
* Neovim
* Qutebrowser

## Usage
Install with
```sh
python setup.py --install
```

Then use in your i3 configuration, by replacing (some of) your focus and move bindings:
```
bindsym $mod+h exec i3cd left
bindsym $mod+j exec i3cd down
bindsym $mod+k exec i3cd up
bindsym $mod+l exec i3cd right

# alternatively, you can use the cursor keys:
bindsym $mod+Left  exec /usr/bin/i3cd left
bindsym $mod+Down  exec /usr/bin/i3cd down
bindsym $mod+Up    exec /usr/bin/i3cd up
bindsym $mod+Right exec /usr/bin/i3cd right

```
## Debugging
Logs by default in $HOME/i3cd.log

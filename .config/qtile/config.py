# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import psutil
import subprocess
from typing import List  # noqa: F401
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod1" # Alt key.
sup = "mod4" # Super key.
terminal = "tilix"

keys = [
    # Program spawn.
    Key([sup], "i", lazy.spawn(
        '/home/necronzero/.intelFPGA_lite/20.1/quartus/bin/quartus --64bit'
        )), # Quartus prime lite.
    Key([sup], "a", lazy.spawn(
        '/home/necronzero/.local/share/JetBrains/Toolbox/apps/AndroidStudio/ch-0/201.7199119/bin/studio.sh'
        )), # Android Studio.
    Key([sup], "j", lazy.spawn(
        '/home/necronzero/.local/share/JetBrains/Toolbox/bin/jetbrains-toolbox %u'
        )), # Jetbrains Toolbox.
    Key([sup], "x", lazy.spawn('simple-scan')), # Gnome document scanner UI.
    Key([sup], "m", lazy.spawn('wxmaxima')), # Maxima's UI.
    Key([sup], "l", lazy.spawn('librewolf')), # Librewolf.
    # Old keybind spawn.
    Key([sup], "1", lazy.spawn('brave')), # Google Chrome browser.
    Key([sup], "2", lazy.spawn('pcmanfm')), # Nautilus File Manager.
    Key([sup], "3", lazy.spawn(terminal)), # Tilix terminal emulator.
    Key([sup], "4", lazy.spawn('code')), # Visual Studio Code.
    Key([sup], "5", lazy.spawn('spyder')), # Spyder IDE.
    Key([sup], "6", lazy.spawn('vmplayer')), # Vmware Player.
    #Key([sup], "7", lazy.spawn("")),
    #Key([sup], "8", lazy.spawn("")),
    #Key([sup], "9", lazy.spawn("")),
    Key([sup], "0", lazy.spawn('tilix -e bpytop')),
    # Navigating through windows.
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn('rofi -show drun'), desc="Launch rofi"),
    #Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Brightness control.
    Key([], 'F7', lazy.spawn('xset dpms force off')),
    Key([], 'XF86MonBrightnessUp',   lazy.spawn('xbacklight -inc 5')),
    Key([], 'XF86MonBrightnessDown', lazy.spawn('xbacklight -dec 5')),
    # Volume control.
    Key([], 'XF86AudioMute', lazy.spawn('amixer -D pulse sset Master toggle')),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer -D pulse sset Master 5%+')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer -D pulse sset Master 5%-')),
    Key([], 'XF86AudioMicMute', lazy.spawn('amixer set Capture toggle')),
    # Screenshots [selection, full].
    Key([mod], 'Print', lazy.spawn('flameshot gui -p /home/necronzero/Pictures')),
    Key([sup], 'Print', lazy.spawn('flameshot full -p /home/necronzero/Pictures')),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

color_main = '#000000'

layout_theme = {"border_width": 2,
                "margin": 0,
                "border_focus": '#345eeb',
                "border_normal": "1D2330"
                }

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='RobotoMono Nerd Font Bold',
    fontsize=11,
    padding=2,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(
                    scale=.75,
                ),
                widget.GroupBox(
                    rounded = False,
                ),
                widget.WindowName(),
                widget.TextBox(
                    text = '| ',
                    background = color_main,
                    padding = 0,
                    fontsize = 14,
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(terminal + " -e bpytop")},
                ),
                widget.CPU(
                    background=color_main,
                    format='{freq_current}GHz {load_percent: 2.0f}%',
                    update_interval=2,
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(terminal + " -e bpytop")},
                ),
                widget.TextBox(
                    text = '| ',
                    background = color_main,
                    padding = 0,
                    fontsize = 14,
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(terminal + " -e bpytop")},
                ),
                widget.Memory(
                    background=color_main,
                    format='{MemUsed: .0f}M/16G',
                    update_interval=2,
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(terminal + " -e bpytop")},
                ),
                widget.TextBox(
                    text = '|說 ',
                    background = color_main,
                    padding = 0,
                    fontsize = 14,
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("bash /home/necronzero/.config/rofi-network-manager/rofi-network-manager.sh")},
                ),
                widget.Wlan(
                    interface='wlp3s0',
                    update_interval=5,
                    format="{essid} {percent:2.0%}",
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("bash /home/necronzero/.config/rofi-network-manager/rofi-network-manager.sh")},

                ),
                #widget.Net(
                #    background=color_main,
                #    format='{down} ↓↑ {up}',
                #    use_bits=True,
                #),
                widget.TextBox(
                    text = '| ',
                    background = color_main,
                    padding = 0,
                    fontsize = 14,
                ),
                widget.Battery(
                    background=color_main,
                    format='{percent:2.0%} {hour:d}:{min:02d}',
                ),
                widget.TextBox(
                    text = '|  ',
                    background = color_main,
                    padding = 0,
                    fontsize = 14,
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("xbacklight = 1")},
                ),
                widget.Backlight(
                    background=color_main,
                    brightness_file='/sys/class/backlight/intel_backlight/brightness',
                    max_brightness_file='/sys/class/backlight/intel_backlight/max_brightness',
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("xbacklight = 1")},
                    update_interval=2,
                ),
                widget.TextBox(
                    text = '| ',
                    background = color_main,
                    padding = 0,
                    fontsize = 14,
                ),
                widget.Volume(
                    background=color_main,
                    step=1,
                    update_interval=.5,
                ),
                #widget.Chord(
                #    chords_colors={
                #        'launch': ("#ff0000", "#ffffff"),
                #    },
                #    name_transform=lambda name: name.upper(),
                #),
                #widget.TextBox("default config", name="default"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                widget.TextBox(
                    text = '| ',
                    background = color_main,
                    padding = 0,
                    fontsize = 14,
                ),
                widget.Clock(
                    background=color_main,
                    format='%H:%M %d/%m ',
                    update_interval=10,
                ),
                #widget.QuickExit(),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.client_new
def _swallow(window):
    pid = window.window.get_net_wm_pid()
    ppid = psutil.Process(pid).ppid()
    cpids = {c.window.get_net_wm_pid(): wid for wid, c in window.qtile.windows_map.items()}
    for i in range(5):
        if not ppid:
            return
        if ppid in cpids:
            parent = window.qtile.windows_map.get(cpids[ppid])
            parent.minimized = True
            window.parent = parent
            return
        ppid = psutil.Process(ppid).ppid()

@hook.subscribe.client_killed
def _unswallow(window):
    if hasattr(window, 'parent'):
        window.parent.minimized = False

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('/home/necronzero/.config/qtile/autostart.sh')
    subprocess.call([home], shell=True)

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

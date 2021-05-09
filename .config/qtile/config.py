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
import battery

mod = "mod1" # Alt key.
sup = "mod4" # Super key.
terminal = "tilix"

keys = [
    # Spawn Guide.
    Key([], "XF86Favorites", lazy.spawn(
        'zathura ~/.config/help.pdf'
        )),
    # Program spawn.
    Key([sup], "i", lazy.spawn(
        '/home/necronzero/.intelFPGA_lite/20.1/quartus/bin/quartus --64bit'
        )), # Quartus prime lite.
    Key([sup], "m", lazy.spawn('wxmaxima')), # Maxima's UI.
    # Old keybind spawn.
    Key([sup], "1", lazy.spawn('firefox')), # Google Chrome browser.
    Key([sup], "2", lazy.spawn('nemo')), # Nemo File Manager.
    Key([sup], "3", lazy.spawn(terminal)), # Tilix terminal emulator.
    Key([sup], "4", lazy.spawn('code')), # Visual Studio Code.
    Key([sup], "5", lazy.spawn('spyder')), # Spyder IDE.
    Key([sup], "6", lazy.spawn('vmplayer')), # Vmware Player.
    Key([sup], "7", lazy.spawn(
        '/home/necronzero/.local/share/JetBrains/Toolbox/apps/AndroidStudio/ch-0/202.7231092/bin/studio.sh'
        )), # Android Studio
    Key([sup], "8", lazy.spawn("simple-scan")), # Gnome document scanner GUI
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
    # Wireless control.
    #Key([], 'XF86Bluetooth', lazy.spawn('')),
    #Key([], 'XF86WLAN', lazy.spawn('')),
    #Key([], 'XF86Tools', lazy.spawn('')),
    # Brightness control.
    Key([], 'XF86MonBrightnessUp',   lazy.spawn('xbacklight -inc 5')),
    Key([], 'XF86MonBrightnessDown', lazy.spawn('xbacklight -dec 5')),
    # Volume control.
    Key([], 'XF86AudioMute', lazy.spawn('amixer -D pulse sset Master toggle')),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer -D pulse sset Master 5%+')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer -D pulse sset Master 5%-')),
    Key([], 'XF86AudioMicMute', lazy.spawn('amixer set Capture toggle')),
    # Screenshots [selection, full].
    Key([mod], 'Print', lazy.spawn('flameshot gui -p /home/necronzero/Pictures/Screenshots')),
    Key([sup], 'Print', lazy.spawn('flameshot full -p /home/necronzero/Pictures/Screenshots')),
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
                "border_normal": "1D2330"}

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
                    use_mouse_wheel = False,
                ),
                widget.WindowName(),
                widget.TextBox(
                    text = ' ',
                    background = color_main,
                    padding = 0,
                    fontsize = 16,
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(terminal + " -e bpytop")},
                ),
                widget.CPU(
                    background=color_main,
                    #format='{freq_current}GHz {load_percent: 2.0f}%',
                    format='{freq_current}GHz',
                    update_interval=2,
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(terminal + " -e bpytop")},
                ),
                widget.Memory(
                    background=color_main,
                    format='{MemUsed: .0f}M/16G',
                    update_interval=2,
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(terminal + " -e bpytop")},
                ),
                widget.TextBox(
                    text = ' ',
                    background = color_main,
                    padding = 0,
                    fontsize = 16,
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("bash /home/necronzero/.config/rofi-network-manager/rofi-network-manager.sh")},
                ),
                widget.Wlan(
                    interface='wlp3s0',
                    update_interval=5,
                    format="{essid} {percent:2.0%}",
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("bash /home/necronzero/.config/rofi-network-manager/rofi-network-manager.sh")},

                ),
                widget.TextBox(
                    text='',
                    background=color_main,
                    padding=0,
                    fontsize=16,
                ),
                battery.BatteryIcon(
                    padding=0,
                    scale=0.7,
                    y_poss=2,
                    theme_path="/home/necronzero/.config/qtile/icons/battery_icons_horiz",
                    update_interval = 5,
                ),
                widget.Battery(
                    background=color_main,
                    format='{percent:2.0%} ﯐ {hour:d}:{min:02d}',
                    update_interval = 5,
                    padding=-1,
                ),
                widget.TextBox(
                    text = '  ',
                    background = color_main,
                    padding = 0,
                    fontsize = 16,
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
                    text = ' ',
                    background = color_main,
                    padding = 0,
                    fontsize = 16,
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("tilix -e alsamixer -V all")},
                ),
                widget.Volume(
                    background=color_main,
                    step=1,
                    update_interval=2,
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("tilix -e alsamixer -V all")},
                ),
                widget.TextBox(
                    text = ' ',
                    background = color_main,
                    padding = 0,
                    fontsize = 16,
                ),
                widget.Clock(
                    background=color_main,
                    format='%H:%M - %d/%m ',
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

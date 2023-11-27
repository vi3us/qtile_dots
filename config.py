from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from os.path import expanduser

mod = "mod4"
terminal = "kitty"
file_manger = "nemo"
browser = "firefox"
icons = "~/.config/qtile/icons/"
auto_minimize = False

import os
import subprocess
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "j", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "k", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "i", lazy.layout.up(), desc="Move focus up"),
    Key(["mod1"], "Tab", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "j", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "i", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "j", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "k", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "i", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack",),
    Key([mod], "Return", lazy.spawn("kitty --config .config/qtile/kitty/kitty.conf "), desc="Launch terminal"),
    Key([mod], "f", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "e", lazy.spawn(file_manger), desc="Launch file manager"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -config ~/.config/qtile/rofi/config.rasi -show drun -icon-theme \"Papirus\" -show-icons "), desc="Spawn a command using a prompt widget"),
    
    Key([], "XF86MonBrightnessUp", lazy.spawn(expanduser("~/.config/qtile/dunst/scripts/brightness up"),shell=True)),
    Key([], "XF86MonBrightnessDown", lazy.spawn(expanduser("~/.config/qtile/dunst/scripts/brightness down"),shell=True)),
    
    Key([], "XF86AudioLowerVolume", lazy.spawn(expanduser("~/.config/qtile/dunst/scripts/volume down"),shell=True)),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(expanduser("~/.config/qtile/dunst/scripts/volume up"),shell=True)),
    Key([], "XF86AudioMute", lazy.spawn(expanduser("~/.config/qtile/dunst/scripts/volume mute"),shell=True)),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause player"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Skip to next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Skip to previous"),

    Key([mod, "mod1"], "l", lazy.spawn("betterlockscreen -l"), desc="lock screen"),
    Key(["control", "shift"], "Escape", lazy.spawn("xkill"), desc="xkill"),


]

groups = [Group(f"{i+1}", label="◉") for i in range(4)]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

nord_col_1 = "2e3440"
nord_col_2 = "3b4252"
nord_col_3 = "434c5e"
nord_col_4 = "5d6f9e"

layouts = [
    layout.Columns(
        margin=5,
        margin_on_single=5,
        border_width=2,
        border_focus = "#FFFFFF",
        border_normal=nord_col_1,
        border_on_single=False
    ),
    layout.Max(),
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
    font="Source Code Pro bold",
    fontsize=17,
    padding=15,
)
extension_defaults = widget_defaults.copy()

def batteryStatus():
    status = (os.popen('cat /sys/class/power_supply/BAT0/status')).read()
    if status == "Discharging\n":
        charge = int((os.popen('cat /sys/class/power_supply/BAT0/capacity')).read().replace("\n", ""))
        if charge<=33:
            return icons + "battery-low.svg"
        elif charge >33 and charge <=66:
            return icons + "battery-mid.svg"
        else:
            return icons + "battery-full.svg"
    else:
        return icons + "battery-charging.svg"

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(
                    length=25,
                    background=nord_col_1,
                ),
                widget.Image(
                    filename = icons + "arch.svg",
                    background=nord_col_1,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("nitrogen --random Pictures/.walls/myWalls/nordic/ --set-zoom-fill")},
                ),
                widget.WindowName(
                    background=nord_col_1,
                    max_chars = 30,
                ),
                widget.Spacer(
                    background=nord_col_1,
                ),
                widget.GroupBox(
                    padding=0,
                    fontsize=23,
                    borderwidth=15,
                    highlight_method='text',
                    active=nord_col_4,
                    inactive=nord_col_2,
                    background=nord_col_1,
                    this_current_screen_border='#FFFFFF',
                    urgent_border='#353446',
                    rounded=True,
                    disable_drag=True,
                ),
                widget.Spacer(
                    background=nord_col_1,
                ),
                widget.Image(
                    filename = batteryStatus(),
                    background=nord_col_1,
                ),
                widget.Battery(
                    background=nord_col_1,
                    format='{char} {percent:2.0%} {hour:d}:{min:02d}'
                ),
                widget.Image(
                    filename = icons + "calendar.svg",
                    background=nord_col_1,
                ),
                widget.Clock(
                    format="%a, %b %d",
                    background=nord_col_1,
                ),
                widget.Image(
                    filename = icons + "clock.svg",
                    background=nord_col_1,
                ),
                widget.Clock(
                    format="%H:%M",
                    background=nord_col_1,
                ),
                widget.Systray(
                    background=nord_col_1,
                    icon_size=25
                ),
                widget.Spacer(
                    length=25,
                    background=nord_col_1,
                ),
            ],
            25,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_focus="#FFFFFF",
    border_normal=nord_col_1,
    border_width=2,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

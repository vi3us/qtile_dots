#!/bin/sh
nitrogen --restore &
picom -b --config ~/.config/qtile/picom/picom.conf &
/usr/lib/mate-polkit/polkit-mate-authentication-agent-1 &
udiskie -A -s -n &
dunst -config ~/.config/qtile/dunst/dunstrc &
volctl -h &
blueman-applet &
nm-applet &
kdeconnect-indicator &

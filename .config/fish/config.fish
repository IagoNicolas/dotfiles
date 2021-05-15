set fish_greeting
~/.config/pacman
# Alias to clear and print colors.
alias clear="clear && ~/.config/pacman"
# Alias to color and format ls (exa).
alias ls="exa -lhF --color=auto"
# Alias to call python black format tool.
alias black="python -m black"
# Aliases to flash android devices.
alias fastboot="sudo fastboot"
alias adb="sudo adb"
# Alias to bluetoothctl.
alias bt="bluetoothctl"
# Set starship prompt on fish shell.
starship init fish | source
# Don't stress, my man, use this and chill.
alias relax="mpv ~/Music/* --shuffle"
# Alias for file management.
alias cp="cp -i"
alias mv="mv -i"
alias rm="rm -i"
# Devour rules.
alias zathura="devour zathura"
alias mpvd="devour mpv"
alias qbittorrent="devour qbittorrent"
alias obs="devour obs"

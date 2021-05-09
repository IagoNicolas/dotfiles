set fish_greeting
~/.config/pacman
# Alias to clear and print colors.
alias clear="clear && ~/.config/pacman"
# Alias to color and format ls (exa).
alias ls="exa -lh --color=auto"
# Alias to call python black format tool.
alias black="python -m black"
# Aliases to flash android devices.
alias fastboot="sudo fastboot"
alias adb="sudo adb"
# Alias to bluetoothctl.
alias bt="bluetoothctl"
# Alias to launch emacs in terminal.
alias emacs="emacs -nw"
# Set starship prompt on fish shell.
starship init fish | source
# Don't stress, my man, use this and chill.
alias relax="mpv ~/Music/* --shuffle"
# Devour rules.
alias zathura="devour zathura"
alias mpvd="devour mpv"
alias qbittorrent="devour qbittorrent"

set fish_greeting
~/.config/pacman
# Alias to clear and print colors.
alias clear="clear && ~/.config/pacman"
# Alias to color and format ls (exa).
alias ls="exa -lh --color=auto"
# Alias to call python black format tool.
alias black="python -m black"
# Alias to use common nmcli terms.
alias wifi="nmcli device wifi"
# Aliases to flash android devices.
alias fastboot="sudo fastboot"
alias adb="sudo adb"
# Pacman alias
alias pacman="sudo pacman"
# Set starship prompt on fish shell.
starship init fish | source

set fish_greeting
~/.config/pacman
# Alias to clear and print colors.
alias clear="clear && ~/.config/pacman"
# Alias to color and format ls (exa).
alias l="exa -lhF --color=auto"
alias ls="exa -lhF --color=auto"
alias ll="exa -lahF --color=auto"
# Alias to navigate backwards.
alias ..="cd .."
alias .="cd ."
# Alias to call python programs.
alias black="python -m black"
# Aliases to flash android devices.
alias fastboot="sudo fastboot"
alias adb="sudo adb"
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
alias spyder="devour python ~/.local/lib/python3.9/site-packages/spyder/app/start.py"
alias quartus="devour ~/intelFPGA_lite/20.1/quartus/bin/quartus"

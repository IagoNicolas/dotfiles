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
# Alias to call stm32 programmer.
alias stm32="/home/necronzero/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI"
# Alias to call quartus FPGA programming.
alias quartus="/home/necronzero/.intelFPGA_lite/20.1/quartus/bin/quartus"
# Alias to call emacs inside the terminal.
alias emacs="emacs -nw"
# Enable micro editor truecolor mode.
set -x MICRO_TRUECOLOR 1
set -x WEBKIT_DISABLE_COMPOSITING_MODE 1
# Set starship prompt on fish shell.
starship init fish | source
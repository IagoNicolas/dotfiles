set fish_greeting
# Alias to show neofetch whenever it starts.
neofetch
# Alias to show neofetch whenever clear is called.
alias clear="clear && neofetch"
# Alias to color, format and replace ls with exa.
alias ls="exa -lh --color=auto"
# Alias to call python black code format tool.
alias black="python -m black"
# Alias to call stm32 programmer.
alias stm32="/home/necronzero/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI"
# Enable micro editor truecolor mode.
set -x MICRO_TRUECOLOR 1
set -x WEBKIT_DISABLE_COMPOSITING_MODE 1
# Set starship prompt on fish shell.
starship init fish | source

#!/bin/env fish

function open
  man ./brother-asiryk.1
end

function format
  mandoc -Tlint ./brother-asiryk.1
end

function format_license
  fmt --width 80 ./LICENSE > ./LICENSE-tmp
  mv ./LICENSE-tmp ./LICENSE
end

set -l args (fish_opt --short=o --long=open) \
             (fish_opt --short=f --long=format) \
              (fish_opt --short=l --long=license)

argparse $args -- $argv

if set -q _flag_open
    open
end

if set -q _flag_format
    format
end

if set -q _flag_license
    format_license
end

if not set -q _flag_open; and not set -q _flag_format; and not set -q _flag_license
    echo "Usage: brother.fish [--open|-o] [--format|-f]"
end

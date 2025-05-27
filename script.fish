#!/bin/env fish

function open
  man ./brother-asiryk.1
end

function format
  mandoc -Tlint ./brother-asiryk.1
end

set -l args (fish_opt --short=o --long=open) \
             (fish_opt --short=f --long=format)

argparse $args -- $argv

if set -q _flag_open
    open
end

if set -q _flag_format
    format
end

if not set -q _flag_open; and not set -q _flag_format
    echo "Usage: brother.fish [--open|-o] [--format|-f]"
end

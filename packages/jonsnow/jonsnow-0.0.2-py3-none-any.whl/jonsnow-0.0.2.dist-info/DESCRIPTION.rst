
jonsnow: Run commands on changes to any file in this directory

Usage: 
   jonsnow ./fight_white_walkers.sh
   jonsnow -r ../ echo "You know nothing..."

Arguments:
-r, --root PATH: specify the root directory you want jonsnow to format.
                 Defaults to the current working directory.
--rtp PATH:      Set the runtime path of the command you want to execute
--poll INT       Set the polling frequency (how often to check for changes)
-h, --help:      Show this message



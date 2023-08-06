
jonsnow is a tool to make running unit tests, etc. easier. Run it in a separate
terminal from where you're doing your editing and it will run an arbitrary shell
comand whenever you change a file in a specified directory.

Usage: 
   jonsnow ./fight_white_walkers.sh
   jonsnow -r ../ echo "You know nothing..."

Arguments:
-r, --root PATH: specify the root directory you want {} to format.
                 Defaults to the current working directory.
--rtp PATH: Set the runtime path of the command you want to execute



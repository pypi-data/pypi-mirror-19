"""
simplefc (simple flash card)

Usage:
  simplefc [-h | --help]
  simplefc [-v | --version]
  simplefc create_set <setname>
  simplefc add_entry <setname> (-M <entry>... | -F <file>...)
  simplefc study [-tdbamfsr] <setname>
  simplefc view_set <setname>
  simplefc view_archive <setname>
  simplefc unarchive <setname> <ID>...
  simplefc delete_entry <setname> <ID>...
  simplefc list_sets
  simplefc delete_set <setname>
  simplefc reset_data <setname>

Arguments:
  <setname>      The name of a simplefc flashcard set. Cannot 
                 contain spaces or special characters. Must begin 
                 with a letter. Use '.' in place of a setname with 
                 the 'study' command to study all sets at once.
  <entry>        An entry of the form 'term;;definition'.
  <file>         A text file containing unquoted entries of the 
                 above form. Each entry must have its own line.
  <ID>           The identification number of an entry.

Options:
  -h --help      Show this page.
  -v --version   Show version.
  -M             Add entries manually.
  -F             Add entries from a file.
  -t             Study terms.
  -d             Study definitions.
  -b             Study with randomized terms and definitions.
  -a             'All' - Include all entries.
  -m             'Many' - Exclude easy entries (those with 
                 correct:incorrect ratio >= 2). 
  -f             'Few' - Include only hard entries (those with 
                 correct:incorrect ratio <= 0.75).
  -s             Go through entries sequentially (in the order 
                 they were recorded).
  -r             Go through entries in random order.


Examples:
  simplefc create_set 'biology_450_final'
  simplefc add_entry biology 450 final -I 'xanthophyll;;a yellow or brown carotenoid pigment found in plants' 'anthocyanin;;a red flavonoid pigment found in plants'
  simplefc study -bmr biology 450 final
  simplefc delete_entry biology_450_final 1 2 7 9

Help:
  For help using this tool, please open an issue on Github:
  https://github.com/vlahm/simplefc
"""

from inspect import getmembers, isclass
from docopt import docopt
from . import __version__ as VERSION

def main():
    """Main CLI entrypoint."""
    import simplefc.commands
    options = docopt(__doc__, version=VERSION)

    for k, v in options.items():
        if hasattr(simplefc.commands, k) and v:
            module = getattr(simplefc.commands, k)
            simplefc.commands = getmembers(module, isclass)
            command = [command[1] for command in simplefc.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()

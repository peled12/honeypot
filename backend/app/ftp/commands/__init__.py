from .user import UserCommand
from .pass_cmd import PassCommand
from .stor import StorCommand
from .quit import QuitCommand
from .cwd import CwdCommand
from .syst import SystCommand
from .opts import OptsCommand

# command registry
COMMANDS = {
    "USER": UserCommand(),
    "PASS": PassCommand(),
    "STOR": StorCommand(),
    "QUIT": QuitCommand(),
    "SYST": SystCommand(),
    "CWD": CwdCommand(),
    "OPTS": OptsCommand()
}

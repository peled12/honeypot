from .user import UserCommand
from .pass_cmd import PassCommand
from .stor import StorCommand
from .quit import QuitCommand
from .cwd import CwdCommand
from .pwd import PwdCommand
from .type import TypeCommand
from .pasv import PasvCommand
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
    "PWD": PwdCommand(),
    "TYPE": TypeCommand(),
    "PASV": PasvCommand(),
    "OPTS": OptsCommand()
}

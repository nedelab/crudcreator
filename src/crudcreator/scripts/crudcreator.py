import sys
from .init_project.init_project import init_project, init_project_create_parser
import argparse
from enum import Enum

class ActionType(Enum):
    init: str = "init"

def crudcreator():
    parser = argparse.ArgumentParser(
        prog="CRUDCreator utilities",
        description="CRUDCreator scripts"
    )
    #parser.add_argument("action_type", choices=[action_type.value for action_type in ActionType])

    subparsers = parser.add_subparsers()
    init_project_create_parser(subparsers)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    crudcreator()
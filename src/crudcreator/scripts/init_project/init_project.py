import shutil
import os
import sys
from enum import Enum
import argparse

class ProjectType(Enum):
    simple: str = "simple"

def init_project_create_parser(subparsers):
    parser: argparse.ArgumentParser = subparsers.add_parser(
        name="init",
        description="Create a new CRUDCreator project"
    )
    parser.add_argument("project_type", choices=[project_type.value for project_type in ProjectType])
    parser.set_defaults(func=init_project)

def init_project(args):
    print("Copying files ...")
    shutil.copytree(
        os.path.join(os.path.dirname(__file__), "..", "..", "docs", "source", "examples", args.project_type), 
        ".",
        dirs_exist_ok=True
    )
    print("Files copied.")
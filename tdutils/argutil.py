"""
Utility to create an argparser with predefined arguments. 
https://docs.python.org/3/library/argparse.html#module-argparse
"""
import argparse
import yaml

import pdb


def get_arg_defs(path):
    with open(path, "r") as fin:
        return eval(fin.read())


def get_parser(prog, description, config_path, *args):
    """
    Return a parser with the specified arguments. Each arg
    in *args must be defined in arg_defsff.
    """
    arg_defs = get_arg_defs(config_path)
    
    parser = argparse.ArgumentParser(prog=prog, description=description)

    for arg_name in args:
        arg_def = arg_defs[arg_name]

        if arg_def.get("flag"):
            parser.add_argument(arg_name, arg_def.pop("flag"), **arg_def)
        else:
            parser.add_argument(arg_name, **arg_def)

    return parser


if __name__ == "__main__":
    # tests
    name = "fake_program.py"
    description = "Fake program which does nothing useful."

    parser = get_parser(
        name,
        description,
        '_arguments.py',
        "dataset",
        "device_type",
        "app_name",
        "eval_type",
        "--destination",
        "--replace",
        "--json",
        "--last_run_date"
    )
    
    print(
        parser.parse_args([
            "cameras",
            "gridsmart",
            "data_tracker_prod",
            "traffic_signal",
            "-d",
            "socrata",
            "--replace",
            "--json",
            "--last_run_date",
            "1535997869"
        ])
    )

    print("\nSuccess!\n")




    
"""
Utility to create an argparser with predefined arguments. 
https://docs.python.org/3/library/argparse.html#module-argparse
"""
from argparse import ArgumentParser
import pdb


class ArgParseConfig(ArgumentParser):
    """
    Extends argparse.ArgumentParser to accept an argument configuration dict.
    """
    def __init__(self, config: [dict], **kwargs):
        super().__init__(**kwargs)

        self.config = config

    def config_args(self, *args):
        for arg_name in args:
            arg_def = self.config.get(arg_name)

            if not arg_def:
                raise Exception(f"Argument \"{arg_name}\"  not found in config.")


            if arg_def.get("flag"):
                self.add_argument(arg_name, arg_def.pop("flag"), **arg_def)
            else:
                self.add_argument(arg_name, **arg_def)

        return self



if __name__ == "__main__":
    NAME = "fake_program.py"
   
    DESCRIPTION = "Fake program which does nothing useful."

    ARG_CONFIG =  {
        "dataset": {
            "action": "store",
            "type": str,
            "help": "Name of the dataset that will be published. Must match entry in Knack config file.",
        }
    }

    parser = ArgParseConfig(ARG_CONFIG, prog=NAME, description=DESCRIPTION)
    parser.config_args("dataset")
    parsed = parser.parse_args()
    print(parsed)
    print("\nSuccess!\n")




    
"""
Utility to create an argparser with predefined arguments. 
https://docs.python.org/3/library/argparse.html#module-argparse
"""
from tdutils import argutil


if __name__ == "__main__":
    # tests
    name = "fake_program.py"
    description = "Fake program which does nothing useful."

    parser = argutil.get_parser(
        name,
        description,
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




    
#!/bin/python3
#  Author: gvenzl
#  Since: July 2024
#  Name: main.py
#  Description: The program that renames file names to their creation date and time.
#
#  MIT License
#
#  Copyright (c) 2024 Gerald Venzl
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
import argparse
import os
import sys
from datetime import datetime


def run(cmd):

    args = parse_arguments(cmd)

    if args.simulate:
        print("Simulating...")

    # Files need to be written to a new directory,
    # otherwise "scandir" (or "listdir") may include the
    # newly renamed files in the results
    new_location = args.directory + "/new/"
    # Create new location if it doesn't exist and this is not a simulation run
    if not os.path.exists(new_location) and not args.simulate:
        print("Creating new location")
        os.makedirs(new_location)

    # Iterate through the directory
    with os.scandir(args.directory) as it:
        # For each entry in the directory
        for entry in it:
            # Ignore any directories and hidden files (do not use recursion)
            if entry.is_file() and not entry.name.startswith("."):
                org_file_name = args.directory + "/" + entry.name
                name, ext = os.path.splitext(org_file_name)
                create_date = datetime.fromtimestamp((os.path.getmtime(entry.path))).strftime("%Y-%m-%d %H.%M.%S")
                new_file_name = new_location + create_date + ext
                # Check whether file already exists
                file_exists = True
                version = 0
                while file_exists:
                    # If file already exists, add a "-1" at the end of the name and check again
                    if os.path.isfile(new_file_name):
                        version = version + 1
                        new_file_name = new_location + create_date + "-" + str(version) + ext
                    else:
                        file_exists = False
                # Print old to new name
                print("Renaming {} --> {}".format(org_file_name, new_file_name))
                if not args.simulate:
                    os.rename(org_file_name, new_file_name)


def parse_arguments(cmd):
    """Parses the arguments.

    Parameters
    ----------
    cmd : str array
        The arguments passed

    Returns
    -------
    arg
        Argparse object
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Renames the files to their create date and time.\n(c) Gerald Venzl"
    )

    parser.add_argument("-d", "--directory", default=".",
                        help="The path to the directory containing the files.")
    parser.add_argument("-s", "--simulate", action="store_true",
                        default=False, help="Simulates the rename operation and does not actually rename any files.")

    return parser.parse_args(cmd)


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))

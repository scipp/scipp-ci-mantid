import argparse
import subprocess as sp
import os
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs docker for testing "
                                                 "scipp against Mantid")
    parser.add_argument("--image_name", type=str, default="scipp_vs_mantid",
                        help="the name of the image to start")

    test_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "tests")
    args = parser.parse_args()
    command = "docker run -u jenkins -v {}:/opt/tests {}".format(
        test_folder, args.image_name)
    sys.exit(sp.run(command, shell=True).returncode)

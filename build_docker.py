import argparse
import subprocess as sp
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Buids docker immage for "
                                                 "testing scipp against "
                                                 "Mantid")
    parser.add_argument("--image_name", type=str, default="scipp_vs_mantid",
                        help="the name of the image to start")

    args = parser.parse_args()
    docker_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "Docker")
    command = "docker build -t {} {}".format(args.image_name, docker_path)
    sp.run(command, check=True, shell=True)

import argparse
import subprocess as sp
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Buids docker image for "
                                                 "testing scipp against "
                                                 "Mantid")
    parser.add_argument("--image_name", type=str, default="scipp_vs_mantid",
                        help="the name of the image to start")
    parser.add_argument("--http_proxy", action="store_true",
                        help="use the http_proxy from the environment")
    parser.add_argument("--https_proxy", action="store_true",
                        help="use the https_proxy from the environment")
    parser.add_argument("--rebuild", action="store_true",
                        help="remove existing image with the same name")
    args = parser.parse_args()

    docker_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "Docker")
    if args.rebuild:
        command = "docker image inspect {}".format(args.image_name)
        if sp.run(command, shell=True).returncode == 0:
            command = "docker rmi -f {}".format(args.image_name)
            sp.run(command, check=True, shell=True)

    command = "docker build -t {}".format(args.image_name)
    if args.http_proxy:
        command = "{} --build-arg http_proxy".format(command)
    if args.https_proxy:
        command = "{} --build-arg https_proxy".format(command)
    print("command = ", command)
    command = "{} {}".format(command, docker_path)
    sp.run(command, check=True, shell=True)

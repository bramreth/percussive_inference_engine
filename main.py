import input_handler
import argparse


def init():
    parser = argparse.ArgumentParser(description="process a wav file and generate creative percussion")
    parser.add_argument("target", metavar="T", type=str, help="the wav file for processing")
    parser.add_argument("--test", dest="test", action="store_true", help="set the generator to test mode.")
    args = parser.parse_args()
    handler = input_handler.InputHandler(args)


# initialise the input handler
init()

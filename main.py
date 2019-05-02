import input_handler, graph_builder, verse_detector
import argparse


def init():
    parser = argparse.ArgumentParser(description="process a wav file and generate creative percussion")
    parser.add_argument("target", metavar="T", type=str, help="the wav file for processing")
    parser.add_argument("--test", dest="test", action="store_true", help="set the generator to test mode.")
    parser.add_argument("--view", dest="view", action="store_true", help="use view mode to see the chroma pattern for your input.")
    parser.add_argument("-s", "--structure", type=str, help="the path for your song structure")
    args = parser.parse_args()
    handler = input_handler.InputHandler(args)

    if handler.view:
        # pass the stereo audio to the graphing tool
        builder = graph_builder.graph_builder(handler.get_audio(), handler.get_params(), handler.get_filter())


# initialise the input handler
init()

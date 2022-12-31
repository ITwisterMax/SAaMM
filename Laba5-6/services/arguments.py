import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process input values')

    parser.add_argument('lmbd', type=float, help='Intensity of claim generated')
    parser.add_argument('mu', type=float, help='Intensity of channel process')
    parser.add_argument('n', type=int, help='Count of channels')

    return parser.parse_args()

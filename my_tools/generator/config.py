import argparse


def get_parameters():
    parser = argparse.ArgumentParser()

    parser.add_argument("--imsize", type=int, default=128)
    parser.add_argument("--n_samples", type=int, default=100)
    parser.add_argument("--save_to", type=str, default="../../my_dataset/train")

    return parser.parse_args()

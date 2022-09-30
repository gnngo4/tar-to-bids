"""Run tar-to-bids"""
import argparse

from src.heuristics.utils import HEURISTIC_DIR

def _setup_parser():
    """
    Set-up Python's ArgumentParser with tar, subject, session, and other options
    """
    parser = argparse.ArgumentParser()

    # Basic arguments
    parser.add_argument(
        '--tar',
        required=True,
        help='Input dicom tar file. This can be obtained using cfmm2tar'
    )

    parser.add_argument(
        '--subject',
        required=True,
        type=str,
        help='Input subject id.'
    )

    parser.add_argument(
        '--session',
        required=True,
        type=str,
        help='Input session id.'
    )

    parser.add_argument(
        '--heuristic',
        required=True,
        type=str,
        help=f'Input the heuristics used to map the DICOM files, relative to {HEURISTIC_DIR}'
    )

    return parser

def main():
    """
    Convert tar file into a bids folder

    Sample command
    ```
    pass
    ```


    """
    parser = _setup_parser()
    args=parser.parse_args()

    print(args)

if __name__ == "__main__":
    main()


import argparse

from src.heuristics.utils import HEURISTIC_DIR

from src.parser.action import CheckTarMappings

def setup_parser():
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

    parser.add_argument(
        '--check_tar_mappings',
        default=None,
        type=str,
        help=f'Input tar file and retrieve subject/session/task_csv mappings',
        action=CheckTarMappings
    )

    parser.add_argument(
        '--task_mappings',
        type=str,
        help=f''
    )

    parser.add_argument(
        '--output_dir',
        default='./bids',
        type=str,
        help=f'Input the output directory (default: ./bids)'
    )

    return parser
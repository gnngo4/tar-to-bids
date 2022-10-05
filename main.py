"""Run tar-to-bids"""
import argparse, os

from src.heuristics.utils import HEURISTIC_DIR

from src.cfmm_tar.cfmm_tar import cfmm_tar

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

    parser.add_argument(
        '--output_dir',
        default='./bids',
        type=str,
        help=f'Input the output directory (default: ./bids)'
    )

    return parser

def call_heudiconv(
        tar_dir,
        out_dir,
        heuristic_py,
        subject,
        session
    ):

    import subprocess
    cmd = f"heudiconv -d {tar_dir}/*/*/*/{{subject}}_{{session}}/*/*/*.dcm -o {out_dir} -f {heuristic_py} -s {subject} -ss {session} -c dcm2niix -b --minmeta --overwrite"
    output = f"{out_dir}/log.txt"
    subprocess.run(cmd,shell=True)

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

    reformat = f"{args.subject}_{args.session}"

    # Extract tar file
    tar_obj = cfmm_tar(args.tar)
    tar_obj.extract()
    tar_obj.reformat_dicom_tree(reformat)

    # heudiconv
    heuristic = os.path.join('/opt/tar-to-bids/src/heuristics',args.heuristic)
    assert os.path.exists(heuristic), f"{heuristic} does not exist."
    call_heudiconv(tar_obj.tar_dir,args.output_dir,heuristic,args.subject,args.session)

    """
    heudiconv does not read physio dicoms, so editing heuristics does not retrieve them.
    The current solution parses tar outputs manually to identify MRI-physio pairs.
    """
    physio_pairs = tar_obj.get_physio_pairs()
    tar_obj.pair_physio_to_mri(physio_pairs,args.subject,args.session,args.output_dir)

    # cleanup
    tar_obj.cleanup()

if __name__ == "__main__":
    main()

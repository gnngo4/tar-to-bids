"""Run tar-to-bids"""
import argparse, os

from src.heuristics.utils import HEURISTIC_DIR

from src.cfmm_tar.cfmm_tar import cfmm_tar
from src.parser.setup_parser import setup_parser

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
    
    # Get argparse arguments
    parser = setup_parser()
    args=parser.parse_args()

    # Make bids directory, if it does not exist
    if not os.path.isdir(args.output_dir): os.mkdir(args.output_dir)

    # Extract tar file
    tar_obj = cfmm_tar(args.tar)
    tar_obj.extract()
    '''
    Relabel dicom directory tree with `reformat`. This allows heudiconv to more easily
    read {subject} and {session} info enabling robust bids labeling of each tar file.
    The tradeoff is that `tar-to-bids` requires specifying `subject` and `session`
    with argparse.
    '''
    reformat = f"{args.subject}_{args.session}" # Relabel dicom 
    tar_obj.reformat_dicom_tree(reformat)

    # heudiconv
    heuristic = os.path.join(HEURISTIC_DIR,args.heuristic)
    assert os.path.exists(heuristic), f"{heuristic} does not exist."
    call_heudiconv(tar_obj.tar_dir,args.output_dir,heuristic,args.subject,args.session)

    # Save physio dcms
    """
    heudiconv does not read physio dicoms (they are not stored in .dicomtsv files).
    This means that editing heuristics will not retrieve them. The current solution
    parses tar outputs manually to identify MRI-physio pairs.
    """
    physio_pairs = tar_obj.get_physio_pairs()
    tar_obj.pair_physio_to_mri(physio_pairs,args.subject,args.session,args.output_dir)

    # cleanup
    tar_obj.cleanup()

if __name__ == "__main__":
    main()

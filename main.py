"""Run tar-to-bids"""
import argparse, os, sys

from src.heuristics.utils import HEURISTIC_DIR
from src.cfmm_tar.cfmm_tar import cfmm_tar
from src.parser.setup_parser import setup_parser
from src.csv_reader.tar_mapper import task_mapper

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

    # Check if session is already run
    subject_session_dir = f"{args.output_dir}/sub-{args.subject}/ses-{args.session}"
    assert not os.path.isdir(subject_session_dir), f"Remove (1) {subject_session_dir} to re-run, and (2) {args.output_dir}/.heudiconv/{args.subject}/ses-{args.session}."

    # Check for post-processing module associated to the specified heuristic.
    run_post_processing = args.task_mappings is not None or args.post_process
    if run_post_processing:
        post_process_module = f"src.heuristics_post.{args.heuristic.replace('.py','')}"
        try:
            from importlib import import_module
            post_process = import_module(f"{post_process_module}")
        except:
            print(f"{post_process_module} does not exist.\nExiting.\n")
            sys.exit(0)

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

    # heudiconv post-processing
    if run_post_processing:
        if args.task_mappings is None: post_process.heudiconv_post_process(tar_obj.tar_tree,args.subject,args.session,args.output_dir,args.heuristic,args.task_mappings)
        else: post_process.heudiconv_post_process(tar_obj.tar_tree,args.subject,args.session,args.output_dir,args.heuristic,"")

    # cleanup
    tar_obj.cleanup()

if __name__ == "__main__":
    main()

"""Run tar-to-bids"""
import os
import sys
from pathlib import Path

from src.heuristics.utils import HEURISTIC_DIR
from src.cfmm_parser.cfmm_tar import cfmm_tar
from src.cfmm_parser.cfmm_zip import cfmm_zip
from src.parser.setup_parser import setup_parser


def call_heudiconv(tar_dir, out_dir, heuristic_py, subject, session):
    import subprocess

    cmd = (
        "heudiconv -d"
        f" {tar_dir}/*/*/*/{{subject}}_{{session}}/*/*/*.dcm -o"
        f" {out_dir} -f {heuristic_py} -s {subject} -ss {session} -c"
        " dcm2niix -b --minmeta --overwrite"
    )
    subprocess.run(cmd, shell=True)


def call_heudiconv_zip(
    tar_dir, out_dir, heuristic_py, subject, session
):
    import subprocess

    cmd = (
        "heudiconv -d"
        f" {tar_dir}/*/*/{{subject}}_{{session}}/*/*/*.dcm -o"
        f" {out_dir} -f {heuristic_py} -s {subject} -ss {session} -c"
        " dcm2niix -b --minmeta --overwrite"
    )
    subprocess.run(cmd, shell=True)


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
    args = parser.parse_args()

    # Make bids directory, if it does not exist
    output_dir = Path(args.output_dir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    # Check if session is already run
    subject_session_dir = (
        f"{args.output_dir}/sub-{args.subject}/ses-{args.session}"
    )
    assert not os.path.isdir(subject_session_dir), (
        f"Remove (1) {subject_session_dir} to re-run, and (2)"
        f" {args.output_dir}/.heudiconv/{args.subject}/ses-{args.session}."
    )

    # Check for post-processing module associated to the specified heuristic.
    run_post_processing = (
        args.task_mappings is not None or args.post_process
    )
    if run_post_processing:
        post_process_module = (
            f"src.heuristics_post.{args.heuristic.replace('.py','')}"
        )
        try:
            from importlib import import_module

            post_process = import_module(f"{post_process_module}")
        except:
            print(
                f"{post_process_module} does not exist.\nExiting.\n"
            )
            sys.exit(0)

    # Extract tar file
    tar_path = Path(args.tar)
    file_extension = tar_path.suffix
    """
    Relabel dicom directory tree with `reformat`. This allows heudiconv to more easily
    read {subject} and {session} info enabling robust bids labeling of each tar file.
    The tradeoff is that `tar-to-bids` requires specifying `subject` and `session`
    with argparse.
    """
    if file_extension == ".tar":
        tar_obj = cfmm_tar(args.tar)
        tar_obj.extract()
        reformat = f"{args.subject}_{args.session}"  # Relabel dicom
        tar_obj.reformat_dicom_tree(reformat)
        # heudiconv
        heuristic = os.path.join(HEURISTIC_DIR, args.heuristic)
        assert Path(
            heuristic
        ).exists(), f"{heuristic} does not exist."
        call_heudiconv(
            tar_obj.tar_dir,
            args.output_dir,
            heuristic,
            args.subject,
            args.session,
        )
        # heudiconv post-processing
        if run_post_processing:
            if args.task_mappings is not None:
                post_process.heudiconv_post_process(
                    tar_obj.tar_tree,
                    args.subject,
                    args.session,
                    args.output_dir,
                    args.heuristic,
                    args.task_mappings,
                )
            else:
                post_process.heudiconv_post_process(
                    tar_obj.tar_tree,
                    args.subject,
                    args.session,
                    args.output_dir,
                    args.heuristic,
                    "",
                )
        # cleanup
        tar_obj.cleanup()

    elif file_extension == ".zip":
        zip_obj = cfmm_zip(args.tar)
        zip_obj.extract()
        reformat = f"{args.subject}_{args.session}"  # Relabel dicom
        zip_obj.reformat_dicom_tree(reformat)
        # heudiconv
        heuristic = os.path.join(HEURISTIC_DIR, args.heuristic)
        assert Path(
            heuristic
        ).exists(), f"{heuristic} does not exist."
        call_heudiconv_zip(
            zip_obj.zip_dir,
            args.output_dir,
            heuristic,
            args.subject,
            args.session,
        )
        # cleanup
        zip_obj.cleanup()

    else:
        NotImplemented


if __name__ == "__main__":
    main()

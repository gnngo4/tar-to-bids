from src.heuristics_post.physio_base import pair_physio_to_mri


def heudiconv_post_process(
    tar_tree: str,
    subject_id: str,
    session_id: str,
    bids_dir: str,
    heuristic: str,
    task_mapping: str,
):
    pair_physio_to_mri(tar_tree, subject_id, session_id, bids_dir)

"""
3T MPRAGE sequence - provides mapping for a T1w image
"""

from src.heuristics.cfmm_filters.utils import create_key


class mprage:
    def __init__(self, seqinfo):
        self.seqinfo = seqinfo

    def get_info(self):
        # Initialize nifti file names
        mprage = create_key(
            "sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-MPRAGE_run-{item:02d}_T1w"
        )

        # Initialize info: key=create_key() and value=[] for all images
        info = {}
        images = [mprage]
        for image in images:
            info[image] = []

        # Map image key(s) to dicom series_id(s)
        for s in self.seqinfo:
            if "T1_3D" in s.series_description:
                info[mprage].append({"item": s.series_id})

        return info

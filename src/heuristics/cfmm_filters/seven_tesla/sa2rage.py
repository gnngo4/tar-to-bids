"""
7T MP2RAGE sequence - provides mappings for UNI, T1map, INV1, and INV2 images
"""

from src.heuristics.cfmm_filters.utils import create_key


class sa2rage:
    def __init__(self, seqinfo):
        self.seqinfo = seqinfo

    def get_info(self):
        # Initialize nifti file names
        b1map = create_key(
            "sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-b1map_run-{item:02d}_part-mag_TB1SRGE"
        )
        inv1 = create_key(
            "sub-{subject}/{session}/fmap/sub-{subject}_{session}_inv-1_run-{item:02d}_part-mag_TB1SRGE"
        )
        inv2 = create_key(
            "sub-{subject}/{session}/fmap/sub-{subject}_{session}_inv-2_run-{item:02d}_part-mag_TB1SRGE"
        )

        # Initialize info: key=create_key() and value=[] for all images
        info = {}
        images = [b1map, inv1, inv2]
        for image in images:
            info[image] = []

        # Map image key(s) to dicom series_id(s)
        for s in self.seqinfo:
            if "sa2rage" in s.series_description:
                if "UNI_Images" in s.series_description:
                    info[b1map].append({"item": s.series_id})

                if "INV1" in s.series_description and s.image_type[2] == "M":
                    info[inv1].append({"item": s.series_id})

                if "INV2" in s.series_description and s.image_type[2] == "M":
                    info[inv2].append({"item": s.series_id})

        return info

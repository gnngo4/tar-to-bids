"""
3T GRE field map sequence - provides mappings for two magnitude and phasediff images
"""

from src.heuristics.cfmm_filters.utils import create_key


class gre_field_map:
    def __init__(self, seqinfo):
        self.seqinfo = seqinfo

    def get_info(self):
        # Initialize nifti file names
        magnitude = create_key(
            "sub-{subject}/{session}/fmap/sub-{subject}_{session}_magnitude"
        )
        phase_difference = create_key(
            "sub-{subject}/{session}/fmap/sub-{subject}_{session}_phasediff"
        )

        # Initialize info: key=create_key() and value=[] for all images
        info = {}
        images = [magnitude, phase_difference]
        for image in images:
            info[image] = []

        # Map image key(s) to dicom series_id(s)
        for s in self.seqinfo:
            if "gre_field_mapping" in s.series_description:
                if "M" in s.image_type:
                    info[magnitude].append({"item": s.series_id})

                if "P" in s.image_type:
                    info[phase_difference].append({"item": s.series_id})

        return info

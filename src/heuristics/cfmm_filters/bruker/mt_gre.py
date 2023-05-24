"""
9.4T Bruker MT GRE images
"""

from src.heuristics.cfmm_filters.utils import create_key


class mt_gre:
    def __init__(self, seqinfo):
        self.seqinfo = seqinfo

    def get_info(self):
        # Initialize empty info dict: key=create_key() and value=[] for all images
        info = {}
        # Map image key(s) to dicom series_id(s)
        for s in self.seqinfo:
            description = s.series_description.lower()
            if "MT_GRE_3D".lower() in description:
                template = create_key(
                    "sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:02d}_MTR"
                )
            else:
                continue

            try:
                info[template].append({"item": s.series_id})
            except:
                info[template] = [{"item": s.series_id}]

        return info

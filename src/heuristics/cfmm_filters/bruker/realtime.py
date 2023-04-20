"""
9.4T Bruker REALTIME analysis - create dummy outputs
"""
import re

from src.heuristics.cfmm_filters.utils import create_key


class bold:
    def __init__(self, seqinfo):
        self.seqinfo = seqinfo

    def get_info(self):
        # Initialize empty info dict: key=create_key() and value=[] for all images
        info = {}
        # Map image key(s) to dicom series_id(s)
        for s in self.seqinfo:
            description = s.series_description
            alphanumeric_description = re.sub(r"[^a-zA-Z0-9]", "", description)
            template = create_key(
                f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-REALTIME_desc-{alphanumeric_description}_run-{{item:02d}}_bold"
            )

            try:
                info[template].append({"item": s.series_id})
            except:
                info[template] = [{"item": s.series_id}]

        return info

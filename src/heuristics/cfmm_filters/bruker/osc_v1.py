"""
9.4T Bruker GE fast fMRI bold acquisition
"""

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
            if "task-visualblock_res-A" in description:
                template = create_key(
                    "sub-{subject}/{session}/func/sub-{subject}_{session}_task-TEST01VisualBlock_dir-AP_run-{item:02d}_bold"
                )
            elif "task-visualosc_res-A" in description:
                template = create_key(
                    "sub-{subject}/{session}/func/sub-{subject}_{session}_task-TEST01VisualFT_dir-AP_run-{item:02d}_bold"
                )
            elif "task-visualblock_res-B" in description:
                template = create_key(
                    "sub-{subject}/{session}/func/sub-{subject}_{session}_task-TEST02VisualBlock_dir-AP_run-{item:02d}_bold"
                )
            elif "task-visualosc_res-B" in description:
                template = create_key(
                    "sub-{subject}/{session}/func/sub-{subject}_{session}_task-TEST02VisualFT_dir-AP_run-{item:02d}_bold"
                )
            else:
                continue

            try:
                info[template].append({"item": s.series_id})
            except:
                info[template] = [{"item": s.series_id}]

        return info

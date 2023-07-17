"""
9.4T Bruker GE fast fMRI bold acquisition
"""

from src.heuristics.cfmm_filters.utils import create_key


class protocol:
    def __init__(self, seqinfo):
        self.seqinfo = seqinfo

    def get_info(self):
        # Initialize empty info dict: key=create_key() and value=[] for all images
        info = {}
        # Map image key(s) to dicom series_id(s)
        for s in self.seqinfo:
            description = s.series_description.lower()
            if (
                description.startswith("T2star_rsFMRI".lower())
                and "_600" in description
            ):
                template = create_key(
                    "sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_dir-AP_run-{item:02d}_bold"
                )
            elif description.startswith(
                "T2star_rsFMRI".lower()
            ) and description.endswith("SAT".lower()):
                template = create_key(
                    "sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-AP_desc-GE_run-{item:02d}_epi"
                )
            elif description.startswith(
                "T2star_rsFMRI".lower()
            ) and description.endswith("SAT_RV".lower()):
                template = create_key(
                    "sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-PA_desc-GE_run-{item:02d}_epi"
                )
            elif description.startswith("T2_".lower()):
                template = create_key(
                    "sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:02d}_T2w"
                )
            else:
                continue

            try:
                info[template].append({"item": s.series_id})
            except:
                info[template] = [{"item": s.series_id}]

        return info

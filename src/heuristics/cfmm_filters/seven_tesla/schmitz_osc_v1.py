"""
7T MP2RAGE sequence - provides mappings for UNI, T1map, INV1, and INV2 images
"""

import collections

from src.heuristics.cfmm_filters.utils import create_key

part_mappings = {"M": "mag", "P": "phase"}


class bold:
    def __init__(self, seqinfo):
        self.seqinfo = seqinfo

    def get_info(self):
        # Initialize empty info dict: key=create_key() and value=[] for all images
        info = {}

        # Track PE directions of all func scans
        phase_dirs = []
        for s in self.seqinfo:
            description = s.series_description.lower()
            if "mbep2d_bold" in description:
                phase_dir = description.split("_p")[1].split("_")[1][:2].upper()
                phase_dirs.append(phase_dir)

        # Map image key(s) to dicom series_id(s)
        for s in self.seqinfo:
            description = s.series_description.lower()
            if "mbep2d_bold" in description:
                # Scrape info from Series_description of dicom.tsv
                mb_factor = description.split("_mb")[1].split("_")[0]
                in_phase_accel = description.split("_p")[1].split("_")[0]
                phase_dir = description.split("_p")[1].split("_")[1][:2].upper()
                dicom_dir_number = str(s.dcm_dir_name)
                part = part_mappings[s.image_type[2]]
                suffix = (
                    "sbref"
                    if "sbref".lower() in s.series_description.lower()
                    else "bold"
                )

                whole_brain = (
                    True if "wholebrain" in s.series_description.lower() else False
                )

                reverse_phase = (
                    True
                    if (
                        collections.Counter(phase_dirs).most_common(1)[0][0]
                        != phase_dir
                    )
                    and (s.dim4 == 1)
                    else False
                )

                if whole_brain:
                    template = create_key(
                        f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-wholebrain_acq-mb{mb_factor}p{in_phase_accel}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}"
                    )

                elif reverse_phase:
                    if suffix == "sbref" and s.series_files == 1:
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/fmap/sub-{{subject}}_{{session}}_acq-mb{mb_factor}p{in_phase_accel}_dir-{phase_dir}_part-{part}_desc-GEsbref_run-{{item:02d}}_epi"
                        )
                    if suffix == "sbref" and s.series_files != 1:
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/fmap/sub-{{subject}}_{{session}}_acq-mb{mb_factor}p{in_phase_accel}_dir-{phase_dir}_desc-GEsbref_run-{{item:02d}}_epi"
                        )
                    if suffix == "bold" and s.series_files == 1:
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/fmap/sub-{{subject}}_{{session}}_acq-mb{mb_factor}p{in_phase_accel}_dir-{phase_dir}_part-{part}_desc-GEbold_run-{{item:02d}}_epi"
                        )
                    if suffix == "bold" and s.series_files != 1:
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/fmap/sub-{{subject}}_{{session}}_acq-mb{mb_factor}p{in_phase_accel}_dir-{phase_dir}_desc-GEbold_run-{{item:02d}}_epi"
                        )

                else:
                    template = create_key(
                        f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{dicom_dir_number}_acq-mb{mb_factor}p{in_phase_accel}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}"
                    )

                try:
                    info[template].append({"item": s.series_id})
                except:
                    info[template] = [{"item": s.series_id}]

        return info

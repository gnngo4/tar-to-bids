"""
7T MP2RAGE sequence - provides mappings for UNI, T1map, INV1, and INV2 images
"""


from src.heuristics.cfmm_filters.utils import create_key

part_mappings = {"M": "mag", "P": "phase"}


class bold:
    def __init__(self, seqinfo):
        self.seqinfo = seqinfo

    def get_info(self):
        # Initialize empty info dict: key=create_key() and value=[] for all images
        info = {}

        # Map image key(s) to dicom series_id(s)
        for s in self.seqinfo:
            description = s.series_description.lower()
            dicom_dir_number = str(s.dcm_dir_name)
            if "_bold_" in description or description.endswith("_fmap"):
                # Scrape info from Series_description of dicom.tsv
                phase_dir = description.split("_dir-")[1].split("_")[0].upper()
                part = part_mappings[s.image_type[2]]
                suffix = "sbref" if "sbref".lower() in description else "bold"
                wholebrain_flag = True if "desc-wholebrain" in description else False
                fmap_flag = True if "_fmap" in description else False

                if fmap_flag and wholebrain_flag:
                    if suffix == "sbref" and s.series_files == 1:
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-wholebrain_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}"
                        )
                    if suffix == "sbref" and s.series_files == 2:
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-wholebrain_dir-{phase_dir}_run-{{item:02d}}_{suffix}"
                        )
                    if suffix == "bold":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-wholebrain_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}"
                        )

                elif fmap_flag and not wholebrain_flag:
                    if suffix == "sbref":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/fmap/sub-{{subject}}_{{session}}_dir-{phase_dir}_part-{part}_desc-GEsbref_run-{{item:02d}}_epi"
                        )
                    if suffix == "bold":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/fmap/sub-{{subject}}_{{session}}_dir-{phase_dir}_part-{part}_desc-GEbold_run-{{item:02d}}_epi"
                        )

                # Map task events
                elif "task-000" in description:
                    task_event = "test"
                    if suffix == "sbref":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_dir-{phase_dir}_run-{{item:02d}}_{suffix}"
                        )
                    if suffix == "bold":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}"
                        )
                    print(
                        f"MAPPING: [{description}] SERIES-ID"
                        f" ({dicom_dir_number}) -> template"
                    )

                # Non-converted series-ids
                else:
                    print(
                        f"WARNING: [{description}] SERIES-ID"
                        f" ({dicom_dir_number}) WAS NOT SAVED."
                    )
                    continue

                try:
                    info[template].append({"item": s.series_id})
                except:
                    info[template] = [{"item": s.series_id}]

        return info

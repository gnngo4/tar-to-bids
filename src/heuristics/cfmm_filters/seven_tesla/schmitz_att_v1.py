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
            if s.image_type[2] not in [i for i in part_mappings.keys()]:
                continue
            part = part_mappings[s.image_type[2]]
            dicom_dir_number = str(s.dcm_dir_name)

            if "rslh_ep3d_vaso_800iso_rl_E00".lower() in description:
                suffix = "vaso"
                task_event = "wbpilot"
                template = create_key(
                    f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_dir-RL_run-{{item:02d}}_part-{part}_{suffix}"
                )
                print(
                    f"MAPPING: [{description}] SERIES-ID"
                    f" ({dicom_dir_number}) -> template"
                )

                try:
                    info[template].append({"item": s.series_id})
                except:
                    info[template] = [{"item": s.series_id}]

            elif "ep_bold_mb" in description:
                # Scrape info from Series_description of dicom.tsv
                mb_factor = description.split("_mb")[1].split("_")[0]
                phase_dir = description.split("_mb")[1][2:4].upper()
                if phase_dir == "P2":
                    mb_factor = "4p2"
                    phase_dir = description.split("_p2")[1][1:3].upper()
                suffix = (
                    "sbref"
                    if "sbref".lower() in s.series_description.lower()
                    else "bold"
                )

                whole_brain = (
                    True if "wholebrain" in s.series_description.lower() else False
                )

                reverse_phase = True if "rev" in s.series_description.lower() else False

                if whole_brain:
                    if suffix == "sbref" and s.series_files == 1:
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-wholebrain_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}"
                        )
                    if suffix == "sbref" and s.series_files != 1:
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-wholebrain_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}"
                        )
                    if suffix == "bold":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-wholebrain_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}"
                        )

                elif reverse_phase:
                    if suffix == "sbref" and s.series_files == 1:
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/fmap/sub-{{subject}}_{{session}}_acq-mb{mb_factor}_dir-{phase_dir}_part-{part}_desc-GEsbref_run-{{item:02d}}_epi"
                        )
                    if suffix == "sbref" and s.series_files != 1:
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/fmap/sub-{{subject}}_{{session}}_acq-mb{mb_factor}_dir-{phase_dir}_desc-GEsbref_run-{{item:02d}}_epi"
                        )
                    if suffix == "bold" and s.series_files == 1:
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/fmap/sub-{{subject}}_{{session}}_acq-mb{mb_factor}_dir-{phase_dir}_part-{part}_desc-GEbold_run-{{item:02d}}_epi"
                        )
                    if suffix == "bold" and s.series_files != 1:
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/fmap/sub-{{subject}}_{{session}}_acq-mb{mb_factor}_dir-{phase_dir}_desc-GEbold_run-{{item:02d}}_epi"
                        )

                # Map task events

                # PRF
                elif "_c89_" in description:
                    task_event = "prfCCW"
                    if suffix == "sbref":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}"
                        )
                    if suffix == "bold":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}"
                        )
                    print(
                        f"MAPPING: [{description}] SERIES-ID"
                        f" ({dicom_dir_number}) -> template"
                    )
                elif "_c91_" in description:
                    task_event = "prfExpand"
                    if suffix == "sbref":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}"
                        )
                    if suffix == "bold":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}"
                        )
                    print(
                        f"MAPPING: [{description}] SERIES-ID"
                        f" ({dicom_dir_number}) -> template"
                    )
                elif "_c93_" in description:
                    task_event = "prfMultibar"
                    if suffix == "sbref":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}"
                        )
                    if suffix == "bold":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}"
                        )
                    print(
                        f"MAPPING: [{description}] SERIES-ID"
                        f" ({dicom_dir_number}) -> template"
                    )

                # Localizer
                elif "_c117_" in description:
                    task_event = "localizerQ1"
                    if suffix == "sbref":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}"
                        )
                    if suffix == "bold":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}"
                        )
                    print(
                        f"MAPPING: [{description}] SERIES-ID"
                        f" ({dicom_dir_number}) -> template"
                    )

                # Osc
                elif "_c101_" in description:
                    task_event = "AttendInF1Q1"
                    if suffix == "sbref":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}"
                        )
                    if suffix == "bold":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}"
                        )
                    print(
                        f"MAPPING: [{description}] SERIES-ID"
                        f" ({dicom_dir_number}) -> template"
                    )
                elif "_c105_" in description:
                    task_event = "AttendInF2Q1"
                    if suffix == "sbref":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}"
                        )
                    if suffix == "bold":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}"
                        )
                    print(
                        f"MAPPING: [{description}] SERIES-ID"
                        f" ({dicom_dir_number}) -> template"
                    )
                elif "_c113_" in description:
                    task_event = "AttendAwayQ1"
                    if suffix == "sbref":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}"
                        )
                    if suffix == "bold":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}"
                        )
                    print(
                        f"MAPPING: [{description}] SERIES-ID"
                        f" ({dicom_dir_number}) -> template"
                    )

                elif "_c000" in description:
                    task_event = "slpilot"
                    if suffix == "sbref":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_dir-RL_run-{{item:02d}}_{suffix}"
                        )
                    if suffix == "bold":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_dir-RL_run-{{item:02d}}_part-{part}_{suffix}"
                        )
                    print(
                        f"MAPPING: [{description}] SERIES-ID"
                        f" ({dicom_dir_number}) -> template"
                    )

                elif "_c500" in description:
                    task_event = "wbpilot"
                    if suffix == "sbref":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_dir-AP_run-{{item:02d}}_{suffix}"
                        )
                    if suffix == "bold":
                        template = create_key(
                            f"sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_dir-AP_run-{{item:02d}}_part-{part}_{suffix}"
                        )
                    print(
                        f"MAPPING: [{description}] SERIES-ID"
                        f" ({dicom_dir_number}) -> template"
                    )

                elif "_c09a_" in description:
                    task_event = "entrainAQ1"
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

                elif "_c09b_" in description:
                    task_event = "entrainBQ1"
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

                elif "_c09c_" in description:
                    task_event = "entrainCQ1"
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
                elif "_c09d_" in description:
                    task_event = "entrainDQ1"
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
                elif "_c09e_" in description:
                    task_event = "entrainEQ1"
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
                elif "_c09f_" in description:
                    task_event = "entrainFQ1"
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
                        f"WARNING: [{description} || suffix: {suffix}] SERIES-ID"
                        f" ({dicom_dir_number}) WAS NOT SAVED."
                    )
                    continue

                try:
                    info[template].append({"item": s.series_id})
                except:
                    info[template] = [{"item": s.series_id}]

        return info

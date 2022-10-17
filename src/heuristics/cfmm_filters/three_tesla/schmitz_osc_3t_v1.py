"""
3T fast-TR multiband bold sequence - provides mappings for task-event(s) of magnitude/phase/sbref images
"""

import collections

from src.heuristics.cfmm_filters.utils import create_key

part_mappings = {'M': 'mag','P': 'phase'}

class bold:

    def __init__(self, seqinfo):

        self.seqinfo = seqinfo

    def get_info(self):

        # Initialize empty info dict: key=create_key() and value=[] for all images
        info = {}
        phase_dirs = [] # for tracking main phase direction of scans
        # Map image key(s) to dicom series_id(s)
        for s in self.seqinfo:

            description = s.series_description.lower()
            if 'ep_bold_mb' in description:

                # Scrape info from Series_description of dicom.tsv
                mb_factor = description.split('_mb')[1].split('_')[0]
                phase_dir = description.split('_mb')[1][2:4].upper()
                if phase_dir == 'P2':
                    mb_factor = '4p2'
                    phase_dir = description.split('_p2')[1][1:3].upper()
                phase_dirs.append(phase_dir)
                dicom_dir_number = str(s.dcm_dir_name)
                part = part_mappings[s.image_type[2]]
                suffix = 'sbref' if 'sbref'.lower() in s.series_description.lower() else 'bold'

                whole_brain = True if 'wholebrain' in s.series_description.lower() else False

                reverse_phase = True if (collections.Counter(phase_dirs).most_common(1)[0][0] != phase_dir) and (s.dim4 == 1 or s.dim4 == 2) else False
                if whole_brain:
                    if suffix == 'sbref': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-wholebrain_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}')
                    if suffix == 'bold': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-wholebrain_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}')
                    print(f'MAPPING: [{description}] SERIES-ID ({dicom_dir_number}) -> template')
                elif reverse_phase:
                    if suffix == 'sbref': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-reversephase_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}')
                    if suffix == 'bold': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-reversephase_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}')
                    print(f'MAPPING: [{description}] SERIES-ID ({dicom_dir_number}) -> template')
                # Map task events
                elif '_c09_' in description:
                    task_event = 'entrain-tr'
                    if suffix == 'sbref': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}')
                    if suffix == 'bold': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}')
                    print(f'MAPPING: [{description}] SERIES-ID ({dicom_dir_number}) -> template')
                elif '_c12_' in description:
                    task_event = 'entrain-tl'
                    if suffix == 'sbref': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}')
                    if suffix == 'bold': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}')
                    print(f'MAPPING: [{description}] SERIES-ID ({dicom_dir_number}) -> template')
                elif '_c17_' in description:
                    task_event = 'control-tr'
                    if suffix == 'sbref': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}')
                    if suffix == 'bold': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}')
                    print(f'MAPPING: [{description}] SERIES-ID ({dicom_dir_number}) -> template')
                elif '_c20_' in description:
                    task_event = 'control-tl'
                    if suffix == 'sbref': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}')
                    if suffix == 'bold': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}')
                    print(f'MAPPING: [{description}] SERIES-ID ({dicom_dir_number}) -> template')
                elif '_c13_' in description:
                    task_event = 'localizer-tr'
                    if suffix == 'sbref': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}')
                    if suffix == 'bold': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}')
                    print(f'MAPPING: [{description}] SERIES-ID ({dicom_dir_number}) -> template')
                elif '_c16_' in description:
                    task_event = 'localizer-tl'
                    if suffix == 'sbref': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}')
                    if suffix == 'bold': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}')
                    print(f'MAPPING: [{description}] SERIES-ID ({dicom_dir_number}) -> template')
                elif '_c93_' in description:
                    task_event = 'prf-multibar'
                    if suffix == 'sbref': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}')
                    if suffix == 'bold': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}')
                    print(f'MAPPING: [{description}] SERIES-ID ({dicom_dir_number}) -> template')
                elif '_c91_' in description:
                    task_event = 'prf-expand'
                    if suffix == 'sbref': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}')
                    if suffix == 'bold': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}')
                    print(f'MAPPING: [{description}] SERIES-ID ({dicom_dir_number}) -> template')
                elif '_c89_' in description:
                    task_event = 'prf-ccw'
                    if suffix == 'sbref': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_{suffix}')
                    if suffix == 'bold': template = create_key(f'sub-{{subject}}/{{session}}/func/sub-{{subject}}_{{session}}_task-{task_event}_acq-mb{mb_factor}_dir-{phase_dir}_run-{{item:02d}}_part-{part}_{suffix}')
                    print(f'MAPPING: [{description}] SERIES-ID ({dicom_dir_number}) -> template')
                else:
                    print(f'WARNING: [{description}] SERIES-ID ({dicom_dir_number}) WAS NOT SAVED.')
                    continue

                try:
                    info[template].append({'item': s.series_id})
                except:
                    info[template] = [{'item': s.series_id}]

        return info

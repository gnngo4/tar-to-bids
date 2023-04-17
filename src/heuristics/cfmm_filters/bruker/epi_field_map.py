"""
9.4T Bruker GE epi sequence for whole brain field map generation using opposite phase-encoding images
"""

from src.heuristics.cfmm_filters.utils import create_key

class epi_field_map:

    def __init__(self, seqinfo):

        self.seqinfo = seqinfo
    
    def get_info(self):

        # Initialize empty info dict: key=create_key() and value=[] for all images
        info = {}
        # Map image key(s) to dicom series_id(s)
        for s in self.seqinfo:
            description = s.series_description.lower()
            if description == 'pciuserEPI_rsfMRI_Mice_40avg'.lower():
                template = create_key(f'sub-{{subject}}/{{session}}/fmap/sub-{{subject}}_{{session}}_dir-AP_desc-WholeBrainGE40Average_run-{{item:02d}}_epi')
            elif description == 'pciuserEPI_rsfMRI_Mice_RV_40avg'.lower():
                template = create_key(f'sub-{{subject}}/{{session}}/fmap/sub-{{subject}}_{{session}}_dir-PA_desc-WholeBrainGE40Average_run-{{item:02d}}_epi')
            else:
                continue
            
            try:
                info[template].append({'item': s.series_id})
            except:
                info[template] = [{'item': s.series_id}]
            
        return info
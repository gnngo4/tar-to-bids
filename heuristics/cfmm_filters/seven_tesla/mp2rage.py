"""
7T MP2RAGE sequence - provides mappings for UNI, T1map, INV1, and INV2 images
"""

from cfmm_filters.utils import create_key

class mp2rage:

    def __init__(self, seqinfo):

        self.seqinfo = seqinfo

    def get_info(self):

        # Initialize nifti file names
        uni = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-UNI_run-{item:02d}_MP2RAGE')
        t1map = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-MP2RAGE_run-{item:02d}_T1map')
        inv1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_inv-1_run-{item:02d}_MP2RAGE')
        inv2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_inv-2_run-{item:02d}_MP2RAGE')

        # Initialize info: key=create_key() and value=[] for all images
        info = {}
        images = [uni,t1map,inv1,inv2]
        for image in images:
            info[image] = []

        # Map image key(s) to dicom series_id(s)
        for s in self.seqinfo:

            if 'mp2rage' in s.series_description:

                if 'UNI_Images' in s.series_description.split('_'):
                    info[uni].append({'item': s.series_id})

                if 'T1_Images' in s.series_description:
                    info[t1map].append({'item': s.series_id})

                if 'INV1' in s.series_description:
                    info[inv1].append({'item': s.series_id})
                
                if 'INV2' in s.series_description:
                    info[inv2].append({'item': s.series_id})
        
        return info
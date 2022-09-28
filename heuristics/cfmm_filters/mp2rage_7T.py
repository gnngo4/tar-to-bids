"""
7T MP2RAGE sequence - provides mappings for UNI, T1map, INV1, and INV2 images
"""
class mp2rage_7T:
    def __init__(self, seqinfo):
        self.seqinfo = seqinfo
        self.uni = self._create_key('sub-{sub_id}/ses-{ses_id}/anat/sub-{sub_id}_ses-{ses_id}_acq-UNI_run-{item:02d}_MP2RAGE')
        self.t1map = self._create_key('sub-{sub_id}/ses-{ses_id}/anat/sub-{sub_id}_ses-{ses_id}_acq-MP2RAGE_run-{item:02d}_T1map')
        self.inv1 = self._create_key('sub-{sub_id}/ses-{ses_id}/anat/sub-{sub_id}_ses-{ses_id}_inv-1_run-{item:02d}_MP2RAGE')
        self.inv2 = self._create_key('sub-{sub_id}/ses-{ses_id}/anat/sub-{sub_id}_ses-{ses_id}_inv-2_run-{item:02d}_MP2RAGE')

    def get_info(self):

        # Initialize info: key=create_key() and value=[] for all images
        info = {}
        scans = [self.uni,self.t1map,self.inv1,self.inv2]
        for scan in scans:
            info[scan] = []

        # Map image key(s) to dicom series_id(s)
        for s in self.seqinfo:

            if 'mp2rage' in s.series_description.lower():

                if 'UNI' in s.series_description.split('_'):
                    info[self.uni].append({'item': s.series_id})

                if 'T1' in s.series_description.split('_'):
                    info[self.t1map].append({'item': s.series_id})

                if 'INV1' in s.series_description.split('_'):
                    info[self.inv1].append({'item': s.series_id})
                
                if 'INV2' in s.series_description.split('_'):
                    info[self.inv2].append({'item': s.series_id})
        
        return info

    def _create_key(template, outtype=('nii.gz',), annotation_classes=None):
        if template is None or not template:
            raise ValueError('Template must be a valid format string')
        return template, outtype, annotation_classes
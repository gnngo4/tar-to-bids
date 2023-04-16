import os, tarfile, shutil, tempfile

class cfmm_tar:

    def __init__(self, tar_file):

        self.tar_file = tar_file
        self.tar_dir = tempfile.mkdtemp()
        self.tar_tree = None

    def extract(self):

        file = tarfile.open(self.tar_file)
        file.extractall(self.tar_dir)
        file.close()

    def reformat_dicom_tree(self, dir_name):

        self._get_dicom_tree()

        src = '/'.join(self.tar_tree.split('/')[:-1])
        dst = src.replace(self.session_info, dir_name)
        os.rename(src,dst)
        print(f'RELABEL: {dst}')
        assert os.path.isdir(dst), f"{dst} does not exist."
        self._update_dicom_tree(dir_name)

    def cleanup(self):
        
        print(f"REMOVE: {self.tar_dir}")
        shutil.rmtree(self.tar_dir)

    def get_physio_pairs(self):
        """
        Naive method to pair physio dcm with corresponding MRI data
        Sequentially matches '_PhysioLog' to MRI data

        Returns a dictionary mapping Physio_log series number to its
        associated MRI series number
        """

        from pydicom import dcmread

        assert self.tar_tree is not None, f"Initialize self.tar_tree with the reformat_dicom_tree() method."
        series_ids = os.listdir(self.tar_tree)
        series_ids.sort() # reorder in ascending order

        # Loop through all SERIES to find SERIES names with a PhysioLog
        track_scans = []
        for series_id in series_ids:
            fp_base = f"{self.tar_tree}/{series_id}"
            single_dcm = f"{fp_base}/{os.listdir(fp_base)[0]}"
            series_description = dcmread(single_dcm).SeriesDescription
            '''
            Associated MRI series_description names can be retrieved 
            from the Physio series description by removing the suffix:
            '_PhysioLog'
            '''
            if '_PhysioLog' in series_description: track_scans.append(series_description.replace('_PhysioLog',''))

        
        physio_idx, physio_pairs = 0, {}
        physio_pair = {'PHYSIO': None,'MRI': None}
        for series_id in series_ids:
            
            fp_base = f"{self.tar_tree}/{series_id}"
            single_dcm = f"{fp_base}/{os.listdir(fp_base)[0]}"
            metadata = dcmread(single_dcm)
            series_description = metadata.SeriesDescription
            series_number = metadata.SeriesNumber

            if '_PhysioLog' in series_description: physio_pair['PHYSIO'] = str(series_number).zfill(4)
            if track_scans[physio_idx] == series_description: physio_pair['MRI'] = str(series_number).zfill(4)

            if physio_pair['PHYSIO'] is not None and physio_pair['MRI'] is not None:
                physio_pairs[physio_pair['PHYSIO']] = physio_pair['MRI'] # Add physio match
                physio_pair = {'PHYSIO': None,'MRI': None} # Reinitialize `physio_pair` after a match is established
                physio_idx += 1 # Increment `physio_idx`
                # End loop after all `physio_pairs` have been matched
                if physio_idx == len(track_scans): break

        return physio_pairs

    def pair_physio_to_mri(self,physio_pairs,subject_id,session_id,bids_dir):
        '''
        Loop through `physio_pairs` and copy physio dicoms to a physio_dir (`physio_dir`)
        '''
        
        physio_dir = f"{bids_dir}/sub-{subject_id}/ses-{session_id}/physio"
        if not os.path.isdir(physio_dir): os.mkdir(physio_dir)

        for physio_id, mri_id in physio_pairs.items():

            dcm_physio_dir = f"{self.tar_tree}/{physio_id}"
            assert len(os.listdir(dcm_physio_dir)) == 1, "Physio dicom folder should contain only 1 file."
            physio_dcm = f"{dcm_physio_dir}/{os.listdir(dcm_physio_dir)[0]}"
            copy_physio_cmd = f"cp {physio_dcm} {physio_dir}/sub-{subject_id}_ses-{session_id}_task-{mri_id}_physio-{physio_id}_PHYSIOLOG.dcm"
            os.system(copy_physio_cmd)

    def _get_dicom_tree(self):

        splits = self.tar_file.split('/')[-1].split('_')
        self.session_info = '_'.join(splits[3:-1])
        self.tar_tree = '/'.join(
            [
                self.tar_dir,
                splits[0],
                splits[1],
                splits[2],
                self.session_info,
                splits[-1].replace('.tar',''),
            ]
        )
        print(f'UNTAR: {self.tar_tree}')
        assert os.path.isdir(self.tar_tree), f"{self.tar_tree} does not exist."

    def _update_dicom_tree(self, dir_name):

        self.tar_tree = self.tar_tree.replace(self.session_info,dir_name)
        print(f'UPDATE: {self.tar_tree}')
        assert os.path.isdir(self.tar_tree), f"{self.tar_tree} does not exist."
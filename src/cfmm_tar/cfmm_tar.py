import os, tarfile, shutil, tempfile

class cfmm_tar:

    def __init__(self, tar_file):

        self.tar_file = tar_file
        self.tar_dir = tempfile.mkdtemp()

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

import os
import zipfile
import shutil
import tempfile
import pathlib


class cfmm_zip:
    def __init__(self, zip_file):
        self.zip_file = zip_file
        self.zip_dir = tempfile.mkdtemp()
        self.zip_tree = None

    def extract(self):
        file = zipfile.ZipFile(self.zip_file)
        file.extractall(self.zip_dir)
        file.close()

    def reformat_dicom_tree(self, dir_name):
        path = pathlib.Path(self.zip_dir)
        common_path = str(
            pathlib.Path(
                os.path.commonprefix(
                    [i for i in path.glob("**/*.dcm")]
                )
            ).parent
        )
        dst = common_path.replace(common_path.split("/")[5], dir_name)
        os.rename(common_path, dst)
        print(f"RELABEL: {dst}")
        assert os.path.isdir(dst), f"{dst} does not exist."

    def cleanup(self):
        print(f"REMOVE: {self.zip_dir}")
        shutil.rmtree(self.zip_dir)

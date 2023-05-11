import os
import shutil
import zipfile
import shutil
import tempfile
import pathlib
import pydicom


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
                os.path.commonprefix([i for i in path.glob("**/*.dcm")])
            ).parent
        )
        dst = common_path.replace(common_path.split("/")[5], dir_name)
        shutil.move(common_path, dst)
        print(f"RELABEL: {dst}")
        assert os.path.isdir(dst), f"{dst} does not exist."
        # Manual retag StackID info for single slice acquisitions
        _ = [
            self._rewrite_stackid(dcm_path)
            for dcm_path in self._get_files_with_suffix(dst, ".dcm")
        ]

    def cleanup(self):
        print(f"REMOVE: {self.zip_dir}")
        shutil.rmtree(self.zip_dir)

    def _get_files_with_suffix(self, directory, suffix):
        file_list = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(suffix):
                    file_list.append(os.path.join(root, file))

        return file_list

    def _rewrite_stackid(self, dcm_path):
        file_basename = os.path.basename(dcm_path)
        file_dir = os.path.dirname(dcm_path)

        ds = pydicom.dcmread(dcm_path)
        seq = ds.PerFrameFunctionalGroupsSequence

        if not hasattr(
            ds.PerFrameFunctionalGroupsSequence[0].FrameContentSequence[0], "StackID"
        ):
            for frame in seq:
                frame.FrameContentSequence[0].StackID = "1"
                frame.FrameContentSequence[0].InstackPositionNumber = 1
                dim_index_value = frame.FrameContentSequence[0].DimensionIndexValues
                frame.FrameContentSequence[0].DimensionIndexValues = [
                    dim_index_value,
                    1,
                    1,
                ]
            ds.save_as(os.path.join(file_dir, file_basename))

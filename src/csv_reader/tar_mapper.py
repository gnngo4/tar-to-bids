import os
import pandas as pd

class task_mapper:

    def __init__(self,heuristic,rel_task_csv):
        
        self.TASK_COLUMNS = ['series_id','task_event']
        self.MAPPING_DIR = '/mappings'
        if '/' in rel_task_csv:
            rel_task_csv = rel_task_csv.split('/')[-1]
        self.task_csv = f"{self.MAPPING_DIR}/{heuristic}/series_task_mappings/{rel_task_csv}"
        assert os.path.exists(self.task_csv), f"{self.task_csv} does not exist."

    def get_series_to_task_mappings(self):

        df = pd.read_csv(self.task_csv)
        assert [i for i in df.columns[:2]] == self.TASK_COLUMNS, f"csv columns should include: {self.TASK_COLUMNS}"
        series_id = [str(i).zfill(4) for i in df['series_id'].to_list()]
        task_event = df['task_event'].to_list()
        
        return dict(zip(series_id,task_event))

class tar_mapper:

    def __init__(self):
        

        self.MAPPING_DIR = '/mappings'
        self.TAR_COLUMNS = ['tar', 'study_id', 'subject_id', 'session_id', 'task_csv', 'notes']
        self.MANDATORY_TAR_COLUMNS = self.TAR_COLUMNS[:-1]
        tar_mappings_csv = self._check_mappings_directory_structure()

        self.tar_csv = tar_mappings_csv

    def check_csv(self,tar_file):

        """
        Load `tar_csv`

        This csv is manually created/updated and includes mapping between
            - tar file names (naming convention is consistent with participant scan IDs as found on the DICOM servers)
            - study_id (as specified by the user)
            - subject_id 
            - session_id
            - task_csv file that contains mapping of MRI series-id(s) to the task fMRI event
        """

        # Check all columns exist
        df = pd.read_csv(self.tar_csv)
        assert [i for i in df.columns] == self.TAR_COLUMNS, f"csv columns should only include: {self.TAR_COLUMNS}"
        # Check if all relevant columns are filled out 
        log_dict = self._check_tar_file(df,tar_file)
        # print information
        for col, info in log_dict.items():
            print(f"{col}: {info}")

    def _check_mappings_directory_structure(self):
        
        assert os.path.isdir(self.MAPPING_DIR), f"{self.MAPPING_DIR} directory does not exist."
        tar_mappings_csv = os.path.join(self.MAPPING_DIR,'tar_mappings.csv')
        assert os.path.exists(tar_mappings_csv), f"{tar_mappings_csv} does not exist."
        
        return tar_mappings_csv
        
    def _check_tar_file(self, df, tar_file):

        tar_row = df[df.tar==tar_file]
        check_null = tar_row.isnull()

        # Check if `tar_file` exists in the csv
        assert tar_row.shape[0] == 1, f"{tar_file} does not exist in the csv, or there are more than 1."
        # Check to make sure the MANDATORY_TAR_COLUMNS are filled out
        log_dict = {}
        for _col in self.MANDATORY_TAR_COLUMNS:
            assert not check_null[_col].values[0], f"{tar_file}: {_col} is empty."
            log_dict[_col] = tar_row[_col].values[0]
        # Check if task_csv mapping exists
        task_csv = f"{self.MAPPING_DIR}/{log_dict['study_id']}/series_task_mappings/{log_dict['task_csv']}"
        assert os.path.exists(task_csv), f"{task_csv} does not exist."

        return log_dict
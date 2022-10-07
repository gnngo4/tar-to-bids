import argparse, os

from src.csv_reader.tar_mapper import tar_mapper
from src.heuristics.utils import HEURISTIC_DIR

class CheckTarMappings(argparse.Action):

    def __call__(self,parser,namespace,values,option_string):
        # https://stackoverflow.com/questions/53434478/python-argparse-ignore-other-options-when-a-specific-option-is-used
        '''
        Retrieve tar mappings if `args.check_tar_mappings` is used.
        '''
        if '/' in values: values = values[-1]
        tar_mapper().check_csv(values)
        parser.exit() # Exit the program with no more arg parsing and checking

class CheckAvailableHeuristics(argparse.Action):

    def __call__(self,parser,namespace,values,option_string):
        print("Available heuristics:")
        for _dir in os.listdir(HEURISTIC_DIR):
            if '.py' == _dir[-3:] and _dir != 'utils.py':
                print(f"    - {_dir}")
        parser.exit()
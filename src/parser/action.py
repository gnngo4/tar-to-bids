import argparse

from src.csv_reader.tar_mapper import tar_mapper

class CheckTarMappings(argparse.Action):

    def __call__(self,parser,namespace,values,option_string):
        # https://stackoverflow.com/questions/53434478/python-argparse-ignore-other-options-when-a-specific-option-is-used
        '''
        Retrieve tar mappings if `args.check_tar_mappings` is used.
        '''
        if '/' in values: values = values[-1]
        tar_mapper().check_csv(values)
        parser.exit() # Exit the program with no more arg parsing and checking
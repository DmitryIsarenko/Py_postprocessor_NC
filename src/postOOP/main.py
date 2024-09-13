from src.postOOP.classes.file_operator import FileOperator
from src.postOOP.classes.parsers.pprint_parser import PprintParser
from src.postOOP.classes.ust_creator import UstanovFileCreator
from src.postOOP.classes.program_creator import ProgramFileCreator
from src.postOOP.classes.ncl_filler import NclFiller
from src.postOOP.classes.ncl_file_analyzer import NclFileAnalyzer

def main():
    filepaths = FileOperator.get_all_ncl_files_in_dir()
    if filepaths:
        for filepath in filepaths:
            try:
                temp_file = FileOperator.create_temp_formatted_ncl_file(filepath=filepath)
                if temp_file is None:
                    continue
                cl_lines = FileOperator.get_cl_lines_in_range(filepath=temp_file)

                # print(len(cl_lines))

                pprint_vars = PprintParser().parse_pprint(lines=cl_lines)
                UstanovFileCreator().create_files_for_ustanov(pprint_vars=pprint_vars)
                ProgramFileCreator().create_files_for_operations_in_ustanov(pprint_vars=pprint_vars)
                NclFiller().loop_through_all_subprograms_parsing_range_cl_lines(cl_lines=cl_lines,
                                                                              pprint_vars=pprint_vars)
                FileOperator.remove_file(filepath=temp_file)
            except FileNotFoundError:
                print(f"FileNotFoundError {filepath}")

    print(NclFileAnalyzer.count_cl_lines_in_cl_list(cl_list=cl_lines))
    print(NclFileAnalyzer.count_nc_sequences_in_cl_list(cl_list=cl_lines))

if __name__ == "__main__":
    main()

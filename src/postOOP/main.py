from src.postOOP.classes.ncl_file_operator import NclFileOperator
from src.postOOP.classes.parsers.pprint_parser import PprintParser
from src.postOOP.classes.ust_creator import UstanovFileCreator
from src.postOOP.classes.program_creator import ProgramFileCreator
from src.postOOP.classes.ncl_filler import NclFiller
from src.postOOP.classes.file_operator import FileOperator



def main():
    filenames = NclFileOperator().get_all_ncl_files_in_dir()
    for filename in filenames:
        try:
            cl_lines = NclFileOperator().read_ncl_file_format_and_create_temp_file(filepath=filename)
            pprint_vars = PprintParser().parse_pprint(lines=cl_lines)
            UstanovFileCreator().create_files_for_ustanov(pprint_vars=pprint_vars)
            ProgramFileCreator().create_files_for_operations_in_ustanov(pprint_vars=pprint_vars)
            NclFiller().loop_through_all_subprograms_parsing_range_cl_lines(cl_lines=cl_lines, pprint_vars=pprint_vars)
            FileOperator().remove_temp_file()
        except FileNotFoundError:
            print(f"FileNotFoundError {filename}")


if __name__ == "__main__":
    main()

from src.postOOP.classes.parsers.ncl_parser import NclParser
from src.postOOP.classes.file_operator import FileOperator


class NclFiller():
    def loop_through_all_subprograms_parsing_range_cl_lines(self, cl_lines, pprint_vars: dict) -> None:
        for sub_prog_dict in pprint_vars["operations"]:
            result_list = NclParser().parse_range_cl_records(cl_lines=cl_lines,
                                                             pprint_vars=pprint_vars,
                                                             program_num_iter=sub_prog_dict["program_num_iter"])
            FileOperator().append_parsed_lines_to_file(filepath=sub_prog_dict["program_O_name_with_extension"],
                                                       list_with_lines=result_list)

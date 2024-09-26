from src.postOOP.config import (
    DELETE_TEMP_FILE,
)

from src.postOOP.classes.parsers.pprint_parser import PprintParser
from src.postOOP.classes.nc_sequence_classes.nc_program import NcProgram
from src.postOOP.classes.nc_sequence_classes.nc_sequence import NcSequence
from src.postOOP.classes.others.file_operator import FileOperator
from src.postOOP.classes.others.formatter import Formatter


# from src.postOOP.classes.ncl_parser import NclParser


class NcOperation(NcProgram):
    postprocessor_name = "basic post class"
    detail_name = None
    date_of_creation = None

    operation_name = None
    operation_number = None
    nc_filename = None
    nc_filename_with_extension = None

    cl_lines_count = None
    nc_sequences_count = None
    list_of_nc_sequences_names = None
    list_of_nc_sequences_objects = None
    sum_machining_time = None

    def __init__(self, filepath: str):
        self.filepath = filepath
        pass

    def start_postprocessing(self):
        temp_filepath = FileOperator.create_temp_formatted_ncl_file(filepath=self.filepath)
        self.cl_list = FileOperator.get_all_cl_lines(filepath=temp_filepath)

        if self.cl_list:
            self.set_cl_lines_count()
            self.set_detail_name()
            self.set_date_of_creation()
            self.set_operation_name()
            self.set_operation_num_from_name()
            self.set_nc_filename()

            self.set_nc_sequences_count()
            self.set_nc_sequences_names_in_list()
            self.set_nc_sequences_objects_in_list()
            self.set_sum_machining_time()

            # self.show()
            self.nc_list = self.generate_nc_list()
            # print(self.nc_list)
            FileOperator.create_file(filepath=self.nc_filename_with_extension)
            FileOperator.append_lines_to_file(filepath=self.nc_filename_with_extension, list_with_lines=self.nc_list)
        else:
            print(f"Empty self.cl_list for {self.filepath}")

        if DELETE_TEMP_FILE == 1:
            FileOperator.remove_file(filepath=temp_filepath)
        else:
            pass

    def set_nc_sequences_count(self):
        self.nc_sequences_count: int = PprintParser.count_nc_sequences_in_cl_list(cl_list=self.cl_list)

    def set_nc_sequences_names_in_list(self):
        self.list_of_nc_sequences_names: list[str] = PprintParser.get_list_of_nc_sequence_names(
            cl_list=self.cl_list)

    def set_nc_sequences_objects_in_list(self):
        lst_of_objects = []
        nc_counter = 0
        for nc_sequence_name in self.list_of_nc_sequences_names:
            nc_counter += 1
            lst_of_objects.append(
                NcSequence(detail_name=self.detail_name, nc_sequence_name=nc_sequence_name, cl_list=self.cl_list,
                           nc_sequence_number=nc_counter, nc_sequences_count=self.nc_sequences_count,
                           nc_operation_number=self.operation_number, date_of_creation=self.date_of_creation))
        self.list_of_nc_sequences_objects: list[NcSequence] = lst_of_objects

    def set_sum_machining_time(self):
        sum_time = 0
        for nc_obj in self.list_of_nc_sequences_objects:
            sum_time += nc_obj.machining_time
        self.sum_machining_time = round(sum_time, ndigits=2)

    def set_cl_lines_count(self):
        self.cl_lines_count = PprintParser.count_cl_lines_in_cl_list(cl_list=self.cl_list)

    def set_detail_name(self):
        self.detail_name = PprintParser.get_detail_name_in_cl_list(cl_list=self.cl_list)

    def set_date_of_creation(self):
        self.date_of_creation = PprintParser.get_date_time_in_cl_list(cl_list=self.cl_list)

    def set_operation_num_from_name(self):
        num = ""
        for char in self.operation_name:
            if char.isdigit():
                num += char
        self.operation_number = int(num)

    def set_operation_name(self):
        self.operation_name: str = PprintParser.get_operation_name_in_cl_list(cl_list=self.cl_list)

    def set_nc_filename(self):
        if self.operation_number < 10:
            num_in_str = str(self.operation_number) + "00"
        else:
            print(f"Too many nc operations")
            raise ValueError

        self.nc_filename = self.main_letter + self.main_digit + num_in_str
        self.nc_filename_with_extension = self.nc_filename + self.file_extension

    def generate_nc_list(self) -> list:
        nc_lines = list()
        nc_lines.extend(self.generate_nc_head_lines())
        nc_lines.extend(self.generate_nc_body_lines())
        nc_lines.extend(self.generate_nc_tail_lines())
        nc_lines = Formatter.append_line_endings_in_cl_list_or_str(cl_list_or_str=nc_lines)
        nc_lines = Formatter.append_line_wraps_in_cl_list_or_str(cl_list_or_str=nc_lines)
        # pprint(nc_lines)
        return nc_lines

    def generate_nc_head_lines(self) -> list:
        nc_lines = [
            f"(PART: {self.detail_name})",
            f"(PROGRAMMER: {self.programmer_name})",
            f"(DATE: {self.date_of_creation})",
            f"(UST:  {self.operation_name})",
            f"(PROG NUMS: {self.nc_sequences_count})",
            f"",
        ]
        return nc_lines

    def generate_nc_body_lines(self) -> list:
        nc_lines = []
        for obj in self.list_of_nc_sequences_objects:
            if obj.is_m00_before_needed is True:
                nc_lines.append("M00")
            nc_lines.extend([
                f"M98P{obj.nc_file_number}"
                f"(OPER {obj.nc_sequence_number}/{obj.nc_sequences_count}: {obj.nc_sequence_name})",
                f"(POT: {obj.tool_pot}, TOOL: {obj.tool_name})",
            ])
            if obj.is_m00_after_needed is True:
                nc_lines.append("M00")
            nc_lines.append(f"")
        return nc_lines

    def generate_nc_tail_lines(self) -> list:
        nc_lines = [
            "G53",
            "G00 Z0.0",
            "G00 X0.0 Y0.0",
            f"(MACHINING TIME: {self.sum_machining_time})",
            "M30",
        ]
        return nc_lines

from pprint import pprint
from src.postOOP.config import (PROGRAM_MAIN_DIGIT,
                                PROGRAM_MAIN_LETTER,
                                G_CODE_FILE_EXTENSION,
                                POST_NAME,
                                PROGRAMMER_NAME,
                                NC_START_KEYWORD,
                                NC_END_KEYWORD,
                                DELETE_TEMP_FILE,
                                SAFETY_LINE_DEFAULT,
                                NC_SEQUENCE_TAIL_LINES,
                                )

from src.postOOP.classes.pprint_parser import PprintParser
from src.postOOP.classes.ncl_parser import NclParser

from src.postOOP.classes.file_operator import FileOperator
from src.postOOP.classes.formatter import Formatter


class NcProgram:
    main_digit = PROGRAM_MAIN_DIGIT
    main_letter = PROGRAM_MAIN_LETTER
    file_extension = G_CODE_FILE_EXTENSION
    postprocessor_name = POST_NAME
    line_with_programmer_name = PROGRAMMER_NAME

    cl_list: list[str] = []
    nc_list: list[str] = []

    def show(self):
        print(f"\n\n"
              f"Dictionary of {self.__class__} object")
        pprint(self.__dict__)
        print(f"\n\n")


class NcOperation(NcProgram):
    def __init__(self, filepath: str):

        temp_filepath = FileOperator.create_temp_formatted_ncl_file(filepath=filepath)
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

            self.show()
        else:
            print(f"Empty self.cl_list for {filepath}")

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
        self.sum_machining_time = sum_time

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
        self.nc_filename = self.main_letter + self.main_digit + num_in_str + self.file_extension


class NcSequence(NcProgram):
    nc_start_keyword = NC_START_KEYWORD
    nc_end_keyword = NC_END_KEYWORD

    def __init__(self, detail_name: str, nc_sequence_name: str, cl_list: list, nc_operation_number: int,
                 nc_sequence_number: int, nc_sequences_count: int, date_of_creation: str):
        self.detail_name = detail_name
        self.nc_sequence_name = nc_sequence_name
        self.cl_list = cl_list
        self.nc_operation_number = nc_operation_number
        self.nc_sequence_number = nc_sequence_number
        self.nc_sequences_count = nc_sequences_count
        self.date_of_creation = date_of_creation
        self.set_nc_filename()

        self.set_cl_start_index()
        self.set_cl_end_index()

        self.set_work_offset()
        self.set_tool_name()
        self.set_tool_pot()
        self.set_spindle_master_data()
        self.set_cut_feed_master()
        self.set_machining_time()

        self.show()
        self.generate_nc_lines()
        FileOperator.create_file(filepath=self.nc_filename)


    def set_cl_start_index(self):
        self.cl_start_index = PprintParser.get_index_of_occurence_in_cl_list_in_range(cl_list=self.cl_list,
                                                                                      search_for=self.nc_sequence_name,
                                                                                      start_index=0,
                                                                                      end_index=len(self.cl_list))

    def set_cl_end_index(self):
        self.cl_end_index = PprintParser.get_index_of_occurence_in_cl_list_in_range(cl_list=self.cl_list,
                                                                                    search_for=self.nc_end_keyword,
                                                                                    start_index=self.cl_start_index,
                                                                                    end_index=len(self.cl_list))

    def set_work_offset(self):
        self.work_offset = PprintParser.get_work_offset(cl_list=self.cl_list)

    def set_machining_time(self):
        self.machining_time = PprintParser.get_machining_time_in_cl_list(
            cl_list=self.cl_list[self.cl_start_index:self.cl_end_index])

    def set_tool_name(self):
        self.tool_name = PprintParser.get_tool_name_in_cl_list_range(cl_list=self.cl_list,
                                                                     start_index=self.cl_start_index,
                                                                     end_index=self.cl_end_index)

    def set_tool_pot(self):
        self.tool_pot = PprintParser.get_tool_pot_in_cl_list_range(cl_list=self.cl_list,
                                                                   start_index=self.cl_start_index,
                                                                   end_index=self.cl_end_index)

    def set_spindle_master_data(self):
        spindle_data = PprintParser.get_spindle_data_in_cl_list_range(cl_list=self.cl_list,
                                                                      start_index=self.cl_start_index,
                                                                      end_index=self.cl_end_index)
        if spindle_data:
            self.spindle_speed_master = spindle_data[0]
            self.spindle_units_master = spindle_data[1]
            self.spindle_direction_master = spindle_data[2]

    def set_cut_feed_master(self):
        self.cut_feed_master = PprintParser.get_cut_feed_in_cl_list_range(cl_list=self.cl_list,
                                                                          start_index=self.cl_start_index,
                                                                          end_index=self.cl_end_index)

    def set_nc_filename(self):
        if self.nc_sequence_number < 10:
            num_in_str = "0" + str(self.nc_sequence_number)
        elif self.nc_sequence_number < 99:
            num_in_str = str(self.nc_sequence_number)
        else:
            print(f"Too many nc sequences")
            raise ValueError
        self.nc_filename = (self.main_letter +
                            self.main_digit +
                            str(self.nc_operation_number) +
                            num_in_str +
                            self.file_extension)

    def generate_nc_lines(self) -> list:
        nc_lines = list()
        nc_lines.extend(self.generate_nc_head_lines())
        nc_lines.extend(self.generate_nc_body_lines())
        nc_lines.extend(self.generate_nc_tail_lines())
        nc_lines = Formatter.append_line_endings_in_cl_list_or_str(cl_list_or_str=nc_lines)
        nc_lines = Formatter.append_line_wraps_in_cl_list_or_str(cl_list_or_str=nc_lines)
        pprint(nc_lines)
        return nc_lines

    def generate_nc_head_lines(self) -> list:
        nc_lines = [f"(TOOL: {self.tool_name})",
                    f"(POT:  {self.tool_pot})",
                    f"(PART: {self.detail_name})",
                    f"(PROG: {self.nc_sequence_name})",
                    f"(PROG NUM: {self.nc_sequence_number} / {self.nc_sequences_count})",
                    f"(DATE: {self.date_of_creation})",
                    f"",
                    f"G{self.work_offset}",
                    f"{SAFETY_LINE_DEFAULT}"
                    ]
        return nc_lines

    def generate_nc_body_lines(self) -> list:
        nc_lines = NclParser.parse_cl_list(nc_seq_obj=self)
        return nc_lines

    def generate_nc_tail_lines(self) -> list:
        nc_lines = NC_SEQUENCE_TAIL_LINES
        return nc_lines

    def add_nc_lines_to_object_nc_list(self, nc_lines_or_str: list[str] | str):
        if type(nc_lines_or_str) == list:
            self.nc_list.extend(nc_lines_or_str)
        elif type(nc_lines_or_str) == str:
            self.nc_list.append(nc_lines_or_str)
        else:
            raise TypeError

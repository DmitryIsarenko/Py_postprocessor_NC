import logging

from src.postOOP import config

from src.postOOP.classes.mill.nc_sequence_classes.basic.nc_sequence_mill_3axis import NcSequenceMill3Axis
from src.postOOP.classes.mill.parsers.pprint_parsers.basic.pprint_parser_basic import PprintParserBasic
from src.postOOP.classes.mill.parsers.ncl_parsers.ncl_parser_basic import NclParserBasic
from src.postOOP.classes.others.file_operator_basic import FileOperatorBasic
from src.postOOP.classes.others.formatter import Formatter

logger = logging.getLogger(__name__)


class NcOperationMill3Axis:
    nc_sequence_class: NcSequenceMill3Axis = NcSequenceMill3Axis
    pprint_parser_class: PprintParserBasic = PprintParserBasic
    ncl_parser_class: NclParserBasic = NclParserBasic
    file_operator_class: FileOperatorBasic = FileOperatorBasic

    postprocessor_name = "NcOperationMill3Axis"

    main_digit = config.PROGRAM_MAIN_DIGIT
    main_letter = config.PROGRAM_MAIN_LETTER
    file_extension = config.G_CODE_FILE_EXTENSION
    programmer_name = config.PROGRAMMER_NAME

    cl_list: list[str] = []
    nc_list: list[str] = []

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

    oper_nc_head_lines = []
    oper_nc_body_lines = []
    oper_nc_tail_lines = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        config.POST_NAME = self.postprocessor_name
        logger.info(f"Post name from config: <<<{config.POST_NAME}>>>")
        # logger.debug(f"nc_operation class name : <<<{self.__class__.__name__}>>>")
        # logger.debug(f"nc_sequence class name : <<<{self.nc_sequence_class.nc_sequence_class_name}>>>")
        # logger.debug(f"Pprint_parser class name: <<<{self.pprint_parser_class.pprint_parser_class_name}>>>")
        # logger.debug(f"Ncl_parser class name : <<<{self.ncl_parser_class.ncl_parser_class_name}>>>")

    def start_postprocessing(self):
        temp_filepath = self.file_operator_class.create_temp_formatted_ncl_file()
        self.cl_list = self.file_operator_class.get_all_cl_lines(filepath=temp_filepath)

        if self.cl_list:
            self.set_cl_lines_count()
            self.set_detail_name()
            self.set_date_of_creation()
            self.set_operation_name()
            self.set_operation_num_from_name()
            self.set_nc_filename()

            self.set_nc_sequences_names_in_list()
            self.set_nc_sequences_objects_in_list()
            self.set_sum_machining_time()

            self.set_nc_sequences_count()
            for seq in self.list_of_nc_sequences_objects:
                seq.generate_nc_seq_head_body_tail_lists()

            for seq in self.list_of_nc_sequences_objects:
                seq.combine_nc_seq_head_body_tail_lines_in_one_list()

            for seq in self.list_of_nc_sequences_objects:
                seq.create_seq_file()

            for seq in self.list_of_nc_sequences_objects:
                seq.fill_seq_file()

            self.generate_nc_oper_head_body_tail_lists()
            self.nc_list = self.combine_nc_oper_head_body_tail_lines_in_one_list()

            self.create_oper_file()
            self.fill_oper_file()

        else:
            logger.warning(f"Empty self.cl_list for {config.abs_path_to_selected_file}")

        if config.DELETE_TEMP_FILE:
            self.file_operator_class.remove_file(filepath=temp_filepath)
        else:
            pass

    def create_oper_file(self):
        self.file_operator_class.create_file(
            filepath=f"{config.abs_path_to_selected_file}/../{self.nc_filename_with_extension}")

    def fill_oper_file(self):
        self.file_operator_class.append_lines_to_file(
            filepath=f"{config.abs_path_to_selected_file}/../{self.nc_filename_with_extension}",
            list_with_lines=self.nc_list)



    def generate_nc_oper_head_body_tail_lists(self):
        self.oper_nc_head_lines = self.generate_nc_oper_head_lines()
        self.oper_nc_body_lines = self.generate_nc_oper_body_lines()
        self.oper_nc_tail_lines = self.generate_nc_oper_tail_lines()


    def set_nc_sequences_count(self):
        counter = 0
        for seq in self.list_of_nc_sequences_objects:
            if seq.is_file_needed:
                counter += 1
        self.nc_sequences_count: int = counter
        for seq in self.list_of_nc_sequences_objects:
            seq.nc_sequences_count = counter
        logger.debug(f"self.nc_sequences_count = {self.nc_sequences_count}")

        # self.nc_sequences_count: int = self.pprint_parser_class.count_nc_sequences_in_cl_list(cl_list=self.cl_list)

    def set_nc_sequences_names_in_list(self):
        self.list_of_nc_sequences_names: list[str] = self.pprint_parser_class.get_list_of_nc_sequence_names(
            cl_list=self.cl_list)
        logger.debug(f"list_of_nc_sequences_names {self.list_of_nc_sequences_names}")

    def set_nc_sequences_objects_in_list(self):
        lst_of_objects = []
        nc_counter = 0
        nc_massive_copy_counter = 0

        for nc_sequence_name in self.list_of_nc_sequences_names:
            nc_counter += 1

            if nc_sequence_name in config.sequence_massive_names:
                nc_sequence_parent_name_of_massive = lst_of_objects[-1].nc_sequence_parent_name_of_massive
                nc_massive_copy_counter += 1

            else:
                nc_sequence_parent_name_of_massive = nc_sequence_name
                nc_massive_copy_counter = 0
            lst_of_objects.append(
                self.nc_sequence_class(ncl_parser_class=self.ncl_parser_class,
                                       pprint_parser_class=self.pprint_parser_class,
                                       file_operator_class=self.file_operator_class,
                                       detail_name=self.detail_name,
                                       nc_sequence_name=nc_sequence_name,
                                       nc_sequence_parent_name_of_massive=nc_sequence_parent_name_of_massive,
                                       nc_massive_copy_counter=nc_massive_copy_counter,
                                       cl_list=self.cl_list,
                                       nc_sequence_number=nc_counter,
                                       nc_sequences_count=self.nc_sequences_count,
                                       nc_operation_number=self.operation_number,
                                       date_of_creation=self.date_of_creation))
        self.list_of_nc_sequences_objects: list = lst_of_objects
        logger.debug(
            f"self.list_of_nc_sequences_objects {[item.nc_sequence_number for item in self.list_of_nc_sequences_objects]}")

    def set_sum_machining_time(self):
        sum_time = 0
        for nc_obj in self.list_of_nc_sequences_objects:
            sum_time += nc_obj.machining_time
        self.sum_machining_time = round(sum_time, ndigits=2)

    def set_cl_lines_count(self):
        self.cl_lines_count = self.pprint_parser_class.count_cl_lines_in_cl_list(cl_list=self.cl_list)

    def set_detail_name(self):
        self.detail_name = self.pprint_parser_class.get_detail_name_in_cl_list(cl_list=self.cl_list)

    def set_date_of_creation(self):
        self.date_of_creation = self.pprint_parser_class.get_date_time_in_cl_list(cl_list=self.cl_list)

    def set_operation_num_from_name(self):
        num = ""
        for char in self.operation_name[0:8:1]:
            if char.isdigit():
                num += char
        self.operation_number = int(num)

    def set_operation_name(self):
        self.operation_name: str = self.pprint_parser_class.get_operation_name_in_cl_list(cl_list=self.cl_list)

    def set_nc_filename(self):
        if self.operation_number < 10:
            num_in_str = str(self.operation_number) + "00"
        else:
            logger.critical(f"Too many nc operations")
            raise ValueError

        self.nc_filename = config.PROGRAM_MAIN_LETTER + config.PROGRAM_MAIN_DIGIT + num_in_str
        self.nc_filename_with_extension = self.nc_filename + config.G_CODE_FILE_EXTENSION

    def combine_nc_oper_head_body_tail_lines_in_one_list(self) -> list:
        nc_lines = list()
        nc_lines.extend(self.oper_nc_head_lines)
        nc_lines.extend(self.oper_nc_body_lines)
        nc_lines.extend(self.oper_nc_tail_lines)
        nc_lines = Formatter.append_line_endings_in_cl_list_or_str(cl_list_or_str=nc_lines)
        nc_lines = Formatter.append_line_wraps_in_cl_list_or_str(cl_list_or_str=nc_lines)
        # pprint(nc_lines)
        return nc_lines

    def generate_nc_oper_head_lines(self) -> list:
        nc_lines = [
            f"(POST: {config.POST_NAME})",
            f"(PART: {self.detail_name})",
            f"(PROGRAMMER: {config.PROGRAMMER_NAME})",
            f"(DATE: {self.date_of_creation})",
            f"(UST:  {self.operation_name})",
            f"(PROG NUMS: {self.nc_sequences_count})",
            f"",
        ]
        return nc_lines

    def generate_nc_oper_body_lines(self) -> list:
        nc_lines = []
        for seq_obj in self.list_of_nc_sequences_objects:
            if seq_obj.is_file_needed:
                if seq_obj.is_m00_before_needed is True:
                    nc_lines.append("M00")
                nc_lines.extend([
                    f"M98P{seq_obj.nc_file_number}"
                    f"(OPER {seq_obj.nc_sequence_number}/{seq_obj.nc_sequences_count}: {seq_obj.nc_sequence_name})",
                    f"(POT: {seq_obj.tool_pot}, TOOL: {seq_obj.tool_name})",
                ])
                if seq_obj.is_m00_after_needed is True:
                    nc_lines.append("M00")
                nc_lines.append(f"")
        return nc_lines

    def generate_nc_oper_tail_lines(self) -> list:
        nc_lines = [
            "G53",
            "G00 Z0.0",
            "G00 X0.0 Y0.0",
            f"(MACHINING TIME: {self.sum_machining_time})",
            "M30",
        ]
        return nc_lines

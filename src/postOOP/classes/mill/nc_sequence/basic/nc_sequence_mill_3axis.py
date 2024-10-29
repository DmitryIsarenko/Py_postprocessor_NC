import logging
from src.postOOP import config
from src.postOOP.classes.mill.nc_operation.mixins.mixin_root import MixinRoot
from src.postOOP.classes.mill.parsers.pprint_parsers.basic.pprint_parser_basic import PprintParserBasic
from src.postOOP.classes.mill.parsers.ncl_parsers.basic.ncl_parser_mill_3axis import NclParserMill3axis
from src.postOOP.classes.file_operator_basic import FileOperatorBasic
from src.postOOP.classes.formatter import Formatter

logger = logging.getLogger(__name__)


class NcSequenceMill3Axis(MixinRoot):
    nc_sequence_class_name = "NcSequenceBasic"

    cur_X = 0
    cur_Y = 0
    cur_Z = 0
    cur_A = 0
    cur_B = 0
    cur_C = 0

    main_digit = config.PROGRAM_MAIN_DIGIT
    main_letter = config.PROGRAM_MAIN_LETTER
    file_extension = config.G_CODE_FILE_EXTENSION
    programmer_name = config.PROGRAMMER_NAME

    cl_list: list[str] = []
    nc_list: list[str] = []

    nc_start_keyword = config.NC_START_KEYWORD
    nc_end_keyword = config.NC_END_KEYWORD
    GOHOME_LINES = [
        f"G00 G28 Z0.0.",
        f"G00 G28 X0.0.",
        f"G00 G28 Y0.0.",
    ]

    nc_filename = None
    nc_file_number = None
    nc_filename_with_extension = None

    cl_start_index = None
    cl_end_index = None

    work_offset = None
    tool_name = None
    tool_pot = None
    tool_type = None
    spindle_master_data = None
    spindle_speed_master = None
    spindle_units_master = None
    spindle_direction_master = None
    cut_feed_master = None
    machining_time = None

    is_m00_before_needed = False
    is_m00_after_needed = False
    is_m01_needed = False
    is_gohome_needed = False



    def __init__(
            self,
            ncl_parser_class: NclParserMill3axis,
            pprint_parser_class: PprintParserBasic,
            file_operator_class: FileOperatorBasic,
            detail_name: str,
            nc_sequence_name: str,
            nc_sequence_parent_name_of_massive: str,
            nc_massive_copy_counter: int,
            cl_list: list,
            nc_operation_number: int,
            nc_sequence_number: int,
            nc_sequences_count: int,
            date_of_creation: str,
            **kwargs,
    ):


        self.ncl_parser_class = ncl_parser_class
        self.pprint_parser_class = pprint_parser_class
        self.file_operator_class = file_operator_class

        self.is_file_needed = True

        self.detail_name = detail_name
        self.nc_sequence_name = nc_sequence_name
        self.nc_sequence_parent_name_of_massive = nc_sequence_parent_name_of_massive
        self.cl_list = cl_list
        self.nc_operation_number = nc_operation_number
        self.nc_sequence_number = nc_sequence_number
        self.nc_sequences_count = nc_sequences_count
        self.nc_massive_copy_counter = nc_massive_copy_counter
        self.date_of_creation = date_of_creation
        self.set_nc_filename()

        self.set_cl_start_index()
        self.set_cl_end_index()

        self.set_work_offset()
        self.set_tool_name()
        self.set_tool_pot()
        self.set_tool_type()
        self.set_spindle_master_data()
        self.set_cut_feed_master()
        self.set_machining_time()

        self.nc_seq_head_lines = []
        self.nc_seq_body_lines = []
        self.nc_seq_tail_lines = []

        # self.nc_seq_head_lines = self.generate_nc_head_lines()

        self.nc_list = []

        super().__init__(**kwargs)

    def generate_nc_seq_head_body_tail_lists(self):
        # self.nc_list = self.combine_nc_head_body_tail_lines_in_one_list()
        self.nc_seq_head_lines = self.generate_nc_seq_head_lines()
        self.nc_seq_body_lines = self.generate_nc_seq_body_lines()
        self.nc_seq_tail_lines = self.generate_nc_seq_tail_lines()


    def create_seq_file(self):
        if self.is_file_needed:
            self.file_operator_class.create_file(
                filepath=f"{config.abs_path_to_selected_file}/../{self.nc_filename_with_extension}")

    def fill_seq_file(self):
        if self.is_file_needed:
            self.file_operator_class.append_lines_to_file(
                filepath=f"{config.abs_path_to_selected_file}/../{self.nc_filename_with_extension}",
                list_with_lines=self.nc_list)

    def set_cl_start_index(self):
        if self.nc_sequence_name == self.nc_sequence_parent_name_of_massive:
            self.cl_start_index = self.pprint_parser_class.get_index_of_occurence_in_cl_list_in_range(
                cl_list=self.cl_list,
                search_for=self.nc_sequence_name,
                nc_massive_copy_counter=self.nc_massive_copy_counter,
                start_index=0,
                end_index=len(
                    self.cl_list))
        elif self.nc_sequence_name in config.sequence_massive_names:
            cl_parent_seq_index = self.pprint_parser_class.get_index_of_occurence_in_cl_list_in_range(
                cl_list=self.cl_list,
                search_for=self.nc_sequence_parent_name_of_massive,
                nc_massive_copy_counter=0,
                start_index=0,
                end_index=len(
                    self.cl_list))

            self.cl_start_index = self.pprint_parser_class.get_index_of_occurence_in_cl_list_in_range(
                cl_list=self.cl_list,
                search_for=self.nc_sequence_name,
                nc_massive_copy_counter=self.nc_massive_copy_counter,
                start_index=cl_parent_seq_index,
                end_index=len(
                    self.cl_list))

        # logger.debug(f"\tcl lines info for {self.nc_sequence_name}")
        # logger.debug(f"\t\tstart index: {self.cl_start_index}")

    def set_cl_end_index(self):
        self.cl_end_index = self.pprint_parser_class.get_index_of_occurence_in_cl_list_in_range(cl_list=self.cl_list,
                                                                                                nc_massive_copy_counter=0,
                                                                                                search_for=config.NC_END_KEYWORD,
                                                                                                start_index=self.cl_start_index,
                                                                                                end_index=len(
                                                                                                    self.cl_list))
        # logger.debug(f"\t\tend   index: {self.cl_end_index}")

    def set_work_offset(self):
        self.work_offset = self.pprint_parser_class.get_work_offset(cl_list=self.cl_list)

    def set_machining_time(self):
        self.machining_time = self.pprint_parser_class.get_machining_time_in_cl_list(
            cl_list=self.cl_list[self.cl_start_index:self.cl_end_index])

    def set_tool_name(self):
        self.tool_name = self.pprint_parser_class.get_tool_name_in_cl_list_range(cl_list=self.cl_list,
                                                                                 start_index=self.cl_start_index,
                                                                                 end_index=self.cl_end_index)

    def set_tool_pot(self):
        self.tool_pot = self.pprint_parser_class.get_tool_pot_in_cl_list_range(cl_list=self.cl_list,
                                                                               start_index=self.cl_start_index,
                                                                               end_index=self.cl_end_index)

    def set_spindle_master_data(self):
        spindle_data = self.pprint_parser_class.get_spindle_data_in_cl_list_range(cl_list=self.cl_list,
                                                                                  start_index=self.cl_start_index,
                                                                                  end_index=self.cl_end_index)
        if spindle_data:
            self.spindle_speed_master = spindle_data[0]
            self.spindle_units_master = spindle_data[1]
            self.spindle_direction_master = spindle_data[2]

    def set_cut_feed_master(self):
        self.cut_feed_master = self.pprint_parser_class.get_cut_feed_in_cl_list_range(cl_list=self.cl_list,
                                                                                      start_index=self.cl_start_index,
                                                                                      end_index=self.cl_end_index)

    def set_nc_filename(self):
        if self.nc_sequence_number < 10:
            num_in_str = "0" + str(self.nc_sequence_number)
        elif self.nc_sequence_number < 99:
            num_in_str = str(self.nc_sequence_number)
        else:
            logger.critical(f"Too many nc sequences")
            raise ValueError
        self.nc_file_number = (config.PROGRAM_MAIN_DIGIT +
                               str(self.nc_operation_number) +
                               num_in_str)
        self.nc_filename = config.PROGRAM_MAIN_LETTER + self.nc_file_number
        self.nc_filename_with_extension = self.nc_filename + config.G_CODE_FILE_EXTENSION

    def combine_nc_seq_head_body_tail_lines_in_one_list(self):
        self.nc_seq_head_lines = self.generate_nc_seq_head_lines()
        nc_lines = list()
        nc_lines.extend(self.nc_seq_head_lines)
        nc_lines.extend(self.nc_seq_body_lines)
        nc_lines.extend(self.nc_seq_tail_lines)
        nc_lines = Formatter.append_line_endings_in_cl_list_or_str(cl_list_or_str=nc_lines)
        nc_lines = Formatter.append_line_wraps_in_cl_list_or_str(cl_list_or_str=nc_lines)
        self.nc_list = nc_lines


    def generate_nc_seq_head_lines(self) -> list:
        nc_lines = [
            f"(PART: {self.detail_name})",
            f"(DATE: {self.date_of_creation})",
            f"(PROG  NUM: {self.nc_sequence_number} / {self.nc_sequences_count})",
            f"(PROG: {self.nc_sequence_name})",
            f"(TOOL: {self.tool_name})",
            f"(POT:  {self.tool_pot})",
            # f"",
            f"G{self.work_offset}",
            f"{config.SAFETY_LINE_DEFAULT}"
        ]
        return nc_lines

    def generate_nc_seq_body_lines(self) -> list:
        nc_lines = self.ncl_parser_class.parse_cl_list(nc_seq_obj=self)
        return nc_lines

    @staticmethod
    def generate_nc_seq_tail_lines() -> list:
        nc_lines = list()
        nc_lines.extend(config.NC_SEQUENCE_TAIL_LINES)
        return nc_lines

    def add_nc_lines_to_object_nc_list(self, nc_lines_or_str: list[str] | str):
        if type(nc_lines_or_str) is list:
            self.nc_list.extend(nc_lines_or_str)
        elif type(nc_lines_or_str) is str:
            self.nc_list.append(nc_lines_or_str)
        else:
            raise TypeError

    def set_tool_type(self):
        self.tool_type = self.pprint_parser_class.get_tool_type(cl_list=self.cl_list,
                                                                start_index=self.cl_start_index,
                                                                end_index=self.cl_end_index)

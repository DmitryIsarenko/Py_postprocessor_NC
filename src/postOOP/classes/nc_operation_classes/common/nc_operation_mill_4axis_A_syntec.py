from src.postOOP.classes.nc_operation_classes.common.nc_operation_mill_3axis_syntec import NcOperationMill3AxisSyntec
from src.postOOP.classes.nc_sequence_classes.common.nc_sequence_mill_4axis_A_syntec import NcSequenceMill4AxisASyntec
from src.postOOP.classes.parsers.ncl_parsers.ncl_parser_mill_4axis_A_syntec import NclParserMill4AxisASyntec
from src.postOOP.classes.parsers.pprint_parsers.pprint_parser_mill_4axis import PprintParserMill4Axis
from src.postOOP import config
import logging

logger = logging.getLogger(__name__)


class NcOperationMill4AxisASyntec(NcOperationMill3AxisSyntec):
    nc_sequence_class: NcSequenceMill4AxisASyntec = NcSequenceMill4AxisASyntec
    pprint_parser_class: PprintParserMill4Axis = PprintParserMill4Axis
    ncl_parser_class: NclParserMill4AxisASyntec = NclParserMill4AxisASyntec

    postprocessor_name = "MILL 4AXIS A SYNTEC POST"
    is_multax_operation = False

    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)

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
            logger.debug(f"nc_sequence_name={nc_sequence_name}")
            logger.debug(f"nc_sequence_parent_name_of_massive={nc_sequence_parent_name_of_massive}")
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
                                       date_of_creation=self.date_of_creation,
                                       is_multax_operation=self.is_multax_operation,
                                       # multax_line_index=self.multax_line_index
                                       ))
        self.list_of_nc_sequences_objects: list = lst_of_objects
        # logger.debug(
        #     f"self.list_of_nc_sequences_objects {[item.nc_sequence_number for item in self.list_of_nc_sequences_objects]}")
        # logger.debug(
        #     f"self.list_of_nc_sequences_objects {[item.nc_sequence_name for item in self.list_of_nc_sequences_objects]}")

    def start_postprocessing(self):
        temp_filepath = self.file_operator_class.create_temp_formatted_ncl_file(filepath=self.filepath)
        self.cl_list = self.file_operator_class.get_all_cl_lines(filepath=temp_filepath)

        if self.cl_list:
            self.set_cl_lines_count()
            self.set_detail_name()
            self.set_date_of_creation()
            self.set_operation_name()
            self.set_operation_num_from_name()
            self.set_nc_filename()

            self.is_multax_operation = self.pprint_parser_class.get_is_oper_multax_in_cl_list(cl_list=self.cl_list)
            if self.is_multax_operation:
                self.multax_line_index = self.pprint_parser_class.get_index_of_occurence_in_cl_list_in_range(
                    cl_list=self.cl_list,
                    search_for="MULTAX / ON",
                    end_index=self.cl_lines_count)
            else:
                self.multax_line_index = None

            logger.info(f"Operation is Multax = {self.is_multax_operation}")

            self.set_nc_sequences_count()
            self.set_nc_sequences_names_in_list()
            self.set_nc_sequences_objects_in_list()
            self.set_sum_machining_time()

            # self.show()
            self.nc_list = self.generate_nc_list()
            # print(self.nc_list)
            self.file_operator_class.create_file(filepath=f"{config.CWD}/../{self.nc_filename_with_extension}")
            self.file_operator_class.append_lines_to_file(filepath=f"{config.CWD}/../{self.nc_filename_with_extension}",
                                                          list_with_lines=self.nc_list)


        else:
            logger.info(f"Empty self.cl_list for {self.filepath}")

        if config.DELETE_TEMP_FILE:
            self.file_operator_class.remove_file(filepath=temp_filepath)
        else:
            pass

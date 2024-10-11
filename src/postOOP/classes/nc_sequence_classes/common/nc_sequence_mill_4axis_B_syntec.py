from src.postOOP.classes.nc_sequence_classes.common.nc_sequence_mill_3axis_syntec import NcSequenceMill3AxisSyntec
import logging

logger = logging.getLogger(__name__)


class NcSequenceMill4AxisBSyntec(NcSequenceMill3AxisSyntec):
    nc_sequence_class_name = "NcSequenceMill4AxisBSyntec"
    is_multax_active = False
    is_multax_operation = False

    def __init__(
            self,
            ncl_parser_class,
            pprint_parser_class,
            file_operator_class,
            detail_name: str,
            nc_sequence_name: str,
            nc_sequence_parent_name_of_massive: str,
            nc_massive_copy_counter: int,
            cl_list: list,
            nc_operation_number: int,
            nc_sequence_number: int,
            nc_sequences_count: int,
            date_of_creation: str,
            is_multax_operation: bool,
    ):
        self.is_multax_operation = is_multax_operation
        super().__init__(
            ncl_parser_class=ncl_parser_class,
            pprint_parser_class=pprint_parser_class,
            file_operator_class=file_operator_class,
            detail_name=detail_name,
            nc_sequence_name=nc_sequence_name,
            nc_sequence_parent_name_of_massive=nc_sequence_parent_name_of_massive,
            cl_list=cl_list,
            nc_operation_number=nc_operation_number,
            nc_sequence_number=nc_sequence_number,
            nc_sequences_count=nc_sequences_count,
            nc_massive_copy_counter=nc_massive_copy_counter,
            date_of_creation=date_of_creation,
        )

        # if self.is_multax_operation and multax_line_index:
        #     if self.cl_start_index < multax_line_index < self.cl_end_index:
        #         self.is_multax_active = True
        #     else:
        #         self.is_multax_active = False

        # self.is_multax_active = bool(
        #     PprintParserMill4AxisA.get_index_of_occurence_in_cl_list_in_range(start_index=self.cl_start_index,
        #                                                                       end_index=self.cl_end_index,
        #                                                                       search_for="MULTAX / ON",
        #                                                                       cl_list=self.cl_list, ))
        # logger.debug(f"self.is_multax_active = {self.is_multax_active}")

    def generate_nc_body_lines(self) -> list:
        nc_lines = self.ncl_parser_class.parse_cl_list(nc_seq_obj=self)
        return nc_lines

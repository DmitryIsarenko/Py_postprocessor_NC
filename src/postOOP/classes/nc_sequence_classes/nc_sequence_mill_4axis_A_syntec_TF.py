from src.postOOP.classes.nc_sequence_classes.nc_sequence_mill_4axis_A_syntec import NcSequenceMill4AxisASyntec
from src.postOOP.classes.parsers.ncl_parsers.ncl_parser_mill_3axis_syntec import NclParserMill3axisSyntec
from src.postOOP.classes.parsers.pprint_parsers.pprint_parser_mill_4axis_A import PprintParserMill4AxisA
import logging

logger = logging.getLogger(__name__)

class NcSequenceMill4AxisASyntecTF(NcSequenceMill4AxisASyntec):
    nc_sequence_class_name = "NcSequenceMill4AxisASyntecTF"
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
            is_multax_operation=is_multax_operation,
        )

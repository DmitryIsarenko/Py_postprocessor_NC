from src.postOOP.classes.nc_sequence_classes.nc_sequence_basic_mill_syntec import NcSequenceMillBasicSyntec
from src.postOOP.classes.parsers.ncl_parsers.ncl_parser_mill_3axis_syntec_TF import NclParserMill3axisSyntecTF


class NcSequenceMill3AxisSyntecTF(NcSequenceMillBasicSyntec):
    nc_sequence_class_name = "NcSequenceMill3AxisSyntecTF"

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
            date_of_creation: str
    ):
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

        self.set_is_m00_before_needed()

    def set_m00_before_if_tool_type_is_boring_bar(self):
        if self.tool_type == "BORING BAR":
            self.is_m00_before_needed = True
        else:
            self.is_m00_before_needed = False

    def set_is_m00_before_needed(self):
        self.set_m00_before_if_tool_type_is_boring_bar()

    # def generate_nc_body_lines(self) -> list:
    #     nc_lines = NclParserMill3axisSyntecTF.parse_cl_list(nc_seq_obj=self)
    #     return nc_lines

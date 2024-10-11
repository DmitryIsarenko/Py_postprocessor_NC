from src.postOOP.classes.nc_sequence_classes.basic.nc_sequence_basic import NcSequenceBasic


class NcSequenceMillBasicSyntec(NcSequenceBasic):
    nc_sequence_class_name = "NcSequenceMillBasicSyntec"

    cur_X = 0
    cur_Y = 0
    cur_Z = 0
    cur_A = 0
    cur_B = 0
    cur_C = 0

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

    # def generate_nc_body_lines(self) -> list:
    #     nc_lines = NclParserBasicMillSyntec.parse_cl_list(nc_seq_obj=self)
    #     return nc_lines

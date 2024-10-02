from src.postOOP.classes.nc_sequence_classes.nc_sequence_mill_3axis_syntec import NcSequenceMill3AxisSyntec
from src.postOOP.classes.parsers.ncl_parsers.ncl_parser_mill_3axis_syntec import NclParserMill3axisSyntec


class NcSequenceMill4AxisASyntec(NcSequenceMill3AxisSyntec):
    def __init__(
            self,
            detail_name: str,
            nc_sequence_name: str,
            cl_list: list,
            nc_operation_number: int,
            nc_sequence_number: int,
            nc_sequences_count: int,
            date_of_creation: str
    ):
        super().__init__(
            detail_name=detail_name,
            nc_sequence_name=nc_sequence_name,
            cl_list=cl_list,
            nc_operation_number=nc_operation_number,
            nc_sequence_number=nc_sequence_number,
            nc_sequences_count=nc_sequences_count,
            date_of_creation=date_of_creation,
        )

    def generate_nc_body_lines(self) -> list:
        nc_lines = NclParserMill3axisSyntec.parse_cl_list(nc_seq_obj=self)
        return nc_lines

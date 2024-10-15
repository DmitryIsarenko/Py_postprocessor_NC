from src.postOOP.classes.nc_operation_classes.basic.nc_operation_basic_mill_syntec import NcOperationBasicMillSyntec
from src.postOOP.classes.nc_sequence_classes.tauras_fenix.nc_sequence_mill_3axis_syntec_TF import NcSequenceMill3AxisSyntecTF
from src.postOOP.classes.parsers.pprint_parsers.pprint_parser_basic import PprintParserBasic
from src.postOOP.classes.parsers.ncl_parsers.ncl_parser_mill_3axis_syntec_TF import NclParserMill3axisSyntecTF
from src.postOOP.classes.others.formatter import Formatter
from src.postOOP import config


class NcOperationMill3AxisSyntecTF(NcOperationBasicMillSyntec):
    nc_sequence_class: NcSequenceMill3AxisSyntecTF = NcSequenceMill3AxisSyntecTF
    pprint_parser_class: PprintParserBasic = PprintParserBasic
    ncl_parser_class: NclParserMill3axisSyntecTF = NclParserMill3axisSyntecTF

    postprocessor_name = "MILL 3AXIS SYNTEC TF POST"

    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)

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
            f"({self.detail_name}_{self.operation_name})",
            f"(PROGRAMMER=(NULL))",
            f"(DATA={self.date_of_creation})",
            f"(POST: {config.POST_NAME})",
            f"(PROG NUMS: {self.nc_sequences_count})",
        ]
        return nc_lines

    def generate_nc_body_lines(self) -> list:
        nc_lines = []
        for obj in self.list_of_nc_sequences_objects:
            if obj.is_m00_before_needed is True:
                nc_lines.append("M00")
            nc_lines.extend([
                f"M98P{obj.nc_file_number}//.T{obj.tool_pot}_{obj.tool_name}",
                f"({obj.nc_sequence_number}/{obj.nc_sequences_count}      {obj.nc_sequence_name})",
                # f"(           {obj.nc_sequence_name})",
            ])
            if obj.is_m00_after_needed is True:
                nc_lines.append("M00")
            nc_lines.append(f"")
        return nc_lines

    def generate_nc_tail_lines(self) -> list:
        nc_lines = [
            "G0 G53 Z0.0",
            "G00 X0.0",
            "G00 Y0.0",
            f"(MACHINING TIME: {self.sum_machining_time})",
            "M30",
        ]
        return nc_lines
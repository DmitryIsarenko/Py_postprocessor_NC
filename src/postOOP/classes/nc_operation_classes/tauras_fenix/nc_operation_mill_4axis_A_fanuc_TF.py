from src.postOOP.classes.nc_operation_classes.common.nc_operation_mill_4axis_A_syntec import NcOperationMill4AxisASyntec
from src.postOOP.classes.nc_sequence_classes.tauras_fenix.nc_sequence_mill_4axis_A_fanuc_TF import NcSequenceMill4AxisAFanucTF
from src.postOOP.classes.parsers.ncl_parsers.ncl_parser_mill_4axis_A_syntec_TF import NclParserMill4AxisASyntecTF
from src.postOOP.classes.parsers.pprint_parsers.pprint_parser_mill_4axis import PprintParserMill4Axis
from src.postOOP.classes.others.formatter import Formatter
from src.postOOP import config
import logging

logger = logging.getLogger(__name__)


class NcOperationMill4AxisAFanucTF(NcOperationMill4AxisASyntec):
    nc_sequence_class: NcSequenceMill4AxisAFanucTF = NcSequenceMill4AxisAFanucTF
    pprint_parser_class: PprintParserMill4Axis = PprintParserMill4Axis
    ncl_parser_class: NclParserMill4AxisASyntecTF = NclParserMill4AxisASyntecTF

    postprocessor_name = "MILL 4AXIS A FANUC TF POST"
    is_multax_operation = False

    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)

    def generate_nc_list(self) -> list:
        pre_percent = ["%", ]
        end_percent = ["%", ]
        nc_lines = list()
        nc_lines.extend(self.generate_nc_head_lines())
        nc_lines.extend(self.generate_nc_body_lines())
        nc_lines.extend(self.generate_nc_tail_lines())

        nc_lines = Formatter.append_line_endings_in_cl_list_or_str(cl_list_or_str=nc_lines)

        pre_percent.extend(nc_lines)
        all_lines = pre_percent
        all_lines.extend(end_percent)

        all_lines = Formatter.append_line_wraps_in_cl_list_or_str(cl_list_or_str=all_lines)
        return all_lines

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
import logging
from src.postOOP.classes.mill.parsers.ncl_parsers.basic.ncl_parser_mill_4axis_B import NclParserMill4AxisB
from src.postOOP.classes.mill.parsers.coord_parsers.rdy_to_use.coords_parser_TF import CoordsParser4axisTF
from src.postOOP import config

logger = logging.getLogger(__name__)


class NclParserMill4AxisB_TF(NclParserMill4AxisB):
    ncl_parser_class_name = "NclParserMill4AxisB_TF"
    coords_parser_class = CoordsParser4axisTF

    @classmethod
    def parse_COOLNT(cls, cl_list: list[str], line_index: int) -> list[str]:
        result_list = list()
        # right_part = cl_list[line_index].split(sep=" / ")[1]
        # if "ON" in right_part:
        #     result_list.append(f"M08")
        # elif "OFF" in right_part:
        #     result_list.append(f"M09")
        return result_list

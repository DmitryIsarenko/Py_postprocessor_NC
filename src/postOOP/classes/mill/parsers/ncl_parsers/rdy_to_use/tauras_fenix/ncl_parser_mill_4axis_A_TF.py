import logging

from src.postOOP.classes.mill.parsers.ncl_parsers.basic.ncl_parser_mill_4axis_A import NclParserMill4AxisA
from src.postOOP.classes.mill.parsers.coord_parsers.rdy_to_use.coords_parser_TF import CoordsParser4axisTF
from src.postOOP import config

logger = logging.getLogger(__name__)


class NclParserMill4AxisA_TF(NclParserMill4AxisA):
    ncl_parser_class_name = "NclParserMill4AxisA_TF"
    coords_parser_class = CoordsParser4axisTF

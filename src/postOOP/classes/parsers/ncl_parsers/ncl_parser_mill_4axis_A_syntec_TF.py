from src.postOOP import config
from src.postOOP.classes.parsers.ncl_parsers.ncl_parser_mill_4axis_A_syntec import NclParserMill4AxisASyntec
from src.postOOP.classes.parsers.coords_parser import CoordsParser
# from src.postOOP.classes.nc_sequence_classes.nc_sequence_mill_4axis_A_syntec import NcSequenceMill4AxisASyntec
import logging

logger = logging.getLogger(__name__)


class NclParserMill4AxisASyntecTF(NclParserMill4AxisASyntec):
    ncl_parser_class_name = "NclParserMill4axisASyntecTF"

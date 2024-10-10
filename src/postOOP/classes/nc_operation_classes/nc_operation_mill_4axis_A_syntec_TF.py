from src.postOOP.classes.nc_operation_classes.nc_operation_mill_4axis_A_syntec import NcOperationMill4AxisASyntec
from src.postOOP.classes.nc_sequence_classes.nc_sequence_mill_4axis_A_syntec_TF import NcSequenceMill4AxisASyntecTF
from src.postOOP.classes.parsers.ncl_parsers.ncl_parser_mill_4axis_A_syntec_TF import NclParserMill4AxisASyntecTF
from src.postOOP.classes.parsers.pprint_parsers.pprint_parser_mill_4axis_A import PprintParserMill4AxisA
from src.postOOP import config
import logging
from pprint import pprint

logger = logging.getLogger(__name__)


class NcOperationMill4AxisASyntecTF(NcOperationMill4AxisASyntec):
    nc_sequence_class: NcSequenceMill4AxisASyntecTF = NcSequenceMill4AxisASyntecTF
    pprint_parser_class: PprintParserMill4AxisA = PprintParserMill4AxisA
    ncl_parser_class: NclParserMill4AxisASyntecTF = NclParserMill4AxisASyntecTF

    postprocessor_name = "MILL 4AXIS A SYNTEC TF POST"
    is_multax_operation = False

    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)
from src.postOOP.classes.nc_operation_classes.nc_operation_mill_4axis_B_syntec import NcOperationMill4AxisBSyntec
from src.postOOP.classes.nc_sequence_classes.nc_sequence_mill_4axis_B_syntec_TF import NcSequenceMill4AxisBSyntecTF
from src.postOOP.classes.parsers.ncl_parsers.ncl_parser_mill_4axis_B_syntec_TF import NclParserMill4AxisBSyntecTF
from src.postOOP.classes.parsers.pprint_parsers.pprint_parser_mill_4axis_B import PprintParserMill4AxisB
from src.postOOP import config
import logging
from pprint import pprint

logger = logging.getLogger(__name__)


class NcOperationMill4AxisBSyntecTF(NcOperationMill4AxisBSyntec):
    nc_sequence_class: NcSequenceMill4AxisBSyntecTF = NcSequenceMill4AxisBSyntecTF
    pprint_parser_class: PprintParserMill4AxisB = PprintParserMill4AxisB
    ncl_parser_class: NclParserMill4AxisBSyntecTF = NclParserMill4AxisBSyntecTF

    postprocessor_name = "MILL 4AXIS B SYNTEC TF POST"
    is_multax_operation = False

    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)

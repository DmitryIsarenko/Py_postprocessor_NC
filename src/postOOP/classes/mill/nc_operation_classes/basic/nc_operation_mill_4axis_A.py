import logging

from src.postOOP.classes.mill.nc_operation_classes.basic.nc_operation_mill_3axis import NcOperationMill3Axis
from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_oper_4axis import MixinOper4Axis
from src.postOOP.classes.mill.nc_sequence_classes.basic.nc_sequence_mill_4axis import NcSequenceMill4Axis
from src.postOOP.classes.mill.parsers.ncl_parsers.ncl_parser_mill_4axis_A_syntec import NclParserMill4AxisASyntec
from src.postOOP.classes.mill.parsers.pprint_parsers.rdy_to_use.pprint_parser_mill_4axis import PprintParserMill4Axis

logger = logging.getLogger(__name__)


class NcOperationMill4AxisA(NcOperationMill3Axis, MixinOper4Axis):
    nc_sequence_class: NcSequenceMill4Axis = NcSequenceMill4Axis
    pprint_parser_class: PprintParserMill4Axis = PprintParserMill4Axis
    ncl_parser_class: NclParserMill4AxisASyntec = NclParserMill4AxisASyntec

    postprocessor_name = "NcOperationMill4AxisA"
    is_multax_operation = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_nc_sequences_objects_in_list(self):
        MixinOper4Axis(self).set_nc_sequences_objects_in_list()

    def start_postprocessing(self):
        MixinOper4Axis(self).start_postprocessing()

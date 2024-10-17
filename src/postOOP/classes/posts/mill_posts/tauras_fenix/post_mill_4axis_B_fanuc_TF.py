from src.postOOP.classes.nc_operation_classes.basic.nc_operation_basic import NcOperationMill3Axis
from src.postOOP.classes.nc_operation_classes.mixins.mixin_oper_4axis import MixinOper4Axis
from src.postOOP.classes.nc_operation_classes.mixins.mixin_oper_filler_fanuc_TF import MixinOperFillerFanucTF
from src.postOOP.classes.nc_sequence_classes.tauras_fenix.nc_sequence_mill_4axis_B_fanuc_TF import \
    NcSequenceMill4AxisBFanucTF
from src.postOOP.classes.parsers.ncl_parsers.ncl_parser_mill_4axis_B_syntec_TF import NclParserMill4AxisBSyntecTF
from src.postOOP.classes.parsers.pprint_parsers.pprint_parser_mill_4axis import PprintParserMill4Axis
import logging

logger = logging.getLogger(__name__)


class NcOperationMill4AxisBFanucTF(NcOperationMill3Axis, MixinOperFillerFanucTF, MixinOper4Axis):
    nc_sequence_class: NcSequenceMill4AxisBFanucTF = NcSequenceMill4AxisBFanucTF
    pprint_parser_class: PprintParserMill4Axis = PprintParserMill4Axis
    ncl_parser_class: NclParserMill4AxisBSyntecTF = NclParserMill4AxisBSyntecTF

    postprocessor_name = "MILL 4AXIS B FANUC TF POST"
    is_multax_operation = False

    def __init__(self, **kwargs):
        super().__init__(
            nc_oper_obj_for_fanuc_filler=self,
            nc_oper_obj_for_4axis=self,
            **kwargs,
        )

    # MixinOperFillerFanucTF
    def generate_nc_list(self) -> list:
        return MixinOperFillerFanucTF(self).generate_nc_list()

    def generate_nc_head_lines(self) -> list:
        return MixinOperFillerFanucTF(self).generate_nc_head_lines()

    def generate_nc_body_lines(self) -> list:
        return MixinOperFillerFanucTF(self).generate_nc_body_lines()

    def generate_nc_tail_lines(self) -> list:
        return MixinOperFillerFanucTF(self).generate_nc_tail_lines()

    # MixinOper4Axis
    def set_nc_sequences_objects_in_list(self):
        MixinOper4Axis(self).set_nc_sequences_objects_in_list()

    def start_postprocessing(self):
        MixinOper4Axis(self).start_postprocessing()

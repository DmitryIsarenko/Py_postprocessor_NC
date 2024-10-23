from src.postOOP.classes.mill.nc_operation_classes.basic.nc_operation_mill_3axis import NcOperationMill3Axis
from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_oper_4axis import MixinOper4Axis
from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_oper_filler_syntec_TF import \
    MixinOperFillerSyntecTF
from src.postOOP.classes.mill.nc_sequence_classes.rdy_to_use.tauras_fenix.nc_sequence_mill_4axis_syntec_TF import \
    NcSequenceMill4AxisSyntecTF
from src.postOOP.classes.mill.parsers.ncl_parsers.ncl_parser_mill_4axis_B_syntec_TF import NclParserMill4AxisBSyntecTF
from src.postOOP.classes.mill.parsers.pprint_parsers.pprint_parser_mill_4axis import PprintParserMill4Axis

import logging

logger = logging.getLogger(__name__)


class NcOperationMill4AxisBSyntecTF(NcOperationMill3Axis, MixinOperFillerSyntecTF, MixinOper4Axis):
    nc_sequence_class: NcSequenceMill4AxisSyntecTF = NcSequenceMill4AxisSyntecTF
    pprint_parser_class: PprintParserMill4Axis = PprintParserMill4Axis
    ncl_parser_class: NclParserMill4AxisBSyntecTF = NclParserMill4AxisBSyntecTF

    postprocessor_name = "MILL 4AXIS B SYNTEC TF POST"
    is_multax_operation = False

    def __init__(self, **kwargs):
        super().__init__(
            nc_oper_obj_for_syntec_filler=self,
            nc_oper_obj_for_4axis=self,
            **kwargs,
        )

    # MixinOperFillerSyntecTF
    def generate_nc_list(self) -> list:
        return MixinOperFillerSyntecTF(self).combine_nc_oper_head_body_tail_lines_in_one_list()

    def generate_nc_head_lines(self) -> list:
        return MixinOperFillerSyntecTF(self).generate_nc_oper_head_lines()

    def generate_nc_body_lines(self) -> list:
        return MixinOperFillerSyntecTF(self).generate_nc_oper_body_lines()

    def generate_nc_tail_lines(self) -> list:
        return MixinOperFillerSyntecTF(self).generate_nc_oper_tail_lines()

    # MixinOper4Axis
    def set_nc_sequences_objects_in_list(self):
        MixinOper4Axis(self).set_nc_sequences_objects_in_list()

    def start_postprocessing(self):
        MixinOper4Axis(self).start_postprocessing()

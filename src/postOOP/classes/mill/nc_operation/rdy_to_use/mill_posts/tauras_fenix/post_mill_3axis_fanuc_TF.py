from src.postOOP.classes.mill.nc_operation.basic.nc_operation_mill_3axis import NcOperationMill3Axis
from src.postOOP.classes.mill.nc_operation.mixins.mixin_oper_arrays_3axis import MixinOperArrays3Axis
from src.postOOP.classes.mill.nc_operation.mixins.mixin_oper_filler_fanuc_TF import \
    MixinOperFillerFanucTF
from src.postOOP.classes.mill.nc_sequence.rdy_to_use.tauras_fenix.nc_sequence_mill_3axis_fanuc_TF import \
    NcSequenceMill3AxisFanucTF
from src.postOOP.classes.mill.parsers.pprint_parsers.basic.pprint_parser_basic import PprintParserBasic
from src.postOOP.classes.mill.parsers.ncl_parsers.ncl_parser_mill_3axis_syntec_TF import NclParserMill3axisSyntecTF
from src.postOOP.classes.mill.parsers.pprint_parsers.rdy_to_use.pprint_parser_mill_3axis import PprintParserMill3Axis


class NcOperationMill3AxisFanucTF(NcOperationMill3Axis,
                                  MixinOperFillerFanucTF,
                                  MixinOperArrays3Axis,
                                  ):
    nc_sequence_class: NcSequenceMill3AxisFanucTF = NcSequenceMill3AxisFanucTF
    pprint_parser_class: PprintParserBasic = PprintParserMill3Axis
    ncl_parser_class: NclParserMill3axisSyntecTF = NclParserMill3axisSyntecTF

    postprocessor_name = "MILL 3AXIS FANUC TF POST"

    def __init__(self, **kwargs):
        super().__init__(
            nc_oper_obj_for_fanuc_filler=self,
            nc_oper_obj_for_arrays=self,
            **kwargs,
        )

    # MixinOperFillerSyntecTF
    def combine_nc_oper_head_body_tail_lines_in_one_list(self) -> list:
        return MixinOperFillerFanucTF(self).combine_nc_oper_head_body_tail_lines_in_one_list()

    def generate_nc_oper_head_lines(self) -> list:
        return MixinOperFillerFanucTF(self).generate_nc_oper_head_lines()

    def generate_nc_oper_body_lines(self) -> list:
        return MixinOperFillerFanucTF(self).generate_nc_oper_body_lines()

    def generate_nc_oper_tail_lines(self) -> list:
        return MixinOperFillerFanucTF(self).generate_nc_oper_tail_lines()

    # MixinOperArrays
    def start_postprocessing(self):
        return MixinOperArrays3Axis(self).start_postprocessing()

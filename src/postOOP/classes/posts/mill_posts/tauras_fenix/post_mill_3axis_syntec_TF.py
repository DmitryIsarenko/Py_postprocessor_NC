from src.postOOP.classes.mill.nc_operation_classes.basic.nc_operation_mill_3axis import NcOperationMill3Axis
from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_oper_arrays import MixinOperArrays
from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_oper_filler_syntec_TF import MixinOperFillerSyntecTF
from src.postOOP.classes.mill.nc_sequence_classes.rdy_to_use.tauras_fenix.nc_sequence_mill_3axis_syntec_TF import \
    NcSequenceMill3AxisSyntecTF
from src.postOOP.classes.mill.parsers.pprint_parsers.pprint_parser_basic import PprintParserBasic
from src.postOOP.classes.mill.parsers.ncl_parsers.ncl_parser_mill_3axis_syntec_TF import NclParserMill3axisSyntecTF


class NcOperationMill3AxisSyntecTF(NcOperationMill3Axis,
                                   MixinOperFillerSyntecTF,
                                   MixinOperArrays,
                                   ):
    nc_sequence_class: NcSequenceMill3AxisSyntecTF = NcSequenceMill3AxisSyntecTF
    pprint_parser_class: PprintParserBasic = PprintParserBasic
    ncl_parser_class: NclParserMill3axisSyntecTF = NclParserMill3axisSyntecTF

    postprocessor_name = "MILL 3AXIS SYNTEC TF POST"

    def __init__(self, **kwargs):
        super().__init__(
            nc_oper_obj_for_syntec_filler=self,
            nc_oper_obj_for_arrays=self,
            **kwargs,
        )

    # MixinOperFillerSyntecTF
    def generate_nc_list(self) -> list:
        return MixinOperFillerSyntecTF(self).generate_nc_list()

    def generate_nc_head_lines(self) -> list:
        return MixinOperFillerSyntecTF(self).generate_nc_head_lines()

    def generate_nc_body_lines(self) -> list:
        return MixinOperFillerSyntecTF(self).generate_nc_body_lines()

    def generate_nc_tail_lines(self) -> list:
        return MixinOperFillerSyntecTF(self).generate_nc_tail_lines()

    # MixinOperArrays
    def start_postprocessing(self):
        return MixinOperArrays(self).start_postprocessing()
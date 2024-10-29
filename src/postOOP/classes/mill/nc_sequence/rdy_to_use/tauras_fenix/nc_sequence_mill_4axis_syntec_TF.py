from src.postOOP.classes.mill.nc_sequence.basic.nc_sequence_mill_4axis import NcSequenceMill4Axis
from src.postOOP.classes.mill.nc_sequence.mixins.mixin_m0_before_boring_bar import \
    MixinM0BeforeBoringBar
from src.postOOP.classes.mill.nc_sequence.mixins.mixin_seq_arrays import MixinSeqArrays
from src.postOOP.classes.mill.nc_sequence.mixins.mixin_seq_filler_syntec_TF import \
    MixinSeqFillerSyntecTF
import logging

logger = logging.getLogger(__name__)


class NcSequenceMill4AxisSyntecTF(NcSequenceMill4Axis,
                                  MixinM0BeforeBoringBar,
                                  MixinSeqFillerSyntecTF,
                                  MixinSeqArrays,
                                  ):
    nc_sequence_class_name = "NcSequenceMill4AxisSyntecTF"

    # is_multax_active = False
    # is_multax_operation = False

    def __init__(self, **kwargs):
        super().__init__(
            nc_seq_obj_for_syntec_filler=self,
            nc_seq_obj_for_m0_before_boring_bar=self,
            nc_seq_obj_for_arrays=self,
            **kwargs,
        )

    # MixinM0BeforeBoringBar
    def set_m00_before_if_tool_type_is_boring_bar(self):
        MixinM0BeforeBoringBar(self).set_m00_before_if_tool_type_is_boring_bar()

    def set_is_m00_before_needed(self):
        MixinM0BeforeBoringBar(self).set_is_m00_before_needed()

    # MixinSeqFillerSyntecTF
    # def combine_nc_seq_head_body_tail_lines_in_one_list(self):
    #     return MixinSeqFillerSyntecTF(self).combine_nc_seq_head_body_tail_lines_in_one_list()

    def generate_nc_seq_head_lines(self):
        return MixinSeqFillerSyntecTF(self).generate_nc_seq_head_lines()

    def generate_nc_seq_body_lines(self):
        return MixinSeqFillerSyntecTF(self).generate_nc_seq_body_lines()

    def generate_nc_seq_tail_lines(self):
        return MixinSeqFillerSyntecTF(self).generate_nc_seq_tail_lines()

from src.postOOP.classes.mill.nc_sequence_classes.basic.nc_sequence_mill_3axis import NcSequenceMill3Axis
from src.postOOP.classes.mill.nc_sequence_classes.mixins_nc_sequence.mixin_m0_before_boring_bar import \
    MixinM0BeforeBoringBar
from src.postOOP.classes.mill.nc_sequence_classes.mixins_nc_sequence.mixin_seq_filler_fanuc_TF import \
    MixinSeqFillerFanucTF


class NcSequenceMill3AxisFanucTF(NcSequenceMill3Axis, MixinM0BeforeBoringBar, MixinSeqFillerFanucTF):
    nc_sequence_class_name = "NcSequenceMill3AxisFanucTF"

    def __init__(self, **kwargs):
        super().__init__(
            nc_seq_obj_for_fanuc_filler=self,
            nc_seq_obj_for_m0_before_boring_bar=self,
            **kwargs,
        )

    # MixinM0BeforeBoringBar
    def set_m00_before_if_tool_type_is_boring_bar(self):
        MixinM0BeforeBoringBar(self).set_m00_before_if_tool_type_is_boring_bar()

    def set_is_m00_before_needed(self):
        MixinM0BeforeBoringBar(self).set_is_m00_before_needed()

    # MixinSeqFillerFanucTF
    def combine_nc_head_body_tail_lines_in_one_list(self):
        return MixinSeqFillerFanucTF(self).generate_nc_list()

    def generate_nc_head_lines(self):
        return MixinSeqFillerFanucTF(self).generate_nc_head_lines()

    def generate_nc_body_lines(self):
        return MixinSeqFillerFanucTF(self).generate_nc_body_lines()

    def generate_nc_tail_lines(self):
        return MixinSeqFillerFanucTF(self).generate_nc_tail_lines()

    #
    #
    # def __init__(
    #         self,
    #         ncl_parser_class,
    #         pprint_parser_class,
    #         file_operator_class,
    #         detail_name: str,
    #         nc_sequence_name: str,
    #         nc_sequence_parent_name_of_massive: str,
    #         nc_massive_copy_counter: int,
    #         cl_list: list,
    #         nc_operation_number: int,
    #         nc_sequence_number: int,
    #         nc_sequences_count: int,
    #         date_of_creation: str
    # ):
    #     super().__init__(
    #         ncl_parser_class=ncl_parser_class,
    #         pprint_parser_class=pprint_parser_class,
    #         file_operator_class=file_operator_class,
    #         detail_name=detail_name,
    #         nc_sequence_name=nc_sequence_name,
    #         nc_sequence_parent_name_of_massive=nc_sequence_parent_name_of_massive,
    #         cl_list=cl_list,
    #         nc_operation_number=nc_operation_number,
    #         nc_sequence_number=nc_sequence_number,
    #         nc_sequences_count=nc_sequences_count,
    #         nc_massive_copy_counter=nc_massive_copy_counter,
    #         date_of_creation=date_of_creation,
    #     )
    #
    #
    #     self.set_is_m00_before_needed()
    #
    # def set_m00_before_if_tool_type_is_boring_bar(self):
    #     if self.tool_type == "BORING BAR":
    #         self.is_m00_before_needed = True
    #     else:
    #         self.is_m00_before_needed = False
    #
    # def set_is_m00_before_needed(self):
    #     self.set_m00_before_if_tool_type_is_boring_bar()
    #
    #
    # def generate_nc_list(self) -> list:
    #     pre_percent = ["%",]
    #     end_percent = ["%",]
    #     nc_lines = list()
    #     nc_lines.extend(self.generate_nc_head_lines())
    #     nc_lines.extend(self.generate_nc_body_lines())
    #     nc_lines.extend(self.generate_nc_tail_lines())
    #
    #     nc_lines = Formatter.append_line_endings_in_cl_list_or_str(cl_list_or_str=nc_lines)
    #
    #     pre_percent.extend(nc_lines)
    #     all_lines = pre_percent
    #     all_lines.extend(end_percent)
    #
    #     all_lines = Formatter.append_line_wraps_in_cl_list_or_str(cl_list_or_str=all_lines)
    #     return all_lines
    #
    # def generate_nc_head_lines(self) -> list:
    #     nc_lines = [
    #         f"{self.nc_filename} (DETAIL={self.detail_name})",
    #         f"({self.nc_sequence_name})",
    #         f"(PROG NUM: {self.nc_sequence_number} / {self.nc_sequences_count})",
    #         f"(DATA={self.date_of_creation})",
    #         f"(T{self.tool_pot}_{self.tool_name})",
    #         f"G{self.work_offset}",
    #         f"{config.SAFETY_LINE_DEFAULT}",
    #     ]
    #     return nc_lines
    #
    # def generate_nc_body_lines(self) -> list:
    #     nc_lines = self.ncl_parser_class.parse_cl_list(nc_seq_obj=self)
    #     return nc_lines
    #
    #
    # @staticmethod
    # def generate_nc_tail_lines() -> list:
    #     nc_lines = list()
    #     nc_lines.extend(config.NC_SEQUENCE_TAIL_LINES)
    #     return nc_lines

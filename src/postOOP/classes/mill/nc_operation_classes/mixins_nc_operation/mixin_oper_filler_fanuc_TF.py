from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_root import MixinRoot
from src.postOOP.classes.others.formatter import Formatter
from src.postOOP import config

""" pass into inheritance class

    def generate_nc_list(self):
        return MixinTFOperFillerFanuc(self).generate_nc_list()

    def generate_nc_head_lines(self):
        return MixinTFOperFillerFanuc(self).generate_nc_head_lines()

    def generate_nc_body_lines(self):
        return MixinTFOperFillerFanuc(self).generate_nc_body_lines()

    def generate_nc_tail_lines(self):
        return MixinTFOperFillerFanuc(self).generate_nc_tail_lines()

"""


class MixinOperFillerFanucTF(MixinRoot):
    def __init__(self, nc_oper_obj_for_fanuc_filler, **kwargs):
        self.nc_oper_obj = nc_oper_obj_for_fanuc_filler
        super().__init__(**kwargs)

    def combine_nc_oper_head_body_tail_lines_in_one_list(self) -> list:
        pre_percent = [r"%", ]
        end_percent = [r"%", ]
        nc_lines = list()
        nc_lines.extend(self.nc_oper_obj.generate_nc_oper_head_lines())
        nc_lines.extend(self.nc_oper_obj.generate_nc_oper_body_lines())
        nc_lines.extend(self.nc_oper_obj.generate_nc_oper_tail_lines())

        nc_lines = Formatter.append_line_endings_in_cl_list_or_str(cl_list_or_str=nc_lines)

        pre_percent.extend(nc_lines)
        all_lines = pre_percent
        all_lines.extend(end_percent)

        all_lines = Formatter.append_line_wraps_in_cl_list_or_str(cl_list_or_str=all_lines)
        return all_lines

    def generate_nc_oper_head_lines(self) -> list:
        nc_lines = [
            f"({self.nc_oper_obj.detail_name}_{self.nc_oper_obj.operation_name})",
            f"(PROGRAMMER=(NULL))",
            f"(DATA={self.nc_oper_obj.date_of_creation})",
            f"(POST: {config.POST_NAME})",
            f"(PROG NUMS: {self.nc_oper_obj.nc_sequences_count})",
        ]
        return nc_lines

    def generate_nc_oper_body_lines(self) -> list:
        nc_lines = []
        for seq_obj in self.nc_oper_obj.list_of_nc_sequences_objects:
            if seq_obj.is_file_needed:
                if seq_obj.is_m00_before_needed is True:
                    nc_lines.append("M00")
                nc_lines.extend([
                    f"M98P{seq_obj.nc_file_number}//.T{seq_obj.tool_pot}_{seq_obj.tool_name}",
                    f"({seq_obj.nc_sequence_number}/{seq_obj.nc_sequences_count}      {seq_obj.nc_sequence_name})",
                    # f"(           {seq_obj.nc_sequence_name})",
                ])
                if seq_obj.is_m00_after_needed is True:
                    nc_lines.append("M00")
                nc_lines.append(f"")
        return nc_lines

    def generate_nc_oper_tail_lines(self) -> list:
        nc_lines = [
            "G0 G53 Z0.0",
            "G00 X0.0",
            "G00 Y0.0",
            f"(MACHINING TIME: {self.nc_oper_obj.sum_machining_time})",
            "M30",
        ]
        return nc_lines

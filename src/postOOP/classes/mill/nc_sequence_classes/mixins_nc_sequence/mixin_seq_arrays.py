from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_root import MixinRoot
from src.postOOP.classes.others.formatter import Formatter


class MixinArrays(MixinRoot):
    def __init__(self,
                 nc_seq_obj_for_arrays,
                 **kwargs):
        self.s = nc_seq_obj_for_arrays
        self.s.is_copy = False
        super().__init__(**kwargs)

    def generate_nc_list(self) -> list:
        nc_lines = list()

        if self.s.is_copy is False:
            nc_lines.extend(self.s.nc_seq_head_lines)

        nc_lines.extend(self.s.nc_seq_body_lines)

        if self.s.is_copy is False:
            nc_lines.extend(self.s.nc_seq_tail_lines)

        nc_lines = Formatter.append_line_endings_in_cl_list_or_str(cl_list_or_str=nc_lines)
        nc_lines = Formatter.append_line_wraps_in_cl_list_or_str(cl_list_or_str=nc_lines)
        return nc_lines


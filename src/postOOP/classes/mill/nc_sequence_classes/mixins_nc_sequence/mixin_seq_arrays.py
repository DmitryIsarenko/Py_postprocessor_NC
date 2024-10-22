from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_root import MixinRoot
from src.postOOP.classes.others.formatter import Formatter

import logging

logger = logging.getLogger(__name__)

class MixinArrays(MixinRoot):
    def __init__(self,
                 nc_seq_obj_for_arrays,
                 **kwargs):
        self.s = nc_seq_obj_for_arrays
        self.s.is_copy = False
        self.s.is_array = self.set_is_array()
        if self.s.is_array:
            self.s.is_param_array = self.set_is_parameter_array()
            self.s.array_copies_amount = self.set_array_copies_amount()
        logger.debug(f"{self.s.nc_sequence_name} : self.s.is_array: {self.s.is_array}")
        logger.debug(f"{self.s.nc_sequence_name} : self.s.is_param_array: {self.s.is_param_array}")
        logger.debug(f"{self.s.nc_sequence_name} : self.s.array_copies_amount: {self.s.array_copies_amount}")

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

    def set_is_array(self):
        return self.s.pprint_parser_class.get_is_array(cl_list=self.s.cl_list,
                                                       start_index=self.s.cl_start_index,
                                                       end_index=self.s.cl_end_index)

    def set_is_parameter_array(self):
        return self.s.pprint_parser_class.get_is_parameter_array(cl_list=self.s.cl_list,
                                                                 start_index=self.s.cl_start_index,
                                                                 end_index=self.s.cl_end_index)

    def set_array_copies_amount(self):
        return self.s.pprint_parser_class.get_array_copies_amount(cl_list=self.s.cl_list,
                                                                  start_index=self.s.cl_start_index,
                                                                  end_index=self.s.cl_end_index)

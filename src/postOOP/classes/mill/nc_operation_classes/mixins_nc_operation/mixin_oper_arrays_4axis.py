from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_oper_arrays_3axis import \
    MixinOperArrays3Axis
from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_root import MixinRoot
from src.postOOP import config
import logging

logger = logging.getLogger(__name__)


class MixinOperArrays4Axis(MixinOperArrays3Axis, MixinRoot):
    def __init__(self,
                 nc_oper_obj_for_arrays,
                 **kwargs, ):
        self.o = nc_oper_obj_for_arrays
        super().__init__(
            nc_oper_obj_for_arrays=self.o,
            **kwargs)

    def check_multax(self):
        self.o.is_multax_operation = self.o.pprint_parser_class.get_is_oper_multax_in_cl_list(
            cl_list=self.o.cl_list)
        if self.o.is_multax_operation:
            self.o.multax_line_index = self.o.pprint_parser_class.get_index_of_occurence_in_cl_list_in_range(
                cl_list=self.o.cl_list,
                search_for="MULTAX / ON",
                end_index=self.o.cl_lines_count)
        else:
            self.o.multax_line_index = None

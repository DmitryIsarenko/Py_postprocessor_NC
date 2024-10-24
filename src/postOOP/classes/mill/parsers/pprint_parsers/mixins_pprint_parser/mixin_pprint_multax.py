from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_root import MixinRoot


class MixinPprintMultax(MixinRoot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def get_is_oper_multax_in_cl_list(cl_list: list[str]) -> bool:
        for line in cl_list:
            if "MULTAX / ON" in line:
                return True
        else:
            return False
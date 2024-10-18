from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_root import MixinRoot

""" pass into inheritance class

def set_m00_before_if_tool_type_is_boring_bar(self):
    MixinM0BeforeBoringBar(self).set_m00_before_if_tool_type_is_boring_bar()

def set_is_m00_before_needed(self):
    MixinM0BeforeBoringBar(self).set_is_m00_before_needed()

"""


class MixinM0BeforeBoringBar(MixinRoot):
    def __init__(
            self,
            nc_seq_obj_for_m0_before_boring_bar,
            **kwargs
    ):
        self.nc_seq_obj = nc_seq_obj_for_m0_before_boring_bar
        super().__init__(**kwargs)

    def set_m00_before_if_tool_type_is_boring_bar(self):
        if self.nc_seq_obj.tool_type == "BORING BAR":
            self.nc_seq_obj.is_m00_before_needed = True
        else:
            self.nc_seq_obj.is_m00_before_needed = False


    def set_is_m00_before_needed(self):
        self.nc_seq_obj.set_m00_before_if_tool_type_is_boring_bar()



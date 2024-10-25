from src.postOOP.classes.mill.nc_operation.rdy_to_use.mill_posts.tauras_fenix.post_mill_3axis_fanuc_TF import \
    NcOperationMill3AxisFanucTF
from src.postOOP.classes.mill.nc_operation.rdy_to_use.mill_posts.tauras_fenix.post_mill_3axis_syntec_TF import NcOperationMill3AxisSyntecTF
from src.postOOP.classes.mill.nc_operation.rdy_to_use.mill_posts.tauras_fenix.post_mill_4axis_A_fanuc_TF import \
    NcOperationMill4AxisAFanucTF
from src.postOOP.classes.mill.nc_operation.rdy_to_use.mill_posts.tauras_fenix.post_mill_4axis_A_syntec_TF import \
    NcOperationMill4AxisASyntecTF
from src.postOOP.classes.mill.nc_operation.rdy_to_use.mill_posts.tauras_fenix.post_mill_4axis_B_fanuc_TF import \
    NcOperationMill4AxisBFanucTF
from src.postOOP.classes.mill.nc_operation.rdy_to_use.mill_posts.tauras_fenix.post_mill_4axis_B_syntec_TF import \
NcOperationMill4AxisBSyntecTF


class PostLister:
    post_dict = dict()

    def __init__(self):
        self.set_default_post(NcOperationMill4AxisASyntecTF)

        # self.add_post_to_list("--- debug ---")
        # self.add_post_to_list(NcOperationBasic)
        # self.add_post_to_list(NcOperationBasicMill)
        # # self.add_post_to_list("--- common fanuc ---")
        #
        # self.add_post_to_list(" ")
        # self.add_post_to_list("--- common syntec ---")
        # self.add_post_to_list(NcOperationMill3Axis)
        # self.add_post_to_list(NcOperationMill4AxisA)
        # self.add_post_to_list(NcOperationMill4AxisB)

        self.add_post_to_list("   ")
        self.add_post_to_list("--- TF syntec ---")
        self.add_post_to_list(NcOperationMill3AxisSyntecTF)
        self.add_post_to_list(NcOperationMill4AxisASyntecTF)
        self.add_post_to_list(NcOperationMill4AxisBSyntecTF)

        self.add_post_to_list("  ")
        self.add_post_to_list("--- TF fanuc ---")
        self.add_post_to_list(NcOperationMill3AxisFanucTF)
        self.add_post_to_list(NcOperationMill4AxisAFanucTF)
        self.add_post_to_list(NcOperationMill4AxisBFanucTF)

    @classmethod
    def add_post_to_list(cls, nc_oper_class):
        if type(nc_oper_class) is str:
            cls.post_dict.update({nc_oper_class: None})
        else:
            cls.post_dict.update({nc_oper_class.postprocessor_name: nc_oper_class})

    @classmethod
    def set_default_post(cls, nc_oper_class):
        cls.default_post_obj = nc_oper_class
        cls.default_post_name = nc_oper_class.postprocessor_name
        return

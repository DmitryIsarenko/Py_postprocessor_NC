from src.postOOP.classes.nc_operation_classes.basic.nc_operation_basic import NcOperationBasic
from src.postOOP.classes.nc_operation_classes.basic.nc_operation_basic_mill_syntec import NcOperationBasicMillSyntec
from src.postOOP.classes.nc_operation_classes.common.nc_operation_mill_3axis_syntec import NcOperationMill3AxisSyntec
from src.postOOP.classes.nc_operation_classes.common.nc_operation_mill_4axis_A_syntec import NcOperationMill4AxisASyntec
from src.postOOP.classes.nc_operation_classes.common.nc_operation_mill_4axis_B_syntec import NcOperationMill4AxisBSyntec
from src.postOOP.classes.nc_operation_classes.tauras_fenix.nc_operation_mill_3axis_syntec_TF import \
    NcOperationMill3AxisSyntecTF
from src.postOOP.classes.nc_operation_classes.tauras_fenix.nc_operation_mill_4axis_A_syntec_TF import \
    NcOperationMill4AxisASyntecTF
from src.postOOP.classes.nc_operation_classes.tauras_fenix.nc_operation_mill_4axis_B_syntec_TF import \
    NcOperationMill4AxisBSyntecTF
from src.postOOP.classes.nc_operation_classes.tauras_fenix.nc_operation_mill_3axis_fanuc_TF import \
    NcOperationMill3AxisFanucTF
from src.postOOP.classes.nc_operation_classes.tauras_fenix.nc_operation_mill_4axis_A_fanuc_TF import \
    NcOperationMill4AxisAFanucTF
from src.postOOP.classes.nc_operation_classes.tauras_fenix.nc_operation_mill_4axis_B_fanuc_TF import \
    NcOperationMill4AxisBFanucTF


class PostLister:
    post_dict = dict()

    def __init__(self):
        self.set_default_post(NcOperationBasicMillSyntec)

        self.add_post_to_list("--- debug ---")
        self.add_post_to_list(NcOperationBasic)
        self.add_post_to_list(NcOperationBasicMillSyntec)
        # self.add_post_to_list("--- common fanuc ---")

        self.add_post_to_list(" ")
        self.add_post_to_list("--- common syntec ---")
        self.add_post_to_list(NcOperationMill3AxisSyntec)
        self.add_post_to_list(NcOperationMill4AxisASyntec)
        self.add_post_to_list(NcOperationMill4AxisBSyntec)

        self.add_post_to_list("  ")
        self.add_post_to_list("--- TF fanuc ---")
        self.add_post_to_list(NcOperationMill3AxisFanucTF)
        self.add_post_to_list(NcOperationMill4AxisAFanucTF)
        self.add_post_to_list(NcOperationMill4AxisBFanucTF)

        self.add_post_to_list("   ")
        self.add_post_to_list("--- TF syntec ---")
        self.add_post_to_list(NcOperationMill3AxisSyntecTF)
        self.add_post_to_list(NcOperationMill4AxisASyntecTF)
        self.add_post_to_list(NcOperationMill4AxisBSyntecTF)


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


    # post_dict = {
    #     NcOperationBasic.postprocessor_name: NcOperationBasic,
    #     "----------basic SYNTEC:----------": NcOperationMill3AxisSyntec,
    #     NcOperationMill3AxisSyntec.postprocessor_name: NcOperationMill3AxisSyntec,
    #     NcOperationMill4AxisASyntec.postprocessor_name: NcOperationMill4AxisASyntec,
    #     NcOperationMill4AxisBSyntec.postprocessor_name: NcOperationMill4AxisBSyntec,
    #     "----------TF SYNTEC:----------": NcOperationMill3AxisSyntecTF,
    #     NcOperationMill3AxisSyntecTF.postprocessor_name: NcOperationMill3AxisSyntecTF,
    #     NcOperationMill4AxisASyntecTF.postprocessor_name: NcOperationMill4AxisASyntecTF,
    #
    #     NcOperationMill4AxisBSyntecTF.postprocessor_name: NcOperationMill4AxisBSyntecTF,
    #     "----------TF Fanuc:----------": NcOperationMill3AxisFanucTF,
    #     NcOperationMill3AxisFanucTF.postprocessor_name: NcOperationMill3AxisFanucTF,
    #     NcOperationMill4AxisAFanucTF.postprocessor_name: NcOperationMill4AxisAFanucTF,
    #     NcOperationMill4AxisBFanucTF.postprocessor_name: NcOperationMill4AxisBFanucTF,
    # }

    # 3axis TF
    # default_post_obj = post_dict[NcOperationMill3AxisSyntecTF.postprocessor_name]
    # default_post_name = NcOperationMill3AxisSyntecTF.postprocessor_name

    # 4axis basic
    # default_post_obj = post_dict[NcOperationMill4AxisBSyntec.postprocessor_name]
    # default_post_name = NcOperationMill4AxisBSyntec.postprocessor_name

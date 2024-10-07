from src.postOOP.classes.nc_operation_classes.nc_operation_basic import NcOperationBasic
from src.postOOP.classes.nc_operation_classes.nc_operation_mill_3axis_syntec import NcOperationMill3AxisSyntec
from src.postOOP.classes.nc_operation_classes.nc_operation_mill_3axis_syntec_TF import NcOperationMill3AxisSyntecTF
from src.postOOP.classes.nc_operation_classes.nc_operation_mill_4axis_A_syntec import NcOperationMill4AxisASyntec


class PostLister:
    post_dict = {
        # NcOperationBasic.postprocessor_name: NcOperationBasic,
        NcOperationMill3AxisSyntec.postprocessor_name: NcOperationMill3AxisSyntec,
        NcOperationMill3AxisSyntecTF.postprocessor_name: NcOperationMill3AxisSyntecTF,
        NcOperationMill4AxisASyntec.postprocessor_name: NcOperationMill4AxisASyntec,
    }

    # 3axis TF
    # default_post_obj = post_dict[NcOperationMill3AxisSyntecTF.postprocessor_name]
    # default_post_name = NcOperationMill3AxisSyntecTF.postprocessor_name
    # 4axis basic
    default_post_obj = post_dict[NcOperationMill4AxisASyntec.postprocessor_name]
    default_post_name = NcOperationMill4AxisASyntec.postprocessor_name

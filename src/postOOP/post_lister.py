from src.postOOP.classes.nc_operation_classes.common.nc_operation_mill_3axis_syntec import NcOperationMill3AxisSyntec
from src.postOOP.classes.nc_operation_classes.common.nc_operation_mill_4axis_A_syntec import NcOperationMill4AxisASyntec
from src.postOOP.classes.nc_operation_classes.common.nc_operation_mill_4axis_B_syntec import NcOperationMill4AxisBSyntec
from src.postOOP.classes.nc_operation_classes.tauras_fenix.nc_operation_mill_3axis_syntec_TF import NcOperationMill3AxisSyntecTF
from src.postOOP.classes.nc_operation_classes.tauras_fenix.nc_operation_mill_4axis_A_syntec_TF import NcOperationMill4AxisASyntecTF
from src.postOOP.classes.nc_operation_classes.tauras_fenix.nc_operation_mill_4axis_B_syntec_TF import NcOperationMill4AxisBSyntecTF
from src.postOOP.classes.nc_operation_classes.tauras_fenix.nc_operation_mill_3axis_fanuc_TF import NcOperationMill3AxisFanucTF
from src.postOOP.classes.nc_operation_classes.tauras_fenix.nc_operation_mill_4axis_A_fanuc_TF import NcOperationMill4AxisAFanucTF
from src.postOOP.classes.nc_operation_classes.tauras_fenix.nc_operation_mill_4axis_B_fanuc_TF import NcOperationMill4AxisBFanucTF



class PostLister:
    post_dict = {
        # NcOperationBasic.postprocessor_name: NcOperationBasic,
        "----------basic SYNTEC:----------":NcOperationMill3AxisSyntec,
        NcOperationMill3AxisSyntec.postprocessor_name: NcOperationMill3AxisSyntec,
        NcOperationMill4AxisASyntec.postprocessor_name: NcOperationMill4AxisASyntec,
        NcOperationMill4AxisBSyntec.postprocessor_name: NcOperationMill4AxisBSyntec,
        "----------TF SYNTEC:----------":NcOperationMill3AxisSyntecTF,
        NcOperationMill3AxisSyntecTF.postprocessor_name: NcOperationMill3AxisSyntecTF,
        NcOperationMill4AxisASyntecTF.postprocessor_name: NcOperationMill4AxisASyntecTF,

        NcOperationMill4AxisBSyntecTF.postprocessor_name: NcOperationMill4AxisBSyntecTF,
        "----------TF Fanuc:----------":NcOperationMill3AxisFanucTF,
        NcOperationMill3AxisFanucTF.postprocessor_name: NcOperationMill3AxisFanucTF,
        NcOperationMill4AxisAFanucTF.postprocessor_name: NcOperationMill4AxisAFanucTF,
        NcOperationMill4AxisBFanucTF.postprocessor_name: NcOperationMill4AxisBFanucTF,
    }

    # 3axis TF
    # default_post_obj = post_dict[NcOperationMill3AxisSyntecTF.postprocessor_name]
    # default_post_name = NcOperationMill3AxisSyntecTF.postprocessor_name
    # 4axis basic
    default_post_obj = post_dict[NcOperationMill4AxisBSyntec.postprocessor_name]
    default_post_name = NcOperationMill4AxisBSyntec.postprocessor_name

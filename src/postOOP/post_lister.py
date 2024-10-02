from src.postOOP.classes.nc_operation_classes.nc_operation_basic import NcOperation
from src.postOOP.classes.nc_operation_classes.nc_operation_mill_3axis_syntec import NcOperationMill3AxisSyntec
from src.postOOP.classes.nc_operation_classes.nc_operation_mill_3axis_syntec_TF import NcOperationMill3AxisSyntecTF


class PostLister:
    post_dict = {
        NcOperation.postprocessor_name: NcOperation,
        NcOperationMill3AxisSyntec.postprocessor_name: NcOperationMill3AxisSyntec,
        NcOperationMill3AxisSyntecTF.postprocessor_name: NcOperationMill3AxisSyntecTF,
    }

    default_post_obj = post_dict[NcOperationMill3AxisSyntecTF.postprocessor_name]
    default_post_name = NcOperationMill3AxisSyntecTF.postprocessor_name

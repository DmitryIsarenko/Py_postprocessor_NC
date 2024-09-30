from src.postOOP.classes.nc_operation_classes.nc_operation_basic import NcOperation
from src.postOOP.classes.nc_operation_classes.nc_operation_mill_3axis_syntec import NcOperationMill3Axis
from src.postOOP.classes.nc_operation_classes.nc_operation_mill_3axis_tf_syntec import NcOperationMill3AxisTF


class PostLister:
    post_dict = {
        NcOperation.postprocessor_name: NcOperation,
        NcOperationMill3Axis.postprocessor_name: NcOperationMill3Axis,
        NcOperationMill3AxisTF.postprocessor_name: NcOperationMill3AxisTF,
    }

    default_post_obj = post_dict[NcOperationMill3AxisTF.postprocessor_name]
    default_post_name = NcOperationMill3AxisTF.postprocessor_name

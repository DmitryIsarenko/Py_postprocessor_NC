import sys
from time import sleep

from src.postOOP.classes.nc_operation_classes.tauras_fenix.nc_operation_mill_3axis_syntec_TF import NcOperationMill3AxisSyntecTF
from src.postOOP import config


# def execute_postprocess(post_obj, work_dir_path: str):
def execute_postprocess(post_obj):
    operations = list()

    filepath = config.work_ncl_file_path
    if filepath:
        # operations.append(post_obj(filepath=filepath))
        operations.append(post_obj())

    for operation in operations:
        operation.start_postprocessing()

    sleep(2)

if __name__ == "__main__":
    post_obj = NcOperationMill3AxisSyntecTF
    # execute_postprocess(post_obj=post_obj, work_dir_path=sys.path[1])
    execute_postprocess(post_obj=post_obj)

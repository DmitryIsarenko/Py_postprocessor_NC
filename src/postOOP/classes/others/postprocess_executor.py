import sys

from src.postOOP.classes.others.file_operator_basic import FileOperatorBasic
from src.postOOP.classes.nc_operation_classes.tauras_fenix.nc_operation_mill_3axis_syntec_TF import NcOperationMill3AxisSyntecTF
from src.postOOP import config

# old version
# def execute_postprocess(post_obj, work_dir_path: str):
#     if config.DEBUG:
#         filepaths = FileOperatorBasic.get_all_ncl_files_in_dir(path=config.DEBUG_CWD)
#     else:
#         filepaths = FileOperatorBasic.get_all_ncl_files_in_dir(path=work_dir_path)
#     operations = list()
#     if filepaths:
#         for filepath in filepaths:
#             operations.append(post_obj(filepath=filepath))
#
#     for operation in operations:
#         operation.start_postprocessing()


def execute_postprocess(post_obj, work_dir_path: str):
    operations = list()
    # filepaths = list()
    #
    # if config.DEBUG:
    #     filepaths = FileOperatorBasic.get_all_ncl_files_in_dir(path=config.DEBUG_CWD)
    #     if filepaths:
    #         for filepath in filepaths:
    #             operations.append(post_obj(filepath=filepath))

    # else:
    filepath = config.CWD
    if filepath:
        operations.append(post_obj(filepath=filepath))

    for operation in operations:
        operation.start_postprocessing()


if __name__ == "__main__":
    post_obj = NcOperationMill3AxisSyntecTF
    execute_postprocess(post_obj=post_obj, work_dir_path=sys.path[1])

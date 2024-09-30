import sys

from src.postOOP.classes.others.file_operator import FileOperator
from src.postOOP.classes.nc_operation_classes.nc_operation_mill_3axis_tf_syntec import NcOperationMill3AxisTF


def execute_postprocess(post_obj, work_dir_path: str):
    filepaths = FileOperator.get_all_ncl_files_in_dir(path=work_dir_path)
    operations = list()
    if filepaths:
        for filepath in filepaths:
            operations.append(post_obj(filepath=filepath))

    for operation in operations:
        operation.start_postprocessing()


if __name__ == "__main__":
    post_obj = NcOperationMill3AxisTF
    execute_postprocess(post_obj=post_obj, work_dir_path=sys.path[1])

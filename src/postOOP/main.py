from src.postOOP.classes.others.file_operator import FileOperator
from src.postOOP.classes.nc_operation_classes.nc_operation import NcOperation
from src.postOOP.classes.nc_operation_classes.nc_operation_mill_3axis import (NcOperationMill3Axis,
                                                                              NcOperationMill3AxisTF)


def main():
    filepaths = FileOperator.get_all_ncl_files_in_dir()
    if filepaths:
        for filepath in filepaths:
            # NcOperation(filepath=filepath)
            # NcOperationMill3Axis(filepath=filepath)
            NcOperationMill3AxisTF(filepath=filepath)


if __name__ == "__main__":
    main()

from src.postOOP.classes.others.file_operator import FileOperator
from src.postOOP.classes.nc_operation_classes.nc_operation import NcOperation
from src.postOOP.classes.nc_operation_classes.nc_operation_mill_3axis import (NcOperationMill3Axis,
                                                                              NcOperationMill3AxisTF)


def main():
    filepaths = FileOperator.get_all_ncl_files_in_dir()
    operations = list()
    if filepaths:
        for filepath in filepaths:
            # operations.append(NcOperation(filepath=filepath))
            # operations.append(NcOperationMill3Axis(filepath=filepath))
            operations.append(NcOperationMill3AxisTF(filepath=filepath))

    for operation in operations:
        operation.start_postprocessing()


if __name__ == "__main__":
    main()

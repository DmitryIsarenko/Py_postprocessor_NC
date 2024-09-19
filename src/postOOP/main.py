from pprint import pprint
from src.postOOP.classes.file_operator import FileOperator
from src.postOOP.classes.nc_operation import NcOperation


def main():
    filepaths = FileOperator.get_all_ncl_files_in_dir()
    if filepaths:
        for filepath in filepaths:
            NcOperation(filepath=filepath)


if __name__ == "__main__":
    main()

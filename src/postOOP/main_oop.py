from src.postOOP.classes.file_operator import FileOperator
from src.postOOP.classes.nc_program import NcOperation

def main():
    filepaths = FileOperator.get_all_ncl_files_in_dir()
    if filepaths:
        for filepath in filepaths:
            operation = NcOperation(filepath=filepath)
            print(operation.__dict__)


if __name__ == "__main__":
    main()
from parsers.pprint_parser import parse_pprint

# from constants import
from file_operations import (read_ncl_file_format_and_create_temp_file,
                             create_files_for_ustanov,
                             create_files_for_operations_in_ustanov,
                             loop_through_all_subprograms_parsing_range_cl_lines,
                             remove_temp_file,
                             get_all_ncl_files_in_dir,
                             )


def main():
    filenames = get_all_ncl_files_in_dir()
    for filename in filenames:
        try:
            cl_lines = read_ncl_file_format_and_create_temp_file(filepath=filename)
            pprint_vars = parse_pprint(lines=cl_lines)
            create_files_for_ustanov(pprint_vars=pprint_vars)
            create_files_for_operations_in_ustanov(pprint_vars=pprint_vars)
            loop_through_all_subprograms_parsing_range_cl_lines(cl_lines=cl_lines, pprint_vars=pprint_vars)
            remove_temp_file()
        except FileNotFoundError:
            print(f"FileNotFoundError {filename}")


if __name__ == "__main__":
    main()

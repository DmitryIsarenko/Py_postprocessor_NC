PROGRAMMER_NAME = "DEFAULT PROGRAMMER"

POST_NAME = "PY POST V1.01"
PROGRAM_MAIN_LETTER = "O"
PROGRAM_MAIN_DIGIT = "7"


# debug
DEBUG = False
# DEBUG = False
DEBUG_CWD = r"c:\WORK_DIRECTORY\10_Programming\Projects\py_post"
DELETE_TEMP_FILE = True
STARTS_FROM_EXE = False

# tolerances
NDIGITS_XYZ = 3
NDIGITS_ABC = 2
NDIGITS_FEEDRATE_G94 = 2
NDIGITS_FEEDRATE_G95 = 3
NDIGITS_CALC_XYZ = 7
NDIGITS_CALC_ABC = 6
NDIGITS_CALC_FEEDRATE_G94 = 4
NDIGITS_CALC_FEEDRATE_G95 = 4
# NDIGITS_FEEDRATE_G95 = 2

# misc
POST_OBJ = None
abs_path_to_selected_file = None


# key_filename_part_1 = "ust"  # will be searched for matches in dir
CL_DATA_FILE_EXTENSION = ".ncl"  # will be searched for matches in dir

G_CODE_FILE_EXTENSION = ""
TEMP_FILE_NAME_PREFIX = "temp"

NC_START_KEYWORD = "PPRINT / NC SEQUENCE NAME :"
NC_END_KEYWORD = "$$-> END /"

# options
LINE_ENDING_EOB = ";"
SAFETY_LINE_DEFAULT = "G17 G40 G49 G90 G94"
NC_SEQUENCE_TAIL_LINES = ["M01", "M99", ""]
G41_G42_SIDE_IS_REVERSED_SWITCH = True

# g-code params for editing:
G_CODE_TOOL_POT_PARAMS_ENABLED = False
G_CODE_SPINDLE_PARAMS_ENABLED = False
G_CODE_FEED_PARAMS_ENABLED = False

G_CODE_TOOL_RPM_PARAMETER = "#101"
G_CODE_TOOL_FEED_PARAMETER = "#102"
G_CODE_TOOL_POT_PARAMETER = "#103"

GATHER_MASSIVE_COPIES_AUTOMATICALLY = False
GATHER_MASSIVE_COPIES_AUTOMATICALLY_VIA_PARAMS = False
PPRINT_FOR_GATHERING_VIA_PARAMS = (
    "PPRINT / # : 1\n"
    "PPRINT / MASSIV : "
)

# # machine configuration
# IS_3AXIS = 1
# IS_4_A_AXIS = 0
# IS_4_B_AXIS = 0
# IS_3_PLUS_2_B_C_AXIS = 0
# IS_5_AXIS = 0
#
# # axis travel
# X_MIN = 0
# X_MAX = 0
# Y_MIN = 0
# Y_MAX = 0
# Z_MIN = 0
# Z_MAX = 0
# A_MIN = 0
# A_MAX = 0
# B_MIN = 0
# B_MAX = 0
# C_MIN = 0
# C_MAX = 0


dict_of_axial_operations_G_codes: dict = {
    "DRILL": "G81",
    "BRKCHP": "G81",
    "DEEP": "G83",
    "FACE": "G81",
    "REAM": "G85",
    "TAP": "G84",
    "BORE": "G86",
}

ust_template_dict = {
    "part_name": "null",
    "date_and_time": "null",
    "ust_name": "null",
    "ust_num_str": "null",
    "ust_O_name": "null",
    "ust_O_name_with_extension": "null",
    "operations": [],
    "cl_file_lines": 0,
    "sum_machining_time": 0,
}

operation_template_dict = {
    "cl_line_index_start": "null",
    "cl_line_index_end": "null",
    "pprints_index_start": "null",
    "pprints_index_end": "null",
    "operation_name": "null",
    "machining_time": 0,
    "tool_name": "null",
    "program_num_iter": "null",
    "program_num": "null",
    "program_num_str": "null",
    "program_O_name": "null",
    "program_O_name_with_extension": "null",
    "tool_pot_num_str": "null",
    "cut_feed": "null",
    "spindle_speed": "null",
}

sequence_massive_names = [
    "TRAJECTORY MILLING",
    "HOLEMAKING",
    "THREAD MILLING",
    # "",
    # "",
    # "",
    # "",
]

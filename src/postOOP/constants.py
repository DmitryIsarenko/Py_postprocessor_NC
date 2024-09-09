
PROGRAMMER_NAME = "DEFAULT PROGRAMMER"

#
# PPRINTS_IN_MAIN_BLOCK = 16
# PPRINTS_IN_SUB_BLOCK = 25


POST_NAME = "PY POST V0.01"
PROGRAM_PREFIX = "O"
PROGRAM_MAIN_DIGIT = "5"


# PATH_TO_NCL = "ust__1_.ncl.1"
key_filename_part_1 = "ust"  # will be searched for matches in dir
key_filename_part_2 = "ncl"  # will be searched for matches in dir


G_CODE_FILE_EXTENSION = ""
TEMP_FILE_NAME = "temp.txt"


# options
SAFETY_LINE_DEFAULT = "G17 G40 G49 G90 G94"
G41_G42_SIDE_IS_REVERSED_SWITCH = 1


# Gcode params for editing:
# G_CODE_PARAMS_ENABLED = 0
G_CODE_TOOL_POT_PARAMS_ENABLED = 1
G_CODE_SPINDLE_PARAMS_ENABLED = 1
G_CODE_FEED_PARAMS_ENABLED = 1

G_CODE_TOOL_POT_PARAMETER = "#101"
G_CODE_TOOL_FEED_PARAMETER = "#102"
G_CODE_TOOL_RPM_PARAMETER = "#103"


dict_of_axial_operations_G_codes: dict = {
    "DRILL": "G81",
    "BRKCHP": "G81",
    "DEEP": "G83",
    "FACE": "G81",
    "REAM": "G85",
    "TAP": "G84",
    "BORE": "G86",
}

from ..constants import PROGRAM_PREFIX, PROGRAM_MAIN_DIGIT, G_CODE_FILE_EXTENSION


class GCodeFile:
    extension = G_CODE_FILE_EXTENSION
    prefix = PROGRAM_PREFIX
    main_digit = PROGRAM_MAIN_DIGIT


class UstanovFile(GCodeFile):
    pass


class ProgramFile(GCodeFile):
    pass


class ProgramFile3AxisMill(ProgramFile):
    pass


class ProgramFile4AxisAMill(ProgramFile):
    pass

from src.postOOP.config import (PROGRAM_MAIN_DIGIT,
                                PROGRAM_MAIN_LETTER,
                                G_CODE_FILE_EXTENSION,
                                POST_NAME,
                                PROGRAMMER_NAME,
                                NC_START_KEYWORD,
                                NC_END_KEYWORD,
                                )


from src.postOOP.classes.ncl_file_analyzer import NclFileAnalyzer
from src.postOOP.classes.file_operator import FileOperator


class NcProgram:
    main_digit = PROGRAM_MAIN_DIGIT
    main_letter = PROGRAM_MAIN_LETTER
    file_extension = G_CODE_FILE_EXTENSION
    postprocessor_name = POST_NAME
    line_with_programmer_name = PROGRAMMER_NAME

    cl_list: list[str] = []
    nc_list: list[str] = []
    #
    # def __init__(self, filepath: str):
    #


class NcOperation(NcProgram):
    def __init__(self, filepath: str):
        # super().__init__(filepath=filepath)
        temp_file = FileOperator.create_temp_formatted_ncl_file(filepath=filepath)
        self.cl_list = FileOperator.get_cl_lines_in_range(filepath=temp_file)
        self.line_with_detail_number = NclFileAnalyzer.get_detail_name_in_cl_list(cl_list=self.cl_list)
        self.line_with_date_of_creation = NclFileAnalyzer.get_date_time_in_cl_list(cl_list=self.cl_list)
        self.cl_lines_count = NclFileAnalyzer.count_cl_lines_in_cl_list(cl_list=self.cl_list)

        self.operation_name: str = NclFileAnalyzer.get_operation_name_in_cl_list(cl_list=self.cl_list)
        self.operation_number: str = self.get_operation_num_from_name()
        self.nc_sequences_count: int = NclFileAnalyzer.count_nc_sequences_in_cl_list(cl_list=self.cl_list)
        self.list_of_nc_sequences_names: list[str] = NclFileAnalyzer.get_list_of_nc_sequence_names(cl_list=self.cl_list)
        self.list_of_nc_sequences_objects: list[NcSequence] = self.generate_list_of_nc_sequences()
        self.sum_machining_time = self.get_sum_of_machining_time()


    def get_operation_num_from_name(self) -> str:
        num = ""
        for char in self.operation_name:
            if char.isdigit():
                num += char
        return num

    def generate_list_of_nc_sequences(self) -> list:
        lst_of_objects = []
        for nc_sequence_name in self.list_of_nc_sequences_names:
            lst_of_objects.append(NcSequence(nc_sequence_name=nc_sequence_name))
        return lst_of_objects

    def get_sum_of_machining_time(self) -> float:
        sum_time = 0
        for nc_obj in self.list_of_nc_sequences_objects:
            sum_time += nc_obj.machining_time
        return sum_time


class NcSequence(NcProgram):
    nc_start_keyword = NC_START_KEYWORD
    nc_end_keyword = NC_END_KEYWORD

    def __init__(self, nc_sequence_name: str):
        self.nc_sequence_name = nc_sequence_name
        self.cl_start_index = NclFileAnalyzer.get_index_of_occurence_in_cl_list_in_range(cl_list=self.cl_list,
                                                                                         search_for=self.nc_sequence_name,
                                                                                         start_index=0, end_index=-1)
        self.cl_end_index = NclFileAnalyzer.get_index_of_occurence_in_cl_list_in_range(cl_list=self.cl_list,
                                                                                       search_for=self.nc_end_keyword,
                                                                                       start_index=self.cl_start_index,
                                                                                       end_index=-1)
        self.machining_time = NclFileAnalyzer.get_machining_time_in_cl_list(
            cl_list=self.cl_list[self.cl_start_index:self.cl_end_index])


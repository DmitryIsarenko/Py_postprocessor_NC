from src.postOOP import config
import logging

logger = logging.getLogger(__name__)

""" pass into inheritance class

def set_nc_sequences_objects_in_list(self):
    MixinOper4Axis(self).set_nc_sequences_objects_in_list()

def start_postprocessing(self):
    MixinOper4Axis(self).start_postprocessing()
    
"""



class MixinOper4Axis:
    def __init__(self, nc_oper_obj_for_4axis, **kwargs):
        self.nc_oper_obj = nc_oper_obj_for_4axis
        super().__init__(**kwargs)


    def set_nc_sequences_objects_in_list(self):
        lst_of_objects = []
        nc_counter = 0
        nc_massive_copy_counter = 0

        for nc_sequence_name in self.nc_oper_obj.list_of_nc_sequences_names:
            nc_counter += 1

            if nc_sequence_name in config.sequence_massive_names:
                nc_sequence_parent_name_of_massive = lst_of_objects[-1].nc_sequence_parent_name_of_massive
                nc_massive_copy_counter += 1

            else:
                nc_sequence_parent_name_of_massive = nc_sequence_name
                nc_massive_copy_counter = 0
            logger.debug(f"nc_sequence_name={nc_sequence_name}")
            logger.debug(f"nc_sequence_parent_name_of_massive={nc_sequence_parent_name_of_massive}")
            lst_of_objects.append(
                self.nc_oper_obj.nc_sequence_class(ncl_parser_class=self.nc_oper_obj.ncl_parser_class,
                                       pprint_parser_class=self.nc_oper_obj.pprint_parser_class,
                                       file_operator_class=self.nc_oper_obj.file_operator_class,
                                       detail_name=self.nc_oper_obj.detail_name,
                                       nc_sequence_name=nc_sequence_name,
                                       nc_sequence_parent_name_of_massive=nc_sequence_parent_name_of_massive,
                                       nc_massive_copy_counter=nc_massive_copy_counter,
                                       cl_list=self.nc_oper_obj.cl_list,
                                       nc_sequence_number=nc_counter,
                                       nc_sequences_count=self.nc_oper_obj.nc_sequences_count,
                                       nc_operation_number=self.nc_oper_obj.operation_number,
                                       date_of_creation=self.nc_oper_obj.date_of_creation,
                                       is_multax_operation=self.nc_oper_obj.is_multax_operation,
                                       ))
        self.nc_oper_obj.list_of_nc_sequences_objects = lst_of_objects

    def start_postprocessing(self):
        temp_filepath = self.nc_oper_obj.file_operator_class.create_temp_formatted_ncl_file()
        self.nc_oper_obj.cl_list = self.nc_oper_obj.file_operator_class.get_all_cl_lines(filepath=temp_filepath)

        if self.nc_oper_obj.cl_list:
            self.nc_oper_obj.set_cl_lines_count()
            self.nc_oper_obj.set_detail_name()
            self.nc_oper_obj.set_date_of_creation()
            self.nc_oper_obj.set_operation_name()
            self.nc_oper_obj.set_operation_num_from_name()
            self.nc_oper_obj.set_nc_filename()

            self.nc_oper_obj.is_multax_operation = self.nc_oper_obj.pprint_parser_class.get_is_oper_multax_in_cl_list(cl_list=self.nc_oper_obj.cl_list)
            if self.nc_oper_obj.is_multax_operation:
                self.nc_oper_obj.multax_line_index = self.nc_oper_obj.pprint_parser_class.get_index_of_occurence_in_cl_list_in_range(
                    cl_list=self.nc_oper_obj.cl_list,
                    search_for="MULTAX / ON",
                    end_index=self.nc_oper_obj.cl_lines_count)
            else:
                self.nc_oper_obj.multax_line_index = None

            logger.info(f"Operation is Multax = {self.nc_oper_obj.is_multax_operation}")

            self.nc_oper_obj.set_nc_sequences_count()
            self.nc_oper_obj.set_nc_sequences_names_in_list()
            self.nc_oper_obj.set_nc_sequences_objects_in_list()
            self.nc_oper_obj.set_sum_machining_time()


            self.nc_oper_obj.nc_list = self.nc_oper_obj.generate_nc_list()

            self.nc_oper_obj.file_operator_class.create_file(
                filepath=f"{config.abs_path_to_selected_file}/../{self.nc_oper_obj.nc_filename_with_extension}")
            self.nc_oper_obj.file_operator_class.append_lines_to_file(
                filepath=f"{config.abs_path_to_selected_file}/../{self.nc_oper_obj.nc_filename_with_extension}",
                list_with_lines=self.nc_oper_obj.nc_list)


        else:
            logger.info(f"Empty self.nc_oper_obj.cl_list for {self.nc_oper_obj.filepath}")

        if config.DELETE_TEMP_FILE:
            self.nc_oper_obj.file_operator_class.remove_file(filepath=temp_filepath)
        else:
            pass
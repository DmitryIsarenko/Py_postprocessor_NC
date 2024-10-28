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
        self.o = nc_oper_obj_for_4axis
        super().__init__(**kwargs)


    def set_nc_sequences_objects_in_list(self):
        lst_of_objects = []
        nc_counter = 0
        nc_massive_copy_counter = 0

        for nc_sequence_name in self.o.list_of_nc_sequences_names:
            nc_counter += 1

            if nc_sequence_name in config.sequence_massive_names and nc_counter > 1:
                nc_sequence_parent_name_of_massive = lst_of_objects[-1].nc_sequence_parent_name_of_massive
                nc_massive_copy_counter += 1

            else:
                nc_sequence_parent_name_of_massive = nc_sequence_name
                nc_massive_copy_counter = 0
            # logger.debug(f"nc_sequence_name={nc_sequence_name}")
            # logger.debug(f"nc_sequence_parent_name_of_massive={nc_sequence_parent_name_of_massive}")
            lst_of_objects.append(
                self.o.nc_sequence_class(ncl_parser_class=self.o.ncl_parser_class,
                                         pprint_parser_class=self.o.pprint_parser_class,
                                         file_operator_class=self.o.file_operator_class,
                                         detail_name=self.o.detail_name,
                                         nc_sequence_name=nc_sequence_name,
                                         nc_sequence_parent_name_of_massive=nc_sequence_parent_name_of_massive,
                                         nc_massive_copy_counter=nc_massive_copy_counter,
                                         cl_list=self.o.cl_list,
                                         nc_sequence_number=nc_counter,
                                         nc_sequences_count=self.o.nc_sequences_count,
                                         nc_operation_number=self.o.operation_number,
                                         date_of_creation=self.o.date_of_creation,
                                         is_multax_operation=self.o.is_multax_operation,
                                         ))
        self.o.list_of_nc_sequences_objects = lst_of_objects

    def start_postprocessing(self):
        temp_filepath = self.o.file_operator_class.create_temp_formatted_ncl_file()
        self.o.cl_list = self.o.file_operator_class.get_all_cl_lines(filepath=temp_filepath)

        if self.o.cl_list:
            self.o.set_cl_lines_count()
            self.o.set_detail_name()
            self.o.set_date_of_creation()
            self.o.set_operation_name()
            self.o.set_operation_num_from_name()
            self.o.set_nc_filename()

            self.o.is_multax_operation = self.o.pprint_parser_class.get_is_oper_multax_in_cl_list(cl_list=self.o.cl_list)
            if self.o.is_multax_operation:
                self.o.multax_line_index = self.o.pprint_parser_class.get_index_of_occurence_in_cl_list_in_range(
                    cl_list=self.o.cl_list,
                    search_for="MULTAX / ON",
                    end_index=self.o.cl_lines_count)
            else:
                self.o.multax_line_index = None

            logger.info(f"Operation is Multax = {self.o.is_multax_operation}")

            self.o.set_nc_sequences_names_in_list()
            self.o.set_nc_sequences_objects_in_list()
            self.o.set_nc_sequences_count()
            self.o.set_sum_machining_time()

            for seq in self.o.list_of_nc_sequences_objects:
                seq.generate_nc_seq_head_body_tail_lists()

            for seq in self.o.list_of_nc_sequences_objects:
                seq.combine_nc_seq_head_body_tail_lines_in_one_list()

            for seq in self.o.list_of_nc_sequences_objects:
                seq.create_seq_file()

            for seq in self.o.list_of_nc_sequences_objects:
                seq.fill_seq_file()


            self.o.generate_nc_oper_head_body_tail_lists()
            self.o.nc_list = self.o.combine_nc_oper_head_body_tail_lines_in_one_list()

            self.o.create_oper_file()
            self.o.fill_oper_file()

        else:
            logger.warning(f"Empty self.cl_list for {config.abs_path_to_selected_file}")

        if config.DELETE_TEMP_FILE:
            self.o.file_operator_class.remove_file(filepath=temp_filepath)
        else:
            pass
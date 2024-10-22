from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_root import MixinRoot
from src.postOOP import config
import logging

logger = logging.getLogger(__name__)


class MixinOperArrays(MixinRoot):
    def __init__(self,
                 nc_oper_obj_for_arrays,
                 **kwargs, ):
        self.o = nc_oper_obj_for_arrays
        super().__init__(**kwargs)

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

            self.o.set_nc_sequences_names_in_list()
            self.o.set_nc_sequences_objects_in_list()
            self.o.set_sum_machining_time()

            for seq_ind, seq in enumerate(self.o.list_of_nc_sequences_objects):
                if seq.is_array:
                    if seq.is_copy:  # is a copy of array
                        seq.is_file_needed = False
                        seq.nc_sequence_number = self.o.list_of_nc_sequences_objects[seq_ind - 1].nc_sequence_number
                        seq.set_nc_filename()
                        self.show_if_seq_info(seq_ind=seq_ind)
                    else:  # not a copy, a head array seq
                        array_copies = seq.array_copies_amount
                        self.set_file_is_copy_for_copies(seq_ind=seq_ind, copies_amount=array_copies)
                        if seq_ind != 0:
                            seq.nc_sequence_number = self.o.list_of_nc_sequences_objects[seq_ind - 1].nc_sequence_number + 1
                        else:
                            seq.nc_sequence_number = 1
                        seq.set_nc_filename()
                        self.show_if_seq_info(seq_ind=seq_ind)
                else:  # not an array seq
                    seq.is_file_needed = True
                    seq.is_copy = False
                    if seq_ind != 0:
                        seq.nc_sequence_number = self.o.list_of_nc_sequences_objects[seq_ind - 1].nc_sequence_number + 1
                    else:
                        seq.nc_sequence_number = 1
                    seq.set_nc_filename()
                    self.show_if_seq_info(seq_ind=seq_ind)

            self.o.set_nc_sequences_count()

            for seq_ind, seq in enumerate(self.o.list_of_nc_sequences_objects):
                pass

            for seq in self.o.list_of_nc_sequences_objects:
                seq.fill_nc_list()

            for seq in self.o.list_of_nc_sequences_objects:
                seq.create_file()

            for seq in self.o.list_of_nc_sequences_objects:
                seq.fill_file()

            # self.o.show()
            self.o.oper_nc_head_lines = self.o.generate_nc_head_lines()
            self.o.oper_nc_body_lines = self.o.generate_nc_body_lines()
            self.o.oper_nc_tail_lines = self.o.generate_nc_tail_lines()
            self.o.nc_list = self.o.generate_nc_list()
            # print(self.o.nc_list)

            self.o.file_operator_class.create_file(
                filepath=f"{config.abs_path_to_selected_file}/../{self.o.nc_filename_with_extension}")
            self.o.file_operator_class.append_lines_to_file(
                filepath=f"{config.abs_path_to_selected_file}/../{self.o.nc_filename_with_extension}",
                list_with_lines=self.o.nc_list)
        else:
            logger.warning(f"Empty self.o.cl_list for {config.abs_path_to_selected_file}")

        if config.DELETE_TEMP_FILE:
            self.o.file_operator_class.remove_file(filepath=temp_filepath)
        else:
            pass

    def set_file_is_copy_for_copies(self, seq_ind: int, copies_amount: int):
        list_of_seq_obj = [obj for obj in self.o.list_of_nc_sequences_objects[seq_ind + 1: seq_ind + copies_amount]]

        for ind, seq in enumerate(list_of_seq_obj):
            seq.is_copy = True

    def set_new_seq_num_for_copies(self, seq_ind: int, copies_amount: int):
        # list_of_seq_obj = [obj for obj in self.o.list_of_nc_sequences_objects[seq_ind + 1: seq_ind + copies_amount]]

        list_of_seq_obj = self.o.list_of_nc_sequences_objects

        new_seq_num = list_of_seq_obj[seq_ind].nc_sequence_number
        for ind, seq in enumerate(list_of_seq_obj):
            if seq_ind <= ind < (seq_ind + copies_amount):
                seq.nc_sequence_number = new_seq_num
                seq.set_nc_filename()
            elif ind >= (seq_ind + copies_amount):
                new_seq_num += 1
                seq.nc_sequence_number = new_seq_num
                seq.set_nc_filename()

    def set_file_is_not_needed_for_copies(self, seq_ind: int, copies_amount: int):
        list_of_seq_obj = [obj for obj in self.o.list_of_nc_sequences_objects[seq_ind + 1: seq_ind + copies_amount]]
        for ind, seq in enumerate(list_of_seq_obj):
            seq.is_file_needed = False

    def show_if_seq_info(self, seq_ind: int):
        logger.debug(
            f"\t{self.o.list_of_nc_sequences_objects[seq_ind].nc_sequence_name}")
        logger.debug(
            f"\t\tis copy {self.o.list_of_nc_sequences_objects[seq_ind].is_copy}")
        logger.debug(
            f"\t\tnum is {self.o.list_of_nc_sequences_objects[seq_ind].nc_sequence_number}")
        logger.debug(
            f"\t\tis file needed {self.o.list_of_nc_sequences_objects[seq_ind].is_file_needed}")


    # def generate_nc_body_lines(self) -> list:
    #     nc_lines = []
    #     for seq_obj in self.o.list_of_nc_sequences_objects:
    #         if seq_obj.is_file_needed:
    #             if seq_obj.is_m00_before_needed is True:
    #                 nc_lines.append("M00")
    #             nc_lines.extend([
    #                 f"M98P{seq_obj.nc_file_number}"
    #                 f"(OPER {seq_obj.nc_sequence_number}/{seq_obj.nc_sequences_count}: {seq_obj.nc_sequence_name})",
    #                 f"(POT: {seq_obj.tool_pot}, TOOL: {seq_obj.tool_name})",
    #             ])
    #             if seq_obj.is_m00_after_needed is True:
    #                 nc_lines.append("M00")
    #         nc_lines.append(f"")
    #     return nc_lines
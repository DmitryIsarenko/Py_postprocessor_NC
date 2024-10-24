from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_root import MixinRoot
from src.postOOP import config
import logging

logger = logging.getLogger(__name__)


class MixinOperArrays3Axis(MixinRoot):
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
                            seq.nc_sequence_number = self.o.list_of_nc_sequences_objects[
                                                         seq_ind - 1].nc_sequence_number + 1
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

            for seq in self.o.list_of_nc_sequences_objects:
                seq.generate_nc_seq_head_body_tail_lists()

            for seq_ind, seq in enumerate(self.o.list_of_nc_sequences_objects):
                if seq.is_array and seq.is_copy is False:
                    combined_body_nc_lines = []
                    combined_body_nc_lines.extend(seq.nc_seq_body_lines)
                    i_start = seq_ind + 1
                    i_end = seq_ind + seq.array_copies_amount
                    for seq_arr_copy in self.o.list_of_nc_sequences_objects[i_start:i_end]:
                        combined_body_nc_lines.extend(seq_arr_copy.nc_seq_body_lines)

                    seq.nc_seq_body_lines = combined_body_nc_lines

            self.clear_copy_extra_gcodes()

            for seq in self.o.list_of_nc_sequences_objects:
                seq.combine_nc_seq_head_body_tail_lines_in_one_list()

            for seq in self.o.list_of_nc_sequences_objects:
                seq.create_seq_file()

            for seq in self.o.list_of_nc_sequences_objects:
                logger.debug(f"HEAD")
                logger.debug(f"{seq.nc_seq_head_lines}")
                logger.debug(f"BODY")
                logger.debug(f"{seq.nc_seq_body_lines}")
                logger.debug(f"TAIL")
                logger.debug(f"{seq.nc_seq_tail_lines}")
                pass

            for seq in self.o.list_of_nc_sequences_objects:
                seq.fill_seq_file()

            self.o.nc_list = self.o.combine_nc_oper_head_body_tail_lines_in_one_list()
            self.o.generate_nc_oper_head_body_tail_lists()

            self.o.create_oper_file()
            self.o.fill_oper_file()

        else:
            logger.warning(f"Empty self.cl_list for {config.abs_path_to_selected_file}")

        if config.DELETE_TEMP_FILE:
            self.o.file_operator_class.remove_file(filepath=temp_filepath)
        else:
            pass

    def create_oper_file(self):
        self.o.file_operator_class.create_file(
            filepath=f"{config.abs_path_to_selected_file}/../{self.o.nc_filename_with_extension}")

    def fill_oper_file(self):
        self.o.file_operator_class.append_lines_to_file(
            filepath=f"{config.abs_path_to_selected_file}/../{self.o.nc_filename_with_extension}",
            list_with_lines=self.o.nc_list)

    def set_file_is_copy_for_copies(self, seq_ind: int, copies_amount: int):
        list_of_seq_obj = [obj for obj in self.o.list_of_nc_sequences_objects[seq_ind + 1: seq_ind + copies_amount]]

        for ind, seq in enumerate(list_of_seq_obj):
            seq.is_copy = True

    def set_new_seq_num_for_copies(self, seq_ind: int, copies_amount: int):
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

    def clear_copy_extra_gcodes(self):
        # deleting g-codes from 2nd copy to the end
        for seq in self.o.list_of_nc_sequences_objects:
            extra_gcodes_del_all_exept_start = [f"G{seq.work_offset}", f"T{seq.tool_pot}",
                                                f"{config.G_CODE_TOOL_POT_PARAMETER}=",
                                                f"{config.G_CODE_TOOL_RPM_PARAMETER}=",
                                                f"{config.G_CODE_TOOL_FEED_PARAMETER}=",
                                                "M03", "M04", "M3", "M4", "M6", "M06", "M08", "M8"]
            if seq.is_file_needed and seq.is_array:
                for gcode in extra_gcodes_del_all_exept_start:
                    copy_counter = 0
                    for ind_line, line in enumerate(seq.nc_seq_body_lines):
                        if gcode in line and copy_counter < seq.array_copies_amount:
                            if copy_counter >= 1:
                                logger.debug(f"Clearing from 2nd copy to the end")
                                # seq.nc_seq_body_lines[ind_line] = "   wo m6 s"
                                seq.nc_seq_body_lines[ind_line] = ""
                            copy_counter += 1

        # deleting g-codes from 1st copy to the last one. Leaving last copy g-codes
        extra_gcodes_del_all_exept_end = ["M05", "M5", "M09", "M9"]
        for seq in self.o.list_of_nc_sequences_objects:
            if seq.is_file_needed and seq.is_array:
                for gcode in extra_gcodes_del_all_exept_end:
                    copy_counter = 1
                    for ind_line, line in enumerate(seq.nc_seq_body_lines):
                        if gcode in line and copy_counter < seq.array_copies_amount:
                            logger.debug(f"Clearing from 1st copy to the last one")
                            copy_counter += 1
                            # seq.nc_seq_body_lines[ind_line] = " m5 m9"
                            seq.nc_seq_body_lines[ind_line] = ""
            # for i, line in enumerate(seq.nc_seq_body_lines):
            while "" in seq.nc_seq_body_lines:
                seq.nc_seq_body_lines.remove("")

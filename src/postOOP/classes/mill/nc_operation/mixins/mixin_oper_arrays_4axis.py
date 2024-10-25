from src.postOOP import config
from src.postOOP.classes.mill.nc_operation.mixins.mixin_oper_arrays_3axis import \
    MixinOperArrays3Axis
from src.postOOP.classes.mill.nc_operation.mixins.mixin_root import MixinRoot
import logging

logger = logging.getLogger(__name__)


class MixinOperArrays4Axis(MixinOperArrays3Axis, MixinRoot):
    def __init__(self,
                 nc_oper_obj_for_arrays,
                 **kwargs, ):
        self.o = nc_oper_obj_for_arrays
        super().__init__(
            nc_oper_obj_for_arrays=self.o,
            **kwargs)

    def check_multax(self):
        # logger.debug("check_multax from 4 axis")
        self.o.is_multax_operation = self.o.pprint_parser_class.get_is_oper_multax_in_cl_list(
            cl_list=self.o.cl_list)
        if self.o.is_multax_operation:
            self.o.multax_line_index = self.o.pprint_parser_class.get_index_of_occurence_in_cl_list_in_range(
                cl_list=self.o.cl_list,
                search_for="MULTAX / ON",
                end_index=self.o.cl_lines_count)
        else:
            self.o.multax_line_index = None

    def gather_param_array(self, sequence_obj, sequence_index):

        rot_adr, sequence_obj.start_angle_of_param_array = self.get_first_rot_adr_and_angle_coord_for_param_array(
            sequence_obj=sequence_obj)

        logger.debug(f"\t\t\t\t{sequence_obj.start_angle_of_param_array}")

        sequence_obj.delta_angle_of_param_array = self.get_delta_angle_of_param_array(sequence_obj=sequence_obj,
                                                                                      seq_ind=sequence_index)

        param_pre_lines = [
            f"#1={sequence_obj.start_angle_of_param_array}(NACH_UGOL)",
            f"#2={sequence_obj.delta_angle_of_param_array}(SHAG_UGLA)",
            f"#3={sequence_obj.array_copies_amount}(KOLICHESTVO)",
        ]

        param_while_lines = [
            "WHILE[#3 GT 0]DO1",
            "M11",
            f"G00 G90 {rot_adr}#1",
            "M10",
        ]

        param_end_lines = [
            "#1=#1+#2",
            "#3=#3-1",
            "IF[#1 GT 360]GOTO1",
            "GOTO2",
            "N1",
            "#1=#1-360",
            "N2",
            "END1",
        ]

        index_for_insert_param_pre_lines = 0
        index_for_insert_param_while_lines = 3 + len(param_pre_lines)
        index_for_insert_param_end_lines = -2

        for line in param_pre_lines:
            sequence_obj.nc_seq_body_lines.insert(index_for_insert_param_pre_lines, line)
            index_for_insert_param_pre_lines += 1

        if not self.alter_existing_clamp_and_rotate(sequence_obj=sequence_obj, rot_adr=rot_adr):
            for line in param_while_lines:
                sequence_obj.nc_seq_body_lines.insert(index_for_insert_param_while_lines, line)
                index_for_insert_param_while_lines += 1

        for line in param_end_lines:
            sequence_obj.nc_seq_body_lines.insert(index_for_insert_param_end_lines, line)
            # index_for_insert_param_end_lines += 1

    def get_first_rot_adr_and_angle_coord_for_param_array(self, sequence_obj) -> tuple[str, str]:
        rotating_axis_adresses = ["A", "B", ]
        for rot_adr in rotating_axis_adresses:
            line_ind_with_rot_adr = self.get_line_with_axis_adr(list_nc_lines=sequence_obj.nc_seq_body_lines,
                                                                adr=rot_adr)
            if line_ind_with_rot_adr:
                angle_str: str = self.get_angle_after_axis_adr(line=line_ind_with_rot_adr, adr=rot_adr)
                return rot_adr, angle_str
            else:
                return "A", "0"

    @staticmethod
    def get_line_with_axis_adr(list_nc_lines: list[str], adr: str) -> str | None:
        for i, line in enumerate(list_nc_lines):
            if adr in line:
                return line
        else:
            return None

    @staticmethod
    def get_angle_after_axis_adr(line: str, adr: str) -> str:
        list_of_codes = line.split(sep=" ")
        code_with_adr = [code for code in list_of_codes if adr in code][0]
        angle_str = code_with_adr.replace(adr, "")
        return angle_str

    def get_delta_angle_of_param_array(self, sequence_obj, seq_ind: int):
        two_seq = [
            self.o.list_of_nc_sequences_objects[seq_ind],
            self.o.list_of_nc_sequences_objects[seq_ind + 1],
        ]
        first_angle = self.get_first_rot_adr_and_angle_coord_for_param_array(sequence_obj=two_seq[0])[1]
        second_angle = self.get_first_rot_adr_and_angle_coord_for_param_array(sequence_obj=two_seq[1])[1]

        delta_angle = float(second_angle) - float(first_angle)
        if delta_angle > 180:
            delta_angle = delta_angle - 360
        return str(round(delta_angle, ndigits=config.NDIGITS_ABC))

    @staticmethod
    def alter_existing_clamp_and_rotate(sequence_obj, rot_adr: str):
        for ind_line, line in enumerate(sequence_obj.nc_seq_body_lines):
            if "M11" in line:
                sequence_obj.nc_seq_body_lines.insert(ind_line, f"WHILE[#3 GT 0]DO1")
                sequence_obj.nc_seq_body_lines.pop(ind_line + 2)
                sequence_obj.nc_seq_body_lines.insert(ind_line + 2, f"G00 G90 {rot_adr}#1")

                return True
        return False

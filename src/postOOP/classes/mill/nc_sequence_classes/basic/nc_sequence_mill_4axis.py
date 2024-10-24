from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_root import MixinRoot
from src.postOOP.classes.mill.nc_sequence_classes.basic.nc_sequence_mill_3axis import NcSequenceMill3Axis
import logging

logger = logging.getLogger(__name__)


class NcSequenceMill4Axis(NcSequenceMill3Axis, MixinRoot):
    nc_sequence_class_name = "NcSequenceMill4AxisA"
    is_multax_active = False
    is_multax_operation = False


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

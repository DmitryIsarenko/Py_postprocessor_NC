from src.postOOP import config
import logging

logger = logging.getLogger(__name__)

def execute_postprocess(post_obj) -> bool:
    if post_obj is None:
        logger.warning("Selected post is None")
        return False
    else:
        operations = list()

        filepath = config.abs_path_to_selected_file
        if filepath:
            operations.append(post_obj())
            for operation in operations:
                operation.start_postprocessing()
            return True
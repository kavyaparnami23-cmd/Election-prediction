"""
Author : Kavya Parnami
Project : ElectionPulse AI
Description : Custom Exception Handling
"""

import sys
from src.logger import logger


class ElectionException(Exception):
    """
    Custom Exception Class
    """

    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)

        self.error_message = self.get_detailed_error_message(
            error_message,
            error_details
        )

    @staticmethod
    def get_detailed_error_message(error_message, error_details: sys):

        _, _, exc_tb = error_details.exc_info()

        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        message = (
            f"\nError occurred in script : {file_name}"
            f"\nLine Number              : {line_number}"
            f"\nError Message            : {error_message}"
        )

        return message

    def __str__(self):
        return self.error_message


# ======================================================
# Testing
# ======================================================

if __name__ == "__main__":

    try:
        a = 10
        b = 0

        result = a / b

    except Exception as e:

        custom_exception = ElectionException(e, sys)

        logger.error(custom_exception)

        print("=" * 60)
        print("Custom Exception Working Successfully")
        print(custom_exception)
        print("=" * 60)
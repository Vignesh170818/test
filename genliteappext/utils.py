'''Utility functions for genliteappext'''
import logging

logger=logging.getLogger("GenLiteApp")

def validate_length(*args):
    '''Validate Length'''
    for string in args:
        if not isinstance(string, str):
            logger.error("The input '%s' is not a string.", string)
            return False
        char_count = len(string)
        if char_count > 40000:
            logger.error("The string '%s' contains %s characters.", string, char_count)
            return False
    return True

import logging


def log_extract_spl_list(log):
    pass


def spl_list_valid_tool(except_spl_list, extract_spl_list):
    if except_spl_list == except_spl_list:
        assert True
    else:
        msg_a = "Spl list not match"
        logging.log(logging.ERROR, msg=msg_a)
        msg = "Except spl list : " + except_spl_list
        logging.log(logging.ERROR, msg=msg)
        msg = "Extract spl list : " + extract_spl_list
        logging.log(logging.ERROR, msg=msg)
        raise AssertionError(msg_a)

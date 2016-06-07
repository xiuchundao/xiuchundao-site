# coding: utf-8


class ResultModel(object):
    SUCCESS_CODE = 1
    SUCCESS_MSG = '成功'
    FAILED_CODE = 0
    FAILED_MSG = '失败'

    def __init__(self, code, message, items):
        self.code = code
        self.message = message
        self.items = items

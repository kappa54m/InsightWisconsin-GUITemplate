import os
from typing import Optional, Set, List

import model
from model import ModelError, ProjectData


class DataChangeHandler:
    def on_project_loaded(self, old_project_data: Optional[ProjectData], new_project_data: Optional[ProjectData]):
        pass

    def get_originator(self):
        return self


class __ModelCallbacksImpl(model.ModelCallbacksInterface):
    def __init__(self):
        self.dc_handlers: List[DataChangeHandler] = []

    def register_data_change_handler(self, dch: DataChangeHandler):
        self.dc_handlers.append(dch)

    def on_project_loaded(self, *a):
        self.__call_model_cbs(DataChangeHandler.on_project_loaded, *a)

    def __call_model_cbs(self, method, originator, *args):
        for icb, dc in enumerate(self.dc_handlers):
            if dc.get_originator() != originator:
                getattr(dc, method.__name__)(*args)


MODEL: Optional[model.Model] = None
model_cbs = __ModelCallbacksImpl()
last_err_msg = ''


def init_model(**kw):
    global MODEL
    if MODEL is not None:
        raise ValueError("Model has already been initialized.")
    MODEL = model.Model(model_cbs)


def register_data_change_handler(handler: DataChangeHandler):
    model_cbs.register_data_change_handler(handler)


def _set_err(e, ret=None, append=False):
    lg.exception("Model Exception (%s)", e)
    global last_err_msg
    if not append:
        last_err_msg = str(e)
    else:
        last_err_msg = "{}\n{}".format(last_err_msg, e)
    return ret


def load_project(project_fp, originator=None):
    try:
        MODEL.load_project(project_fp, originator=originator)
        return True
    except ModelError as e:
        return _set_err(e, ret=False)


def get_last_error():
    return last_err_msg

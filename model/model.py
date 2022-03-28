import os
from typing import Optional
from abc import abstractmethod
import json

#from PIL import Image
from config import lg


class ModelError(Exception):
    """
    For errors that model can recover from that are not always preventable from an outside caller (cf. ValueError).
    """
    pass


#class DBIOError(ModelError):
#    pass


class Model:
    """
    Synchronous model
    """

    def __init__(self, callbacks):
        # Initializations
        self.project_data = ProjectData()
        
        #self.__init_db()
        self.callbacks = LoggingModelCallbacks(callbacks)

    def load_project(self, project_fp, originator=None):
        old_project_data = self.project_data.clone()
        
        # Project loading code here
        lg.debug("TODO: Load project from data")
        #self.project_data.update(...)

        self.callbacks.on_project_loaded(originator, old_project_data, self.project_data)

    #def __init_db(self):
    #    with self.__connect() as conn:
    #        conn.execute("""
    #            CREATE TABLE IF NOT EXISTS
    #            ...
    #        ) 
    #        """.format(config.get_imagehash_str_len()))
    #        conn.commit()

    #def __connect(self):
    #    db_path = config.get_db_path()
    #    try:
    #        return sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    #    except Exception as e:
    #        raise DBIOError("Failed to connect to database {}".format(db_path)) from e

    #@staticmethod
    #def __list_to_csv(lst):
    #    return list_to_csv(lst, strip=True, quoting=csv.QUOTE_MINIMAL)

    #@staticmethod
    #def __csv_to_list(s):
    #    return csv_to_list(s)


class ProjectData:
    def __init__(self, time_btw_iter: float=0.0, n_iters: int=0):
        self.time_btw_iter = time_btw_iter
        self.n_iters = n_iters

    def update(self, time_btw_iter: float=0.0, n_iters: int=0):
        self.time_btw_iter = time_btw_iter
        self.n_iters = n_iters

    def clone(self):
        pd = ProjectData()
        pd.update(time_btw_iter=self.time_btw_iter, n_iters=self.n_iters)
        return pd

    @property
    def len_of_experiment(self):
        return self.n_iters * self.time_btw_iter


# TODO clear -> on_project_loaded with empty new_project_data, or separate callback?
class ModelCallbacksInterface:
    @abstractmethod
    def on_project_loaded(self, originator, old_project_data: Optional[ProjectData],
            new_project_data: Optional[ProjectData]):
        pass


class LoggingModelCallbacks(ModelCallbacksInterface):
    def __init__(self, cb: Optional[ModelCallbacksInterface]):
        self.cb_impl: Optional[ModelCallbacksInterface] = cb

    def on_project_loaded(self, originator, old_project_data: Optional[ProjectData],
            new_project_data: Optional[ProjectData]):
        lg.debug("model project loaded by %s - %s -> %s",
                      originator, old_project_data, new_project_data)
        self.cb_impl.on_project_loaded(originator, old_project_data, new_project_data)


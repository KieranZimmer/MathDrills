from abc import ABC, abstractmethod
import importlib


class AbstractDrill(ABC):
    drill_types = ["multi", "frac", "div", "skip", "distrib", "multi_tab", "add_tab"]
    drill_type_name = {"multi": "Multiplication Drill", "frac": "Fraction Addition Drill", "div": "Division Drill",
                       "skip": "Skip Counting Drill", "distrib": "Distributive Property Drill",
                       "multi_tab": "Multiplication Table Drill", "add_tab": "Addition Table Drill"}
    global_params_list = ["rand_seed", "drill_name", "num_drills"]

    #Drill specific parameters
    drill_param_list = []
    drill_param_text = {}
    drill_param_input = {}

    @classmethod
    @abstractmethod
    def build_drill_pdf(cls, params):
        pass

    @classmethod
    @abstractmethod
    def build_drill_tex(cls, params):
        pass

    @classmethod
    def import_drill(cls, drill_type):
        """
        Returns the drill class represented by the drill type name.
        """
        drill_cls_name = cls.drill_type_name[drill_type].replace(" ","")
        return getattr(importlib.import_module(drill_cls_name), drill_cls_name)
from abc import ABC, abstractmethod
import importlib


class AbstractDrill(ABC):
    drill_types = ["multi", "frac", "div", "skip", "distrib", "multi_tab", "add_tab", "frac_simp", "dec_ex"]
    drill_type_name = {"multi": "Multiplication Drill", "frac": "Fraction Addition Drill", "div": "Division Drill",
                       "skip": "Skip Counting Drill", "distrib": "Distributive Property Drill",
                       "multi_tab": "Multiplication Table Drill", "add_tab": "Addition Table Drill",
                       "frac_simp": "Fraction Simplification Drill", "dec_ex": "Decimal Expansion Drill"}
    drill_type_name_reversed = {v: k for k, v in drill_type_name.items()} #invert above dict
    drill_names = list(drill_type_name_reversed.keys()) #list of all drill names
    global_params_list = ["rand_seed", "drill_name", "num_drills"] #input parameters general to all drill types

    #Drill specific parameters
    drill_param_list = []
    drill_param_text = {}
    #0: binary default no, 1: binary default yes, 2: text entry
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
from abc import ABC, abstractmethod


class AbstractDrill(ABC):
    drill_types = ["multi", "frac", "div", "skip"]
    drill_type_name = {"multi": "Multiplication", "frac": "Fraction Addition", "div": "Division",
                       "skip": "Skip Counting"}
    global_params_list = ["rand_seed", "drill_name", "num_drills"]

    @classmethod
    @abstractmethod
    def build_drill_pdf(cls, params):
        pass

    @classmethod
    @abstractmethod
    def build_drill_tex(cls, params):
        pass
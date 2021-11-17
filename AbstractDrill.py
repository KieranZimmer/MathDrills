from abc import ABC, abstractmethod


class AbstractDrill(ABC):
    drill_types = ["multi", "frac", "div", "skip"]
    drill_type_name = {"multi": "Multiplication", "frac": "Fraction Addition", "div": "Division",
                       "skip": "Skip Counting"}

    @abstractmethod
    def build_drill_pdf(self):
        pass

    @abstractmethod
    def build_drill_tex(self):
        pass
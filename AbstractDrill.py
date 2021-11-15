from abc import ABC, abstractmethod


class AbstractDrill(ABC):

    @abstractmethod
    def build_drill_pdf(self):
        pass

    @abstractmethod
    def build_drill_tex(self):
        pass
from delicolour.colour import Colour


class AppModel:
    @staticmethod
    def get_default():
        model = AppModel()
        model.colour = Colour.from_rgb(255, 255, 255)

        return model

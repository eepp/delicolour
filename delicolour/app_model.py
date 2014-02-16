from delicolour.colour import Colour


class AppModel:
    @staticmethod
    def get_default():
        model = AppModel()
        model.colour = Colour.from_rgb(255, 255, 255)
        model.css_hex_copy_hash = True
        model.css_hex_lower = True
        model.fine_incr = 0.01

        return model

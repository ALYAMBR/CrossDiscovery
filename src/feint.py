from src.ui.main_frame import MainFrame


class Feint:
    def __init__(self, data_X, data_y, eval_func) -> None:
        main_frame = MainFrame(data_X, data_y)
        main_frame.show()
        

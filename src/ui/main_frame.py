"""
Compilation of all components together.
"""

import pandas as pd
import panel as pn
import param


class ProcessStorage():
    def __init__(self) -> None:
        self.selected_features = []

class MainFrame():
    def __init__(self, data_X, data_y) -> None:
        self.data_X = data_X
        self.data_y = data_y
        self.process_storage = ProcessStorage()
        self.tmplt = self.init_main_frame()

    def init_main_frame(self):
        tmplt = pn.template.GoldenTemplate(
            title='Feent'
            )
        
        pn_col_feature_selection = self._init_feature_selection()

        tmplt.main.append(
            pn_col_feature_selection
        )

        return tmplt
    
    def _init_feature_selection(self):
        class FeatureSelection(param.Parameterized):
            cross_selection = param.ListSelector(
                default=[],
                objects=self.data_X.columns.tolist())
        
        feature_selection = FeatureSelection()
        selector_param = pn.Param(
            feature_selection.param.cross_selection,
            widgets={
                'cross_selection': pn.widgets.CrossSelector
            }
        )
        text_selected_features = pn.widgets.StaticText(
            value='Selected features: []'
        )
        dataframe_show = pn.widgets.DataFrame(
            pd.concat([self.data_X, self.data_y], axis=1),
            autosize_mode='fit_columns',
            frozen_rows=10,
            width=1200    
        )
        def on_click_feature_selection(event):
            selected_features = feature_selection.param.get_param_values()[0][1]
            self.process_storage.selected_features = selected_features
            text_selected_features.value = f'Selected features: {self.process_storage.selected_features}'
            dataframe_show.value = pd.concat(
                [
                    self.data_X[self.process_storage.selected_features],
                    self.data_y
                ],
                axis=1
            )

        button_select_features = pn.widgets.Button(name='👴🏻 Select Features')
        button_select_features.on_click(on_click_feature_selection)
    
        pn_col = pn.Column(
                selector_param,
                button_select_features,
                text_selected_features,
                dataframe_show,
                name='Feature Selection'
            )
    
        return pn_col
    
    # def _init_

    def show(self):
        self.tmplt.show()
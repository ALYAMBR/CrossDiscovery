"""
Compilation of all components together.
"""

from collections import defaultdict

import pandas as pd
import panel as pn
from panel import param


class MainFrame():
    def __init__(self, data_X, data_y) -> None:
        self.data_X = data_X
        self.data_y = data_y
        self.process_storage = defaultdict(list)
        self.tmplt = None

    def init_main_frame(self):
        if self.tmplt is not None:
            return self.tmplt
        
        tmplt = pn.template.GoldenTemplate(
            title='Feint'
            )
        
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
            value='Selected features: '
        )
        dataframe_show = pn.widgets.DataFrame(
            pd.concat([self.data_X.head(10), self.data_y.head(10)], axis=0),
            autosize_mode='fit_columns',
            frozen_rows=10,
            width=800    
        )
        def on_click_feature_selection(event):
            selected_features = feature_selection.param.get_param_values()[0][1]
            self.process_storage.update({'selected_features': selected_features})
            text_selected_features.value = f'Selected features: {self.process_storage.get('selected_features')}'
            dataframe_show.value = 
"""
Compilation of all components together.
"""

import pandas as pd
import panel as pn
import param
import plotly.graph_objs as go
from plotly import subplots

pn.extension('plotly')


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
        pn_col_settings = self._init_fe_iteration_settings()
        pn_col_visualizations = self._init_build_base_visualizations()
        pn_col_export = self._init_save_page()
        pn_col_history = self._init_history_page()

        pn_cols = [
            pn_col_feature_selection,
            pn_col_settings,
            pn_col_visualizations,
            pn_col_export,
            pn_col_history,
        ]

        [tmplt.main.append(pn_col) for pn_col in pn_cols]

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

    def _init_build_base_visualizations(self):
        # todo для всех числовых построить распределения
        # todo для всех категориальных каунтплоты
        int_subdf = self.data_X.select_dtypes('int')
        cat_df = pd.DataFrame((int_subdf.nunique() < 20), columns=['is_categorical'])
        cat_cols = cat_df[cat_df['is_categorical']].index.tolist()
        int_cols = cat_df[~cat_df['is_categorical']].index.tolist()
        float_cols = self.data_X.select_dtypes('float').columns.tolist()
        obj_cols = self.data_X.select_dtypes('object').columns.tolist()
        
        total_len = (
            len(cat_cols) +
            len(int_cols) +
            len(float_cols) +
            len(obj_cols)
        )

        cat_plots = {}
        for cat_col in cat_cols:
            cat_plot = go.Histogram(x=self.data_X[cat_col])
            cat_plots.update({cat_col: cat_plot})

        int_plots = {}
        for int_col in int_cols:
            int_plot = go.Histogram(x=self.data_X[int_col])
            int_plots.update({int_col: int_plot})
        
        float_plots = {}
        for float_col in float_cols:
            float_plot = go.Histogram(x=self.data_X[float_col])
            float_plots.update({float_col: float_plot})

        obj_plots = {}
        for obj_col in obj_cols:
            obj_plot = go.Histogram(x=self.data_X[obj_col])
            obj_plots.update({obj_col: obj_plot})

        plots = {}
        plots.update(cat_plots)
        plots.update(int_plots)
        plots.update(float_plots)
        plots.update(obj_plots)

        fig_layout = subplots.make_subplots(
            rows = total_len // 4 + 1, cols = 4,
            subplot_titles=list(plots.keys()),
            vertical_spacing=0.03,
            horizontal_spacing=0.03
        )

        row, col = 1, 1
        for k, v in plots.items():
            fig_layout.append_trace(v, row, col)
            col += 1
            if col == 5:
                row += 1
                col = 1

        fig_layout['layout'].update(height=1600, width=1600, title='Original Data Distributions')

        pn_col = pn.Column(
            pn.pane.Plotly(fig_layout),
            name='Visualizations'
        )
        return pn_col

    def _init_fe_iteration_settings(self):
        # todo настройки для конкретной итерации алгоритма
        # выбор операций, какие-то базовые настройки
        # можно продвинутые настройки спрятать под кат
        pn_col = pn.Column(
            name='Settings'
        )

        return pn_col

    def _init_history_page(self):
        # todo страничка с снэпшотами предыдущих итераций
        # в идеале интересно было бы сделать дерево, где можно
        # возвращаться на предыдущие шаги и начинать от какого-то
        # конкретного состояния
        pn_col = pn.Column(
            name='History'
        )

        return pn_col

    def _init_save_page(self):
        # todo страничка, на которой можно сохранить артефакты
        # графики можно и так сохранять
        pn_col = pn.Column(
            name='Export'
        )

        return pn_col
    

    def show(self):
        self.tmplt.show()
from panel import param

class FeatureSelection(param.Parameterized):
    cross_selection = param.ListSelector(default=[], objects=data.columns.tolist())


def get_on_click_feature_selection(feature_selection, process_storage, text_selected_features, dataframe_show, data):
    def on_click_feature_selection(event):
        selected_features = feature_selection.param.get_param_values()[0][1]
        process_storage.selected_features = selected_features
        text_selected_features.value = f'Selected features: {process_storage.selected_features}'
        dataframe_show.value = data[process_storage.selected_features].head(10)
    return on_click_feature_selection
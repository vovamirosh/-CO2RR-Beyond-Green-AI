import pickle
import warnings
from catboost import CatBoostRegressor
import os
warnings.filterwarnings('ignore')




def lgbm_predict(input, cb_with_cat=False):
    dir_name = os.path.split(os.getcwd())[0]
    model = CatBoostRegressor()
    if cb_with_cat:
        path_catboost = f"{dir_name}\CO2RR\Regression\Models\Catboost_cat_C2H4_2024_11_02_opt"
    else:
        path_catboost = f"{dir_name}\CO2RR\Regression\Models\cb_main"
        
    model.load_model(path_catboost)
    # x_input = input.drop(['material'], axis=1)
    y_input_predict = model.predict(input)
    return y_input_predict

if __name__ == "__main__":
    dir_name = os.path.split(os.getcwd())[0]
    path_name = f"{dir_name}\Regression\Models\Catboost_C2H4_2024_10_22"
    print(path_name)

    # learning_rate= 0.07492896323506779, depth= 10, subsample= 0.9326185676855095, colsample_bylevel= 0.6178905559048042, min_data_in_leaf= 61, logging_level = "Silent"

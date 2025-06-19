import os
import pandas as pd


class Encoding():
  def __init__(self,df, product="C2H4") -> None:
    self.product = product
    self.df = df
    # self.col_to_drop = ['FE, %','Unnamed: 0', 'DOI', 'Cu2O-110, %', 'Cu2O-111, %', 'Cu2O-200, %', 'Cu2O-220, %', 'Cu-111, %', 'Cu-200, %', 'Cu-220, %', 'XRD noises', 'Current density, mA/cm2']
    self.__get_scaler()
   
  def __get_scaler(self):
    cat_col = list(self.df.select_dtypes(include="object").columns)
    # scaler = StandardScaler()
    # normalized_df = pd.DataFrame(self.num_encoder.transform(data), columns=data.columns)
    self.new_df =  self.df.drop(cat_col, axis=1)


if __name__ == "__main__":
  dir_name = os.getcwd()
  path_name = f"{dir_name}\\New_datasets\\prepr.csv"
  df = pd.read_csv(path_name)

  df_new = Encoding(df).new_df
  print(len(list(df_new.columns)))


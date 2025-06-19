import os
import pandas as pd
import MV_models
import random
from MV_encoder_transformation import Encoding
import numpy as np

size = 100

dir_name = os.path.split(os.getcwd())[0]
path_name = f"{dir_name}\\CO2RR\\New_datasets\\prepr.csv"
# path_name = "G:\\python_projects\\CO2RR\\New_datasets\\prepr.csv"
df = pd.read_csv(path_name)
X = df.drop(["FE, %", 'DOI'], axis=1)
X = X.loc[X["Product"] == "C2H4"]

unic_morph = ['Morphology (TEM/SEM)', 'width min (nm)', 'width aver (nm)', 'width max (nm)',
'length min (nm)', 'length aver (nm)', 'length max (nm)', 'Av_volume, mkm^3', 'Ratio_sphere_volume', 'Min_volume, mkm^3', 'Max_volume, mkm^3']

morph_comb = X[unic_morph].drop_duplicates()
morph_comb.iloc[np.random.randint(0, len(morph_comb)),:].to_dict()

unic_comp_1 = ['Compound_1', '1_efermi',
       '1_density_atomic', '1_total_magnetization_normalized_formula_units',
       '1_energy_above_hull', '1_energy_per_atom', '1_volume', '1_band_gap']
comp1_comb = X[unic_comp_1].drop_duplicates()

unic_comp_2 = ['Compound_2', '2_efermi',
       '2_density_atomic', '2_total_magnetization_normalized_formula_units',
       '2_energy_above_hull', '2_energy_per_atom', '2_volume', '2_band_gap']

comp2_comb = X[unic_comp_2].drop_duplicates()

base_df = X[['Base', 'Base_carbon paper electrode', 'Base_gasdiffusion electrode']].drop_duplicates()

elecltr_df = X[['electrolyte','anion_molar_conductance',
       'anion_mobility', 'anion_diffusion_coefficient', 'anion_hydr_R_of_ion']].drop_duplicates()

reactor_df = X[['Type of reactor', 'Type of reactor_H-cell']].drop_duplicates()

cu_df = X[['Cu, % (at.)', 'Cu+, % (at.)', 'Cu(2+), % (at.)']].drop_duplicates()

uniq = [] # stores all the unique characters available in the dataset, it helps to make a new population with randomized parameters
for a in range(len(X.columns)):
    uni = pd.unique(X.iloc[:, a])
    uniq.append(uni)

def correlated_types():
    levels = {0: "Type of reactor",
            1: "electrolyte",
            2: "conc, M",
            3: "pH"}
    structure = {"Flow cell": 
                {'KOH': 
                    {1: [14],
                     2: [14],
                     3: [14],
                     0.5: [13]},
                'KHCO3':
                    {1: [8.32],
                    0.1: [6.8]}},
                'H-cell':
                {'KHCO3':
                    {0.5:
                        [6.85, 7.2, 7.8, 8.4],
                    0.1: [6.8],
                    1: [8.32]},
                'KOH': 
                    {2: [14]},
                'KCl': {1: [6.9]}}}

    choices = []
    end = False
    while True:
        temp = structure
        for i in range(len(choices)):
            if isinstance(temp, list):
                temp = temp[choices[i]]
            else:
                temp = temp[list(temp.keys())[choices[i]]]
            if not(isinstance(temp, dict) or isinstance(temp, list)):
                end = True
        if end:
            break
        size = len(temp)
        value = np.random.randint(0, size)
        choices.append(value)

    answer = dict()
    temp = structure
    for i in range(len(choices)):
        level_name = levels[i]
        if isinstance(temp, list):
            choosen_item = temp[choices[i]]
        else:
            choosen_item = list(temp.keys())[choices[i]]
            temp = temp[list(temp.keys())[choices[i]]]
        answer[level_name] = choosen_item

    #Get morphology value
    morph_to_use = morph_comb.iloc[np.random.randint(0, len(morph_comb)),:].to_dict()

    comp1_to_use = comp1_comb.iloc[np.random.randint(0, len(comp1_comb)),:].to_dict()

    comp2_to_use = comp2_comb.iloc[np.random.randint(0, len(comp2_comb)),:].to_dict()

    base_to_use = base_df.iloc[np.random.randint(0, len(base_df)),:].to_dict()

    cu_to_use = cu_df.iloc[np.random.randint(0, len(cu_df)),:].to_dict()

    electr_to_use = elecltr_df[elecltr_df["electrolyte"] == answer["electrolyte"]].iloc[0,1:].to_dict()

    reactor_to_use = reactor_df[reactor_df["Type of reactor"] == answer["Type of reactor"]].iloc[0,1:].to_dict()

    return(answer | morph_to_use | comp1_to_use | comp2_to_use | base_to_use | electr_to_use | reactor_to_use | cu_to_use)    


def individuals():
    indv = []
    cols = X.columns
    corr_col = list(correlated_types().keys())
    k = 0
    corr_generated = correlated_types()
    for col in cols:
        if col not in corr_col:
            uniqas = random.choice(uniq[k])
        else:
            uniqas = corr_generated[col]
        indv.append(uniqas)
        k += 1
    return indv

"""generate population with specific population size"""
#population with specific material descriptors were generated but cell line were still random
def population(size):
    pops = []
    for indv in range(2*size):
        single = individuals()
        pops.append(single)
    new_one = pd.DataFrame(data=pops, columns=X.columns)
    new_one["Time, h"].values[:] = 1
    new = new_one.head(size)
    return new

def fitness(df):
    gen_encoded = Encoding(df).new_df
    gen_viability = MV_models.lgbm_predict(gen_encoded)
    copy3 = gen_encoded.assign(FE = gen_viability)
    copy3 = copy3.sort_values('FE', ascending=False)
    return copy3

Generation1 = fitness(population(size)).sort_values('FE', ascending=False)

Generation1.head()

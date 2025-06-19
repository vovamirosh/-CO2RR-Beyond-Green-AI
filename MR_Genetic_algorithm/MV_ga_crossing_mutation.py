import os
import MV_ga_compd_generation
import random
import pandas as pd
import itertools
from MV_encoder_transformation import Encoding

indv2_list = MV_ga_compd_generation.fitness(MV_ga_compd_generation.population(size=50))

dir_name = os.path.split(os.getcwd())[0]
path_name = f"{dir_name}\\CO2RR\\New_datasets\\prepr.csv"
df = pd.read_csv(path_name)
X = df.drop(["FE, %", 'DOI'], axis=1)
X = X.loc[X["Product"] == "C2H4"]
df_new = Encoding(df).new_df
col = list(df_new.columns)

# Write all the blocks of descriptors, which are correlated 
correl_features = {'width min (nm)': ['width min (nm)','width aver (nm)', 'width max (nm)', 'length min (nm)', 'length aver (nm)',  'length max (nm)'],
                   'Cu, %':['Cu, % (at.)', 'Cu+, % (at.)', 'Cu(2+), % (at.)'],
                   '1_efermi': ['1_efermi', '1_density_atomic', '1_total_magnetization_normalized_formula_units', '1_energy_above_hull', '1_energy_per_atom', '1_volume', '1_band_gap'],
                   '2_efermi': ['2_efermi', '2_density_atomic', '2_total_magnetization_normalized_formula_units', '2_energy_above_hull', '2_energy_per_atom', '2_volume', '2_band_gap'],
                   'Base_carbon paper electrode': ['Base_carbon paper electrode', 'Base_gasdiffusion electrode'],
                   'anion_molar_conductance': ['anion_molar_conductance', 'anion_mobility', 'anion_diffusion_coefficient', 'anion_hydr_R_of_ion'],
                   'Type of reactor_H-cell': ['Type of reactor_H-cell', 'anion_molar_conductance', 'anion_mobility', 'anion_diffusion_coefficient', 'anion_hydr_R_of_ion',
                                              "conc, M", "pH"]}
levels = list(itertools.chain(*correl_features.values()))

def to_crossover(indv1, indv2, cross_over_frequency):
    a = random.random()
    for each in range(0, len(indv1)-1):
        conditions_changed = False
        # if (each ==1) or (each ==9) or (each == 10) or (each == 11) or (each == 12):
        #     if random.random()< cross_over_frequency:
        #         indv1[each] = indv2[each]
        #     continue   
        if a < cross_over_frequency:
            if col[each] in levels:
                if col[each] in correl_features:
                    for i in range(len(correl_features[col[each]])):
                        actual_index = col.index(levels[i])
                        indv1[actual_index] = indv2[actual_index]
                continue
            indv1[each] = indv2[each]

    return indv1

def to_mutation(individual1, mutation_rate):
    individual2 = indv2_list.iloc[random.randrange(20)].values.tolist()
    mut = to_crossover(individual1, individual2, mutation_rate)
    return mut

def evolve_crossing(df_compound_list, cross_over_rate, mutation_rate):
    original = df_compound_list
    unique = []
    length = len(original)-2
    j = 0
    # while j < length:
    #     if str(original.iloc[[j], [2]].values) == str(original.iloc[[j+1],[2]].values):
    #         unique.append(original.iloc[j].values.tolist())
    #         j += 1
    #     else:
    #         unique.append(original.iloc[j].values.tolist())
    #     j+= 1

    # dff = pd.DataFrame(unique, columns=original.columns)

    dff = original.copy()
    #crossing two individuals
    i = 0
    selected_ind = []
    while i < len(dff):
        individual1 = dff.iloc[i].values.tolist()
        individual2 = dff.iloc[random.randint(0, len(dff) -1)].values.tolist()
        cross_individual = to_crossover(individual1, individual2, cross_over_rate)
        mutate_individual =to_mutation(cross_individual, mutation_rate)
        selected_ind.append(mutate_individual)
        i +=1
    dframe =pd.DataFrame(selected_ind, columns=df_compound_list.columns)
    #selection pressure
    dframe_copy = dframe.copy()
    # dframe_copy= dframe_copy.iloc[: , :-3]
    dframe_evolved = MV_ga_compd_generation.fitness(dframe_copy)
    #select parents if they have high fitness (drop children) or select children if parents have low fitness
    selection = []
    for a in range(len(dff)):
        if dff.iloc[a,-1] >= dframe_evolved.iloc[a,-1]:
            selection.append(dff.iloc[a].values.tolist())
        else:
            selection.append(dframe_evolved.iloc[a].values.tolist())

    df_new = pd.DataFrame(selection, columns=df_compound_list.columns)
    all_sort = df_new.sort_values('FE', ascending=False)
    all_sort.reset_index(drop=True, inplace=True)
    without_selection = pd.DataFrame(dframe_evolved, columns=df_compound_list.columns)
    return all_sort

# population_size = 100
# mutation_rate = 0.3
# cross_over_rate = 0.3
# in1 = ['HepG2', 'AlamarBlue', 'TiO2', 'original', 'Human', 'Human', 'epithelial', 'liver', 'Carcinoma', 48, 600.0, 549.0, 20.02, 5.369127517, 2.806666667, -0.93, 1.4, 16, 79.865, 2, 0, 0, -0.2401, 2.878049394, 1.683250823, 0.0, 0.314285714, 3.314285714, 76.53795327071668, 74.7304359843506, 1.8075172863660782]
# in2 = ['Hep', 'Alamar', 'C', 'original1', 'Human1', 'Human1', 'epithelial1', 'liver1', 'Carcinoma1', 12, 19.0, 39.7, 8.29, 0.0, 2.55, 0.0, 0.7, 4, 12.011, 0, 0, 0, 0.08129, 0.5, 0.0, 0.0, 0.0, 0.0, 73.8215991847434, 72.4381269946488, 1.3834721900946079]

# print(to_crossover(in1,in2,cross_over_frequency))
# print(to_mutation(in1, mutation_rate))

# df = ga_compd_generation.fitness(ga_compd_generation.population(population_size)).sort_values('Fitness', ascending=False)
# df = df.reset_index(drop=True)
# print(evolve_crossing(df, cross_over_rate, mutation_rate))
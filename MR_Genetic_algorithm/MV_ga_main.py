import pandas as pd
import MV_ga_compd_generation
import MV_ga_crossing_mutation
import time
from tqdm import tqdm

population_size = 100
mutation_rate = 0.1
cross_over_rate = 0.1

# df = ga_compd_generation.fitness(ga_compd_generation.population(population_size)).sort_values('Fitness', ascending=False)
df_high_50 = list()

def new_generations(Gen, population_size):
    half = int((population_size * 0.5)+1)
    selected = Gen.iloc[:half,:]
    # print(selected)
    new = [selected, MV_ga_compd_generation.fitness(MV_ga_compd_generation.population(half))]
    new_generation_input = pd.concat(new)
    new_generation_input.reset_index(drop=True, inplace=True)
    # print(new_generation_input)
    new_gen = MV_ga_crossing_mutation.evolve_crossing(new_generation_input, cross_over_rate, mutation_rate)
    new_gen.reset_index(drop=True, inplace=True)
    # print(new_gen)
    # mut_pop = new_gen.drop_duplicates()
    # return mut_pop.head(population_size)
    return new_gen

col = list()
#print('original', df, 'new', new_generations(df))
means = []
maxs = []
def Genetic_Algorithm(generation_number, population_size): #(population_size):
    Generation1 = MV_ga_compd_generation.fitness(MV_ga_compd_generation.population(population_size)).sort_values('FE', ascending=False)
    # print('Generation 1 and Fitness', Generation1.iloc[0][0], Generation1, '\n' )
    mean1 = Generation1['FE'][:len(Generation1) // 2].mean()
    max1 = Generation1['FE'].max()
    print('mean1: ', mean1, 'max1:' , max1)
    #Generation1.to_csv('output/results/ovary/pop_size_50/t2/pop_size_' + str(population_size) + '_Generation_'+ str(generation_number) + '.csv')
    Generation1.to_csv('MR_Genetic_algorithm/results/pop_size_' + str(population_size) + '_Generation_1.csv')
    Generation2 = MV_ga_crossing_mutation.evolve_crossing(Generation1, cross_over_rate, mutation_rate)
    # print('Generation 2 and Fitness ', Generation2.iloc[0][0], Generation2, '\n')
    mean2 = Generation2['FE'].mean()
    max2 = Generation2['FE'].max()
    mean2 = Generation2['FE'][:len(Generation2) // 2].mean()
    print('mean1: ', mean2, 'max1:', max2)
    #Generation2.to_csv('output/results/pop_size_50/t2/pop_size_' + str(population_size)+ '_Generation_'+ str(generation_number) + '.csv')
    Generation2.to_csv('MR_Genetic_algorithm/results/pop_size_' + str(population_size)+ '_Generation_2.csv')
    global col
    col =Generation2.columns
    Generation_next = Generation2
    means = [ mean1, mean2]
    maxs = [max1, max2]
    #print('means', means, 'maxs', maxs)
    g = 3
    i =  Generation2.iloc[0][0]
    #while i <= 100 and g in range(generation_number+1):
    while g in range(generation_number + 1):
        Generation_next = new_generations(Generation_next, population_size)
        i = Generation_next.iloc[0][0]
        # mean = Generation_next['Fitness'].mean()
        max = Generation_next['FE'].max()
        mean = Generation_next['FE'][:len(Generation_next) // 2].mean()
        # max = Generation_next['Fitness'][:len(Generation_next) // 2].max()
        df_high_50.extend((Generation_next[Generation_next["FE"] > 50].values.tolist()))
        Generation_next.to_csv('MR_Genetic_algorithm/results/pop_size_' + str(population_size) + '_Generation_' + str(g) + '.csv')
        #print('generation_number:', g, 'fitness', i, '\n')
        #print(Generation_next)


        #Generation_next.to_csv('output/results/pop_size_50/t2/pop_size_' +str(population_size)+ '_Generation_' + str(g) +'.csv')

        # Generation_next.to_csv('MR_Genetic_algorithm/results/pop_size_' + str(population_size) + '_Generation_' + str(g) + '.csv')

        means.append(mean)
        maxs.append(max)
        g += 1

    #print(means)
    #print(maxs)
    genn = generation_number + 1
    gens = list(range(1,genn))
    summary = pd.DataFrame( list(zip( gens, means, maxs)), columns= ['generations','mean', 'max'] )
    print(summary)
    #summary.to_csv('output/results/pop_size_50/t2/summary_pop_size_' + str(population_size) + '.csv')
    summary.to_csv('MR_Genetic_algorithm/results/summary_pop_size_' + str(population_size) +'_gen_' + str(generation_number)+'.csv')
    return Generation_next

def final_loop():
    pop_col = []
    time_all = []
    gen_col = []
    gen = 10
    while gen <=100:
        population_size = 10
        while population_size <= 100:
            st = time.time()
            Genetic_Algorithm(gen, population_size)
            gen_col.append(gen)
            escape_time = time.time() - st
            time_all.append(escape_time)
            pop_col.append(population_size)
            print('Escape time:', escape_time)
            population_size += 10
        gen +=10
        et = pd.DataFrame(list(zip(pop_col, gen_col, time_all)), columns=['population_size','Generation number', 'Time'])
        et.to_csv('MR_Genetic_algorithm/results/Time_' + str(population_size-10) + '.csv')
        print(f"{gen}/100")
    df_for_save = pd.DataFrame(df_high_50, columns=col)
    df_for_save.drop_duplicates(inplace=True)
    df_for_save.to_csv('MR_Genetic_algorithm/results/Higher_50_samples.csv.csv')

final_loop()
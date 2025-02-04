
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd

from .base import Data


def plot_system(system : Data, seqLength : int, excludeY=True):
    """
        Plots one roll-out of the given system and seqLength
    """

    X,y = system.sample(1, seqLength)

    plot_trajectory_from_data(X,y, excludeY=excludeY)

def plot_trajectory_from_data(X : np.array, y : np.array, sample_n = 0,  excludeY=True, ylabel=None, xlabel=None):
    
    """
        Plots trajectory from data
        sample_n: sample index
    """

    fig, ax = plt.subplots()

    dim = X.shape[2]
    for d in range(dim):

        trajectory = list(X[sample_n,:,d].squeeze())
        if not excludeY: trajectory.append(y[sample_n])
        ax.plot(list(range(1,len(trajectory)+1)) ,trajectory, alpha=0.9)

    if not xlabel: 
        ax.set_xlabel("Time steps")
    else:
        ax.set_xlabel(xlabel)
    if not ylabel: 
        ax.set_ylabel("State")
    else:
        ax.set_ylabel(ylabel)
        
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_linewidth(3)
    ax.spines['left'].set_linewidth(3)

    return fig, ax


color_dict = {
    'Baseline' : 'blue',
    'LuPTS'    : 'red',
    'Stat-LuPTS': 'black',
    'Distill-Seq': 'purple',
    'Distill-Concat': 'green',
    'SelectBest'      : 'orange',
    'RF' : 'green',
    'KNN' : 'purple',
    'MLP' : 'gray'

} 
marker_dict = {
    'Baseline' : 's',
    'LuPTS'    : 'o',
    'Stat-LuPTS': 'D',
    'Distill-Seq': '^',
    'Distill-Concat': 'D',
    'SelectBest'      : 'p',
    'RF' : '*',
    'KNN' : 'X',
    'MLP' : '^'
}

def method_color(method_name):
    if method_name in color_dict:
        return color_dict[method_name]
    else:
        return 'yellow'

def method_marker(method_name):
    if method_name in marker_dict:
        return marker_dict[method_name]
    else:
        return 'X'

def score_label(score_str):

    if score_str == 'r2_score':
        return '$R^2$ score'
    else:
        return score_str

def set_mpl_default_settings():
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']) # Set the default color cycle
    mpl.rcParams['font.family'] = 'serif'
    mpl.rcParams['font.size'] = 18


def print_table(dict_list, n_size, timestep=1):
    """
    Print out table for LaTeX
    """
    results_dict = {'Method': [model for model in dict_list[0]['model_list']]}
    for city_dict in dict_list:
        
        city_results = []
        n_list = city_dict['n_list']
        city = city_dict['city']

        assert n_size in n_list, "Missing desired sample size in data"

        for idx, model in enumerate(city_dict['model_list']):
            
            assert model == results_dict['Method'][idx], "Incorrect ordering in results_dict entry for Methods"

            for jdx, n in enumerate(n_list):
                if int(n) == int(n_size):
                    data_mean, data_std = city_dict['timestep'][timestep][model][jdx]
                    city_results.append(f"{data_mean:0.2f} ({data_std:0.2f})")
                    break
        
        results_dict[city.capitalize()] = city_results

    df = pd.DataFrame(results_dict)

    print(df.to_latex(index=False))

    return df
from utils_mtmc.get_mtmc_files import *
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def run_car_mileage_in_switzerland_in_2015():
    df_vehicles, nb_observations = get_nb_km_in_last_12_months_with_weights()
    # Sum observations by intervals
    df_km_per_interval = sum_observations_by_intervals(df_vehicles, nb_intervals=10)
    # df_km_per_interval.loc[0] = [0, 0]
    df_with_0_0 = pd.DataFrame([[0, 0]], columns=['cumulative_household_weight_prop', 'cumulative_weighted_nb_km_prop'])
    df_km_per_interval = df_with_0_0.append(df_km_per_interval)
    # Plot figure
    plot_figure_in_french(df_km_per_interval, nb_observations)
    # ...
    # Save table as CSV
    df_km_per_interval.to_csv('../data/output/car_mileage_in_Switzerland_in_2015.csv', sep=';', index=False,
                              header=['Cumulative proportion of private cars, in increasing order of mileage',
                                      'Cumulative proportion of total mileage'])


def plot_figure_in_french(df_km_per_interval, nb_observations):
    cumulative_nb_km_prop_for_70_pc = int(round(100 * df_km_per_interval.iloc[7]['cumulative_weighted_nb_km_prop']))
    sns.set(rc={'figure.figsize': (6.4, 6)})
    sns.set_style("whitegrid", {'axes.spines.bottom': False,
                                'axes.spines.left': False,
                                'axes.spines.right': False,
                                'axes.spines.top': False})
    sns_plot = sns.pointplot(x='cumulative_household_weight_prop', y='cumulative_weighted_nb_km_prop',
                             data=df_km_per_interval)
    sns_plot.set(yticklabels=['', '0%', '20%', '40%', '60%', '80%', '100%'])
    sns_plot.set(xticklabels=['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
    plt.text(x=-2.15, y=1.16, s='Répartition du kilométrage des voitures privées, en 2015', fontsize=16, weight='bold')
    plt.text(x=-2.15, y=-0.5, s='Exemple de lecture: en 2015, 70% des voitures privées qui avaient parcouru le '
                                'kilométrage le plus faible lors des 12 mois\n'
                                'précédents avaient réalisé ' + str(cumulative_nb_km_prop_for_70_pc) +
                                '% du kilométrage total des voitures privées.\n\n'
                                'Base: ' + str("{0:,g}".format(nb_observations)).replace(",", " ") +
                                ' voitures privées dont le kilométrage est connu\n\n'
                                'Source: OFS, ARE - Microrecensement mobilité et transports (MRMT)',
             fontsize=8, alpha=0.75)
    plt.subplots_adjust(bottom=0.28)
    sns_plot.set_xlabel("Proportion des véhicules dans l'ordre du plus petit au plus grand kilométrage")
    sns_plot.set_ylabel('Proportion du kilométrage total des voitures privées')

    sns_figure = sns_plot.get_figure()
    sns_figure.savefig('../data/output/car_mileage_in_Switzerland_in_2015.png', dpi=600)


def sum_observations_by_intervals(df_vehicles, nb_intervals):
    sum_weigths = df_vehicles['household_weight'].sum()
    sum_nb_km_in_last_12_months = df_vehicles['weighted_nb_km'].sum()
    length_intervals = sum_weigths / nb_intervals
    array_of_intervals = np.arange(0, sum_weigths + length_intervals, length_intervals)
    df_km_per_interval = df_vehicles.groupby(pd.cut(df_vehicles['cumulative_household_weight'],
                                                    array_of_intervals)).sum()
    del df_km_per_interval['cumulative_household_weight']
    df_km_per_interval['household_weight_prop'] = df_km_per_interval['household_weight'] / sum_weigths
    del df_km_per_interval['household_weight']
    df_km_per_interval['weighted_nb_km_prop'] = \
        df_km_per_interval['weighted_nb_km'] / sum_nb_km_in_last_12_months
    del df_km_per_interval['weighted_nb_km']
    df_km_per_interval['cumulative_household_weight_prop'] = df_km_per_interval['household_weight_prop'].cumsum(axis=0)
    df_km_per_interval['cumulative_weighted_nb_km_prop'] = df_km_per_interval['weighted_nb_km_prop'].cumsum(axis=0)
    del df_km_per_interval['household_weight_prop']
    del df_km_per_interval['weighted_nb_km_prop']
    return df_km_per_interval


def get_nb_km_in_last_12_months_with_weights():
    selected_columns = ['WM', 'fahrzeugart', 'f30800_31600', 'f30900_31700']
    df_vehicles = get_vehicles(selected_columns=selected_columns)
    # Rename variables
    df_vehicles = df_vehicles.rename(columns={'WM': 'household_weight',
                                              'fahrzeugart': 'type_of_vehicle',  # 1 corresponds to car,
                                              # 2 to motorbikes
                                              'f30800_31600': 'total_mileage',  # -97: doesn't know,
                                              # -98: no answer
                                              'f30900_31700': 'nb_km_in_last_12_months',  # -97: doesn't know,
                                              # -98: no answer,
                                              # -99: no mileage (0 km) or
                                              # no answer to question about total mileage
                                              })
    # Select cars only (no motorbikes)
    df_vehicles = df_vehicles[df_vehicles['type_of_vehicle'] == 1]
    del df_vehicles['type_of_vehicle']
    # Replace the -99 value by 0 in the nb of km in the last 12 months if the vehicle has no mileage at all
    df_vehicles.loc[df_vehicles['total_mileage'] == 0, 'nb_km_in_last_12_months'] = 0
    del df_vehicles['total_mileage']
    # Remove observations where the respondent doesn't know the mileage or doesn't answer
    df_vehicles = df_vehicles[df_vehicles.nb_km_in_last_12_months != -97]
    df_vehicles = df_vehicles[df_vehicles.nb_km_in_last_12_months != -98]
    df_vehicles = df_vehicles[df_vehicles.nb_km_in_last_12_months != -99]
    nb_observations = len(df_vehicles)
    print('Number of private cars with known mileage:', nb_observations)
    ''' Sort the nb of km made in the last 12 months:
    Here we sort by the nb of km in the last 12 months and not by the *weighted* nb of km in the last 12 months. 
    A vehicle with a high mileage, say 40'000 km in the last 12 months, must be at the top of ranking, independently of 
    its weight. If its weight is small, say 0.2, it just means that this vehicle ist not very representative and will 
    be grouped with more vehicles to represent some proportion of the population (say 1%). '''
    df_vehicles.sort_values('nb_km_in_last_12_months', inplace=True)
    # Compute weighted nb of km in last 12 months
    df_vehicles['weighted_nb_km'] = df_vehicles['nb_km_in_last_12_months'] * df_vehicles['household_weight']
    del df_vehicles['nb_km_in_last_12_months']
    # Create a column containing the cumulative sum of weights
    df_vehicles['cumulative_household_weight'] = df_vehicles['household_weight'].cumsum(axis=0)
    return df_vehicles, nb_observations


if __name__ == '__main__':
    run_car_mileage_in_switzerland_in_2015()

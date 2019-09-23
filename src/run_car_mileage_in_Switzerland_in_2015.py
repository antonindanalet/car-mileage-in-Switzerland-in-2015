from get_ecdf import get_ecdf
from get_average_mileage_per_interval import get_average_mileage_per_interval
from utils_mtmc.get_mtmc_files import get_vehicles

import matplotlib.pyplot as plt


def run_car_mileage_in_switzerland_in_2015():
    nb_intervals = 10
    df_vehicles, nb_observations = get_nb_km_in_last_12_months_with_weights()
    ''' Cumulative distribution function: prepare data, plot them and save them as CSV '''
    get_ecdf(nb_intervals, df_vehicles, nb_observations)
    ''' Average mileage per interval '''
    get_average_mileage_per_interval(df_vehicles, nb_intervals, nb_observations)
    ''' Test '''
    df_vehicles[df_vehicles['nb_km_in_last_12_months'] > 60000] = 60000
    fig, ax = plt.subplots()
    df_vehicles.hist(column='nb_km_in_last_12_months', bins=12, ax=ax, density=True)
    fig.savefig('../data/output/test.png', dpi=600)


def get_nb_km_in_last_12_months_with_weights():
    selected_columns = ['WM', 'fahrzeugart', 'f30900_31700', 'f30600_31500', 'f31000_31800']
    df_vehicles = get_vehicles(selected_columns=selected_columns)
    # Rename variables
    df_vehicles = df_vehicles.rename(columns={'WM': 'household_weight',
                                              'fahrzeugart': 'type_of_vehicle',  # 1 corresponds to car,
                                                                                 # 2 to motorbikes
                                              'f30900_31700': 'nb_km_in_last_12_months',  # -97: doesn't know,
                                                                                          # -98: no answer,
                                                                                          # -99: no mileage (0 km) or
                                                                                          #      no answer to question
                                                                                          #      about total mileage
                                              'f30600_31500': 'matriculation_year',  # -98: no answer
                                                                                     # -97: doesn't know
                                              'f31000_31800': 'nb_km_abroad'  # -99: nb_km_in_last_12_months = 0 or -99
                                                                              # -98: no answer
                                                                              # -97: doesn't know
                                              })
    # Select cars only (no motorbikes)
    df_vehicles = df_vehicles[df_vehicles['type_of_vehicle'] == 1]
    del df_vehicles['type_of_vehicle']
    # Select only cars with matriculation year known and before 2015
    df_vehicles = df_vehicles[df_vehicles['matriculation_year'] < 2015]
    df_vehicles = df_vehicles[df_vehicles['matriculation_year'] > 0]
    del df_vehicles['matriculation_year']
    # Remove observations where the respondent doesn't know the mileage or doesn't answer
    df_vehicles = df_vehicles[df_vehicles.nb_km_in_last_12_months >= 0]
    nb_observations = len(df_vehicles)
    print('Number of private cars with known mileage and known matriculation time:', nb_observations)
    ''' Sort the nb of km made in the last 12 months:
    Here we sort by the nb of km in the last 12 months and not by the *weighted* nb of km in the last 12 months.
    A vehicle with a high mileage, say 40'000 km in the last 12 months, must be at the top of ranking, independently of
    its weight. If its weight is small, say 0.2, it just means that this vehicle ist not very representative and will
    be grouped with more vehicles to represent some proportion of the population (say 1%). '''
    df_vehicles.sort_values('nb_km_in_last_12_months', inplace=True)
    # Compute weighted nb of km in last 12 months
    df_vehicles['weighted_nb_km'] = df_vehicles['nb_km_in_last_12_months'] * df_vehicles['household_weight']
    # Create a column containing the cumulative sum of weights
    df_vehicles['cumulative_household_weight'] = df_vehicles['household_weight'].cumsum(axis=0)
    return df_vehicles, nb_observations


if __name__ == '__main__':
    run_car_mileage_in_switzerland_in_2015()

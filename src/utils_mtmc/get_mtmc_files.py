import pandas as pd

folder_path_2015 = '../data/input/'


def get_vehicles(selected_columns=None):
    with open(folder_path_2015 + 'fahrzeuge.csv', 'r') as vehicles_file:
        if selected_columns is None:
            df_vehicles = pd.read_csv(vehicles_file)
        else:
            df_vehicles = pd.read_csv(vehicles_file,
                                      dtype={'HHNR': int},
                                      usecols=selected_columns)
    return df_vehicles

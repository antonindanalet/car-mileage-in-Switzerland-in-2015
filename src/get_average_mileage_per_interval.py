from utils_mtmc.compute_confidence_interval import get_weighted_avg_and_std
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt


def get_average_mileage_per_interval(df_vehicles, nb_intervals, nb_observations):
    """
    Average mileage per interval
    :param df_vehicles: the pandas dataframe with the data about the privately-owned vehicles
    :param nb_intervals: the number of intervals in which we divide the list of vehicles by their mileage
    :return: nothing, but generates a CSV-file with the results, a figure and prints the main results
    """
    df_vehicles_avg = compute_average_and_std_per_interval(df_vehicles, nb_intervals)
    plot_average_and_std_per_interval(df_vehicles_avg, nb_observations)


def plot_average_and_std_per_interval(df_vehicles_avg, nb_observations):
    dict_title = {'fr': 'Prestations kilométriques moyennes des voitures,\nen 2015',
                  'de': 'Durchschnittliche Fahrleistung der Personenwagen,\n2015',
                  'en': 'Average mileage of cars in 2015'}
    dict_subtitle = {'fr': 'Uniquement les voitures que possèdent les ménages; Prestations durant les 12 mois '
                           "précédant le jour de l'enquête",
                     'de': 'Nur Personenwagen, die sich im Besitz von Haushalten befinden; Fahrleistung in den 12 '
                           'Monaten vor dem Befragungstag',
                     'en': 'Only private cars owned by households; Mileage in the 12 months before the day of the '
                           'survey'}
    dict_x_label = {'fr': "Proportion des voitures dans l'ordre croissant de leur prestation kilométrique",
                    'de': 'Anteil der Privatwagen in aufsteigender Reihenfolge ihrer Fahrleistung',
                    'en': 'Proportion of privately owned vehicles in the increasing order of mileage'}
    dict_y_label = {'fr': 'Kilométrage moyen lors des 12 derniers mois (en km)',
                    'de': 'Jährliche Fahrleistung (in km)',
                    'en': 'Average mileage in the last 12 months (in km)'}
    # avg_nb_km_for_top_group = int(round(df_vehicles_avg.iloc[9]))
    dict_example = {'fr': 'Exemple de lecture: en 2015, le 10% des voitures avec les prestations kilométriques les plus '
                          'élevées ont réalisé\n28 620 km en moyenne.\n\n'
                          'Base: ' + str("{0:,g}".format(nb_observations)).replace(",", " ") +
                          ' voitures qui ont été mises en circulation avant 2015 et avec '
                          "indication valable de l'âge du véhicule et des\nprestations kilométriques annuelles\n\n"
                          'Source: OFS, ARE - Microrecensement mobilité et transports (MRMT)',
                    'de': 'Lesebeispiel: 2015 haben die 10% der Personenwagen, die die höchste Fahrleistung gemacht '
                          'haben, durchschnittlich\n28 620 km realisiert.\n\n'
                          'Basis: ' + str("{0:,g}".format(nb_observations)).replace(",", " ") +
                          ' Privatwagen, die vor 2015 in Verkehr gesetzt wurden und gültige Angaben zum Fahrzeugalter '
                          'und zur\nJahresfahrleistung aufweisen\n\n'
                          'Quelle: BFS, ARE - Mikrozensus Mobilität und Verkehr (MZMV)',
                    'en': 'Reading example: in 2015, the 10% of privately owned cars with the largest mileage '
                          'traveled 28 620 km on average.\n\n'
                          'Basis: ' + str("{0:,g}".format(nb_observations)).replace(",", " ") +
                          ' cars that were put into service before 2015 and with a valid age of the vehicule and '
                          'mileage in the last\n12 months\n\n'
                          'Source: FSO, ARE - Mobility and Transport Microcensus (MTMC)'}
    sns.set_style("whitegrid", {'axes.spines.bottom': False,
                                'axes.spines.left': False,
                                'axes.spines.right': False,
                                'axes.spines.top': False})
    plt.subplots_adjust(bottom=0.26)  # Add some place below the figure
    plt.subplots_adjust(left=0.14)  # Add some place below the figure
    for language in ['fr', 'de', 'en']:
        plt.clf()
        sns_plot = sns.barplot(df_vehicles_avg.index, df_vehicles_avg.values, color='#0098c6')
        sns_plot.set(yticklabels=['0', '5000', '10 000', '15 000', '20 000', '25 000', '30 000'])
        sns_plot.set(xticklabels=['10%', '10%', '10%', '10%', '10%', '10%', '10%', '10%', '10%', '10%'])
        right_margin_param = -1.73
        if language == 'fr':  # Title on two lines
            plt.text(x=right_margin_param, y=1.08*30000, s=dict_title[language], fontsize=16, weight='bold')
            plt.text(x=right_margin_param, y=1.04*30000, s=dict_subtitle[language], fontsize=8)
            plt.text(x=right_margin_param, y=-0.37 * 30000, s=dict_example[language], fontsize=8)
        elif language == 'de':
            right_margin_param_de = -2.1
            plt.text(x=right_margin_param_de, y=1.07 * 30000, s=dict_title[language], fontsize=16, weight='bold')
            plt.text(x=right_margin_param_de, y=1.03 * 30000, s=dict_subtitle[language], fontsize=8)
            plt.text(x=right_margin_param_de, y=-0.37 * 30000, s=dict_example[language], fontsize=8)
        else:
            plt.text(x=right_margin_param, y=1.1 * 30000, s=dict_title[language], fontsize=16, weight='bold')
            plt.text(x=right_margin_param, y=1.06 * 30000, s=dict_subtitle[language], fontsize=8)
            plt.text(x=right_margin_param, y=-0.37*30000, s=dict_example[language], fontsize=8)
        # Add values on each bar
        nb_bar = 0
        for row in df_vehicles_avg:
            sns_plot.text(nb_bar, row + 200, round(row), ha="center", fontsize=11)
            nb_bar += 1
        sns_plot.set_xlabel(dict_x_label[language])
        sns_plot.set_ylabel(dict_y_label[language])
        sns_figure = sns_plot.get_figure()
        sns_figure.savefig('../data/output/average_per_interval/'
                           'average_car_mileage_in_Switzerland_in_2015_' + language + '.png', dpi=600)


def compute_average_and_std_per_interval(df_vehicles, nb_intervals):
    ''' Filter the observations to keep only those that can be differentiated between kilometer driven in Switzerland
    and abroad '''
    # new column with values: 0 if no km was performed in the last 12 years and
    #                         with the number of kilometers driven abroad otherwise
    df_vehicles['dist_abroad'] = df_vehicles.apply(lambda row: (row.nb_km_in_last_12_months != 0) * row.nb_km_abroad,
                                                   axis=1)
    df_vehicles = df_vehicles[df_vehicles['dist_abroad'] >= 0]  # All negative observations correspond to no information
    nb_observations = len(df_vehicles)  # Statistical bases (!= basis for empirical cumulative distribution function
    ''' Compute the average mileage in Switzerland (all cars) '''
    """ TO DO: COMPUTE MILEAGE IN SWITZERLAND AND ABROAD SEPARATELY """
    nb_km_in_last_12_months_avg_and_std = get_weighted_avg_and_std(df_vehicles, 'household_weight',
                                                                   list_of_columns=['nb_km_in_last_12_months'])
    nb_km_in_last_12_months_avg = nb_km_in_last_12_months_avg_and_std[0]['nb_km_in_last_12_months'][0]
    nb_km_in_last_12_months_std = nb_km_in_last_12_months_avg_and_std[0]['nb_km_in_last_12_months'][1]
    nb_km_in_last_12_months_basis = nb_km_in_last_12_months_avg_and_std[1]
    print('Number of kilometers in the last 12 months:', nb_km_in_last_12_months_avg,
          '+/-', nb_km_in_last_12_months_std,
          '(statistical basis:', str(nb_km_in_last_12_months_basis) + ')')
    ''' Compute the average mileage per interval '''
    sum_weights = df_vehicles['household_weight'].sum()
    length_intervals = sum_weights / nb_intervals
    array_of_intervals = np.arange(0, sum_weights+1, length_intervals)
    ''' Here we group by groups of similar cumulative household weight. Since each observation is one car, it represents
    groups of similar numbers of cars.
    Then, we apply the function get_weighted_avg_and_std, computing the weighted average and the standard deviation. 
    This function returns a list of two elements. The first one ist the weighted average and the standard deviation; 
    The second one is the statistical basis of the computation. Here, we are only interested in the first element.
    Thus is '[0]' after the parameters of the function below. Moreover, we compute the weighted average and the 
    standard deviation only for one variable of the dataframe, 'nb_km_in_last_12_months'. We would like to get only the
    results for this variable. Thus is '['nb_km_in_last_12_months']' written below a the end of the function we apply. 
    '''
    df_km_per_interval_avg = df_vehicles.groupby(pd.cut(df_vehicles['cumulative_household_weight'],
                                                        array_of_intervals)).apply(
        lambda x: get_weighted_avg_and_std(x, 'household_weight',
                                           list_of_columns=['nb_km_in_last_12_months'])[0]['nb_km_in_last_12_months'][0]
    )
    df_km_per_interval_std = df_vehicles.groupby(pd.cut(df_vehicles['cumulative_household_weight'],
                                                        array_of_intervals)).apply(
        lambda x: get_weighted_avg_and_std(x, 'household_weight',
                                           list_of_columns=['nb_km_in_last_12_months'])[0]['nb_km_in_last_12_months'][1]
    )
    df_km_per_interval = pd.concat([df_km_per_interval_avg, df_km_per_interval_std], axis=1)
    df_km_per_interval.columns = ['Average mileage of cars per group of cars of the same size in increasing order of '
                                  'mileage', '+/-']
    df_km_per_interval.to_csv(os.path.join('..', 'data', 'output', 'average_per_interval', 'average_per_interval.csv'),
                              sep=';',
                              index=False)
    print('Number of private cars with known mileage and known matriculation time:', nb_observations)
    return df_km_per_interval_avg
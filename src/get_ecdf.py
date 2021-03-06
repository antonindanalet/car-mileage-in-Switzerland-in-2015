import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


def get_ecdf(nb_intervals, df_vehicles, nb_observations):
    # Sum observations by intervals
    df_km_per_interval = sum_observations_by_intervals(df_vehicles, nb_intervals=nb_intervals)
    # Add the data point (0,0) for the visualization
    df_with_0_0 = pd.DataFrame([[0, 0]], columns=['cumulative_household_weight_prop', 'cumulative_weighted_nb_km_prop'])
    df_km_per_interval = df_with_0_0.append(df_km_per_interval, sort=True)
    # Plot figure in French, German and English
    plot_ecdf_figures(df_km_per_interval, nb_observations)
    # Save table as CSV
    df_km_per_interval[['cumulative_household_weight_prop',
                        'cumulative_weighted_nb_km_prop']] \
        .to_csv(os.path.join('..', 'data', 'output', 'empirical_cumulative_distribution_function',
                             'car_mileage_in_Switzerland_in_2015.csv'),
                sep=';',
                index=False,
                header=['Cumulative proportion of private cars, in increasing order of mileage',
                        'Cumulative proportion of total mileage'])


def weigthed_average(group):
    d = group['data']
    w = group['weights']
    return (d * w).sum() / w.sum()


def plot_ecdf_figures(df_km_per_interval, nb_observations):
    dict_title = {'fr': 'Répartition des prestations kilométriques des voitures,\nen 2015',
                  'de': 'Verteilung der Fahrleistung der Personenwagen, 2015',
                  'en': 'Cumulative distribution of mileage of cars in 2015'}
    dict_subtitle = {'fr': 'Uniquement les voitures que possèdent les ménages; Prestations durant les 12 mois '
                           "précédant le jour de l'enquête",
                     'de': 'Nur Personenwagen, die sich im Besitz von Haushalten befinden; Fahreleistung in den 12 '
                           'Monaten vor dem Befragungstag',
                     'en': 'Only private cars owned by households; Mileage in the 12 months before the day of the '
                           'survey'}
    dict_x_label = {'fr': "Proportion des voitures dans l'ordre croissant de leur prestation kilométrique",
                    'de': 'Anteil der Privatwagen in aufsteigender Reihenfolge ihrer Fahrleistung',
                    'en': 'Proportion of privately owned vehicles in the increasing order of mileage'}
    dict_y_label = {'fr': 'Proportion des prestations kilométriques totales',
                    'de': 'Anteil der gesamten Fahrleistung von Privatwagen',
                    'en': 'Proportion of total mileage of privately owned cars'}
    cumulative_nb_km_prop_for_70_pc = int(round(100 * df_km_per_interval.iloc[7]['cumulative_weighted_nb_km_prop']))
    dict_example = {'fr': 'Exemple de lecture: en 2015, 70% des voitures (avec les prestations kilométriques les plus '
                          "faibles) ont réalisé " + str(cumulative_nb_km_prop_for_70_pc) +
                          '% des\nprestations kilométriques totales.\n\n'
                          'Base: ' + str("{0:,g}".format(nb_observations)).replace(",", " ") +
                          ' voitures qui ont été mises en circulation avant 2015 et avec '
                          "indication valable de l'âge du véhicule et des\nprestations kilométriques annuelles\n\n"
                          'Source: OFS, ARE - Microrecensement mobilité et transports (MRMT)',
                    'de': 'Lesebeispiel: 2015 haben 70% der Personenwagen (in ansteigender Reihenfolge ihrer '
                          'Fahrleistung), ' + str(cumulative_nb_km_prop_for_70_pc) +
                          '% der gesamten\nFahrleistung von Personenwagen realisiert.\n\n'
                          'Basis: ' + str("{0:,g}".format(nb_observations)).replace(",", " ") +
                          ' Privatwagen, die vor 2015 in Verkehr gesetzt wurden und gültige Angaben zum Fahrzeugalter '
                          'und zur\nJahresfahrleistung aufweisen\n\n'
                          'Quelle: BFS, ARE - Mikrozensus Mobilität und Verkehr (MZMV)',
                    'en': 'Reading example: in 2015, 70% of privately owned cars with the smallest mileage '
                          'traveled ' + str(cumulative_nb_km_prop_for_70_pc) +
                          '% of the total mileage\nof privately owned cars.\n\n'
                          'Basis: ' + str("{0:,g}".format(nb_observations)).replace(",", " ") +
                          ' cars that were put into service before 2015 and with a valid age of the vehicule and '
                          'mileage in the last 12 months\n\n'
                          'Source: FSO, ARE - Mobility and Transport Microcensus (MTMC)'}
    sns.set(rc={'figure.figsize': (6.4, 6.4)})
    sns.set_style("whitegrid", {'axes.spines.bottom': False,
                                'axes.spines.left': False,
                                'axes.spines.right': False,
                                'axes.spines.top': False})
    plt.subplots_adjust(bottom=0.26)  # Add some place below the figure
    for language in ['fr', 'de', 'en']:
        plt.clf()
        sns_plot = sns.pointplot(x='cumulative_household_weight_prop', y='cumulative_weighted_nb_km_prop',
                                 data=df_km_per_interval)
        sns_plot.set(yticklabels=['', '0%', '20%', '40%', '60%', '80%', '100%'])
        sns_plot.set(xticklabels=['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
        if language == 'fr':  # Title on two lines
            plt.text(x=-2.15, y=1.125, s=dict_title[language], fontsize=16, weight='bold')
            plt.text(x=-2.15, y=1.075, s=dict_subtitle[language], fontsize=8)
        else:  # Title on one line
            plt.text(x=-2.15, y=1.15, s=dict_title[language], fontsize=16, weight='bold')
            plt.text(x=-2.15, y=1.1, s=dict_subtitle[language], fontsize=8)
        plt.text(x=-2.15, y=-0.5, s=dict_example[language], fontsize=8)
        sns_plot.set_xlabel(dict_x_label[language])
        sns_plot.set_ylabel(dict_y_label[language])
        sns_figure = sns_plot.get_figure()
        sns_figure.savefig('../data/output/empirical_cumulative_distribution_function/'
                           'car_mileage_in_Switzerland_in_2015_' + language + '.png', dpi=600)


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
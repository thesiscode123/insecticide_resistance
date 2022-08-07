import pandas as pd
import seaborn as sns
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
from datetime import date, timedelta
mpl.rcParams['pdf.fonttype'] = 42

projectpath = 'C:/Users/hunagi/OneDrive - Nexus365/insecticide_resistance'


def inset_chart_plotter(expt_name, data_channels) :

    df = pd.read_csv(os.path.join(projectpath, 'simulation_outputs', 'data', '%s_inset_chart.csv' % expt_name))
    sns.set_style('whitegrid', {'axes.linewidth': 0.5})

    fig = plt.figure('Inset Chart', figsize=(12, 6))
    formatter = mdates.DateFormatter("%m-%Y")
    axes = [fig.add_subplot(2, 2, x + 1) for x in range(len(data_channels))]
    fig.subplots_adjust(left=0.08, right=0.8, bottom=0.05, top=0.95)
    fig.autofmt_xdate()
    palette = sns.color_palette('Set1', n_colors=10)

    df['date'] = df['day'].apply(lambda x: date(2021, 1, 1) + timedelta(days=x))

    for ai, (ax, channel) in enumerate(zip(axes, data_channels)):
        for ia, (a, adf) in enumerate(df.groupby('scenario')): # previous was scenario
            gdf = adf.groupby('date')[channel].agg([np.min, np.max, np.mean]).reset_index()
            print(gdf)
            ax.plot(gdf['date'], gdf['mean'], '-', label=a, color=palette[ia])
            #ax.fill_between(gdf['date'], gdf['amin'], gdf['amax'], linewidth=0, alpha=0.3, color=palette[ia])
        ax.set_ylabel(channel)
        ax.xaxis.set_major_formatter(formatter)
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        if ai == 1 :
            ax.legend(title='scenario', bbox_to_anchor=(1.6, 1))
    plt.savefig(os.path.join(projectpath, 'simulation_outputs', 'plots', '%s_inset_chart.png' % expt_name))


def vector_genetics_plotter(expt_name, plot_channel, stratify_by='Alleles') :
    df = pd.read_csv(os.path.join(projectpath, 'simulation_outputs',
                                  'data', '%s_vector_genetics_report.csv' % expt_name))
    df['date'] = pd.to_datetime(df['date'])
    sns.set_style('whitegrid', {'axes.linewidth': 0.5,
                                'legend.frameon': True})
    formatter = mdates.DateFormatter("%m-%Y")
    palette = sns.color_palette('Set2')

    for scenario, sdf in df.groupby('scenario'):

        fig = plt.figure('%s genetics' % scenario, figsize=(8, 6))
        fig.autofmt_xdate()

        ax = fig.add_subplot(2, 1, 1)
        for gi, (genome, gdf) in enumerate(sdf.groupby(stratify_by)):
            pdf = gdf.groupby('date')[plot_channel].agg(np.mean).reset_index()
            ax.plot(pdf['date'], pdf[plot_channel], '-', label=genome, color=palette[gi])
        ax.set_ylabel(plot_channel)
        ax.legend(title=stratify_by, loc='upper right', facecolor='white', framealpha=1)
        ax.xaxis.set_major_formatter(formatter)
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        ax.set_title(scenario)

        ax = fig.add_subplot(2, 1, 2)
        bottom = [0] * len(sdf['date'].unique())
        for gi, (genome, gdf) in enumerate(sdf.groupby(stratify_by)):
            pdf = gdf.groupby('date')['fraction'].agg(np.mean).reset_index()
            top = [x + y for x, y in zip(bottom, pdf['fraction'].values)]
            ax.fill_between(pdf['date'].values, bottom, top, color=palette[gi],
                            linewidth=0, alpha=0.8, label=genome)
            bottom = top
        ax.set_ylabel('%s fraction' % plot_channel)
        ax.legend(title=stratify_by, loc='upper right', facecolor='white', framealpha=1)
        ax.xaxis.set_major_formatter(formatter)
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))

        plt.savefig(os.path.join(projectpath, 'simulation_outputs', 'plots', '%s_%s_.png' % (expt_name, scenario)))

# def vector_migration_plotter(expt_name, vector_migration_plot_channel) :
#     df = pd.read_csv((os.path.join(projectpath, 'simulation_outputs',
#                                    'data', 'VectorMigrationSummary.csv')), skiprows=[i for i in range(1, 218)])
#
#     #df = df[df['FromNodeID'] == 1]
#     sns.set_style('whitegrid', {'axes.linewidth': 0.5,
#                                 'legend.frameon': True}) # setting parameters to control plot style
#     formatter = mdates.DateFormatter("%m-%Y")
#     palette = sns.color_palette('Set2')
#
#     fig = plt.figure('Daily Trips to Node X', figsize=(8, 4))
#     for d, (dest_node, ddf) in enumerate(df.groupby('ToNodeID')):
#         adf = pd.merge(left=ddf, right=df, on='date', how='outer')
#         adf = adf.fillna(0)
#         adf['fraction'] = (df['Age']/df['TotalMigrations'])
#         #adf['TotalMigrations']
#         #adf['per_capita_trips'] = (df['Age']/df['TotalMigrations'])
#        # adf.to_csv('ReportVectorMigrationSummary.csv', index=False)
#
#         ax = fig.add_subplot(1, len(df['ToNodeID'].unique()), d+1)
#         ax.xaxis.set_major_formatter(formatter)
#         sns.distplot(df['TotalMigrations'], ax=ax)
#         ax.set_title('to node %d' % dest_node)
#     plt.savefig(os.path.join(projectpath, 'simulation_outputs', 'plots', '%s.png' % expt_name))


        # ax.set_ylim(0,)
        # for gi, (migration, gdf) in enumerate(sdf.groupby('ToNodeID')):
        #     try:
        #         pdf = gdf.groupby('date')['TotalMigrations'].agg(np.mean).reset_index()
        #         ax.plot(pdf['date'], pdf['TotalMigrations'], '-', label=migration, color=palette[gi])
        #     except IndexError:
        #         pass
        # ax.set_ylabel('TotalMigrations')
        # ax.legend(title='ToNodeID', loc='upper right', facecolor='white', framealpha=1)
        # ax.xaxis.set_major_formatter(formatter)
        # ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        # ax.set_title(FromNodeID)



if __name__ == "__main__":

    expt_name = 'IH ITN Combinations'

    inset_data_channels_to_plot = ['Adult Vectors', 'Daily EIR',
                                   'Blood Smear Parasite Prevalence', 'New Clinical Cases']
    vector_genetics_plot_channel = 'VectorPopulation'
    #vector_migration_plot_channel = 'TotalMigrations'

    inset_chart_plotter(expt_name, inset_data_channels_to_plot)
    vector_genetics_plotter(expt_name, vector_genetics_plot_channel, stratify_by='Alleles')
    #vector_migration_plotter(expt_name, vector_migration_plot_channel)

    plt.show()

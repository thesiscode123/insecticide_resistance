import pandas as pd
import seaborn as sns
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
from datetime import date, timedelta
from simtools.Analysis.BaseAnalyzers import BaseAnalyzer

mpl.rcParams['pdf.fonttype'] = 42

class InsetAnalyzer(BaseAnalyzer):
    def __init__(self, exp_name, working_dir='.', sweep_variables=None):  # sweep_variables=None,

        super(InsetAnalyzer, self).__init__(working_dir=working_dir,
                                            filenames=["output/InsetChart.json"]
                                            )
        self.sweep_variables = sweep_variables or ["scenario", "ITN_coverage"]
        self.inset_channels = ['Infected', 'New Infections', 'Adult Vectors', 'Daily EIR']
        #self.sweep_variables = sweep_variables or ["start_days", 'Run_Number', 'krate_scale_factor_s']
        self.exp_name = exp_name
        # self.inset_channels = ['Infected', 'New Infections', 'Adult Vectors', 'Daily EIR']

    # def filter(self, simulation):
    #    return simulation.tags["Run_Number"] == 0

    def select_simulation_data(self, data, simulation):
        """
        Extract data from output data and accumulate in same bins as reference.
        """

        # Load data from simulation
        simdata = pd.DataFrame( { x : data[self.filenames[0]]['Channels'][x]['Data'] for x in self.inset_channels})
        simdata['day'] = simdata.index

        for sweep_var in self.sweep_variables :
            simdata[sweep_var] = simulation.tags[sweep_var]

        return simdata

    def finalize(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("No data have been returned... Exiting...")
            return

        df = pd.concat(selected, sort=False).reset_index(drop=True)

       # df['krate'] = df['krate_scale_factor_s'].apply(lambda x : 'old' if x == 1 else 'new') # comment out

        sns.set_style('whitegrid', {'axes.linewidth': 0.5})

        fig = plt.figure(figsize=(12, 8))
        formatter = mdates.DateFormatter("%m-%Y")
        axes = [fig.add_subplot(2,2, x+1) for x in range(len(self.inset_channels))]
        fig.autofmt_xdate()
        palette = sns.color_palette('Set1')

        df['date'] = df['day'].apply(lambda x : date(2013, 1, 1) + timedelta(days=x))

        for ia, (a, adf) in enumerate(df.groupby('scenario')): # comment out block

            for ax, channel in zip(axes, self.inset_channels) :
                gdf = adf.groupby('date')[channel].agg([np.min, np.max, np.mean]).reset_index()
                ax.plot(gdf['date'], gdf['mean'], '-', label=a, color=palette[ia])
                #ax.fill_between(gdf['date'], gdf['amin'], gdf['amax'], linewidth=0, color=palette[ia], alpha=0.3)
                ax.set_ylabel(channel)
                ax.legend()
                ax.xaxis.set_major_formatter(formatter)
                ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.show()


if __name__ == "__main__":

    from simtools.Analysis.AnalyzeManager import AnalyzeManager
    from simtools.SetupParser import SetupParser

    SetupParser.default_block = 'HPC'
    SetupParser.init()

    analyzer = InsetAnalyzer(exp_name='Spatial IR Rotation ITNs')

    am = AnalyzeManager('eef6b34b-f4d2-ec11-a9f8-b88303911bc1', analyzers=analyzer)
    am.analyze()
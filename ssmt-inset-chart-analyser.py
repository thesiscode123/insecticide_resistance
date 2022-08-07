import pandas as pd
import numpy as np
import os
from simtools.Analysis.BaseAnalyzers import BaseAnalyzer
from simtools.Analysis.SSMTAnalysis import SSMTAnalysis


class InsetAnalyzer(BaseAnalyzer):

    def __init__(self, exp_name, sweep_variables=None, working_dir='.'):

        super(InsetAnalyzer, self).__init__(working_dir=working_dir,
                                        filenames=["output/InsetChart.json"]
                                           )
        self.sweep_variables = sweep_variables or ["Run_Number", "ITN_coverage"]
        self.exp_name = exp_name
        self.plot_by = 'scenario'
        self.data_channels = ['Blood Smear Parasite Prevalence', 'New Clinical Cases', 'Adult Vectors', 'Daily EIR']

    def select_simulation_data(self, data, simulation):
        """
        Extract data from output data and accumulate in same bins as reference.
        """

        # Load data from simulation
        simdata = pd.DataFrame( { x : data[self.filenames[0]]['Channels'][x]['Data'] for x in self.data_channels})
        simdata['day'] = simdata.index

        for sweep_var in self.sweep_variables :
            simdata[sweep_var] = simulation.tags[sweep_var]

        return simdata

    def finalize(self, all_data):

        selected = [data for sim, data in all_data.items()]

        df = pd.concat(selected, sort=False).reset_index(drop=True)
        if not os.path.exists(os.path.join(self.working_dir, 'data')):
            os.mkdir(os.path.join(self.working_dir, 'data'))
        df.to_csv(os.path.join(self.working_dir, 'data', '%s_inset_chart.csv' % self.exp_name), index=False)


if __name__ == "__main__":

    from simtools.Analysis.AnalyzeManager import AnalyzeManager
    from simtools.SetupParser import SetupParser

    SetupParser.default_block = 'HPC'
    SetupParser.init()

    expts = {
        'IH ITN Combinations': '66187905-5d01-ed11-a9fa-b88303911bc1'
        #'IH ITN Combinations': 'abd30505-f9fd-ec11-a9fa-b88303911bc1',
    }
    analyzers = [InsetAnalyzer]
    sweep_variables = ['scenario', 'ITN_coverage']

    mode = 'local'

    for expname, expid in expts.items():

        if mode == 'local':
            projectpath = 'C:/Users/hunagi/OneDrive - Nexus365/insecticide_resistance/simulation_outputs'
            #wdir = os.path.join(projectpath, 'simulation_outputs')
            analyzer = InsetAnalyzer(exp_name=expname,
                                     sweep_variables=sweep_variables,
                                     working_dir=projectpath)

            am = AnalyzeManager(expid, analyzers=analyzer)
            am.analyze()

        else:
            wi_name = "ssmt_analyzer_%s" % expname

            args_each = {'exp_name': expname,
                         'working_dir': ".",
                         'sweep_variables': sweep_variables
                         }
            analysis = SSMTAnalysis(experiment_ids=[expid],
                                    analyzers=analyzers,
                                    analyzers_args=[args_each] * len(analyzers),
                                    analysis_name=wi_name)
            analysis.analyze()

import pandas as pd
import numpy as np
import os
from simtools.Analysis.BaseAnalyzers import BaseAnalyzer
from datetime import date, timedelta
from simtools.Analysis.SSMTAnalysis import SSMTAnalysis


class VectorGeneticsAnalyzer(BaseAnalyzer):

    def __init__(self, exp_name, stratify_by='Alleles',
                 sweep_variables=None, working_dir='.'):
        super(VectorGeneticsAnalyzer, self).__init__(working_dir=working_dir,
                                                     filenames=["output/ReportVectorGenetics_gambiae_Female_ALLELE_FREQ.csv"]
                                                     )
        self.sweep_variables = sweep_variables or ['ITN_coverage']
        self.exp_name = exp_name
        self.plot_channel = 'VectorPopulation'
        self.stratify_by = stratify_by
        self.plot_by = 'scenario'

    def select_simulation_data(self, data, simulation):
        """
        Extract data from output data and accumulate in same bins as reference.
        """

        # Load data from simulation
        simdata = data[self.filenames[0]]

        for sweep_var in self.sweep_variables :
            simdata[sweep_var] = simulation.tags[sweep_var]

        return simdata

    def finalize(self, all_data):

        selected = [data for sim, data in all_data.items()]

        df = pd.concat(selected, sort=False).reset_index(drop=True)
        df = df[df[self.stratify_by] != 'X'].reset_index(drop=True)
        df['date'] = df['Time'].apply(lambda x : date(2021, 1, 1) + timedelta(days=x))

        sdf = df.groupby(self.stratify_by)[self.plot_channel].agg(np.sum).reset_index()
        unused_genomes = sdf[sdf[self.plot_channel] == 0][self.stratify_by].values
        df = df[~df[self.stratify_by].isin(unused_genomes)]
        df = df.reset_index(drop=True)

        tdf = df.groupby(['date'] + self.sweep_variables)[self.plot_channel].agg(np.sum).reset_index()
        tdf = tdf.rename(columns={self.plot_channel: 'total'})
        df = pd.merge(left=df, right=tdf, on=['date'] + self.sweep_variables, how='left')
        df['fraction'] = df[self.plot_channel] / df['total']

        if not os.path.exists(os.path.join(self.working_dir, 'data')):
            os.mkdir(os.path.join(self.working_dir, 'data'))
        df.to_csv(os.path.join(self.working_dir, 'data', '%s_vector_genetics_report.csv' % self.exp_name), index=False)


if __name__ == "__main__":

    from simtools.Analysis.AnalyzeManager import AnalyzeManager
    from simtools.SetupParser import SetupParser

    SetupParser.default_block = 'HPC'
    SetupParser.init()

    expts = {
        'Node Checkerboard ITNs': '818fbacb-fd14-ed11-a9fb-b88303911bc1',
    }
    analyzers = [VectorGeneticsAnalyzer]
    sweep_variables = ['scenario', 'ITN_coverage']

    mode = 'local'

    for expname, expid in expts.items():

        if mode == 'local':
            projectpath = 'C:/Users/hunagi/OneDrive - Nexus365/insecticide_resistance'
            wdir = os.path.join(projectpath, 'simulation_outputs')
            analyzer = VectorGeneticsAnalyzer(exp_name=expname,
                                              sweep_variables=sweep_variables,
                                              working_dir=wdir)

            am = AnalyzeManager(expid, analyzers=analyzer)
            am.analyze()

        else:
            wi_name = "ssmt_analyzer_%s" % expname

            args_each = {'exp_name': expname,
                         'working_dir': ".",
                         'sweep_variables' : sweep_variables,
                         'stratify_by' : 'Alleles'
                         }
            analysis = SSMTAnalysis(experiment_ids=[expid],
                                    analyzers=analyzers,
                                    analyzers_args=[args_each] * len(analyzers),
                                    analysis_name=wi_name)
            analysis.analyze()


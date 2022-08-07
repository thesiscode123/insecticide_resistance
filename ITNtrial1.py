from dtk.utils.core.DTKConfigBuilder import DTKConfigBuilder
from dtk.vector.study_sites import configure_site
from simtools.ExperimentManager.ExperimentManagerFactory import ExperimentManagerFactory
from simtools.SetupParser import SetupParser
from simtools.ModBuilder import ModBuilder, ModFn
from dtk.interventions.itn import add_ITN


def configure_ITN(cb, start_day=0, coverage=1) :

    add_ITN(cb, start=start_day, coverage_by_ages=[{'min': 0, 'max': 100, 'coverage': coverage}])
    return {'ITN_coverage': coverage}


if __name__ == "__main__":
    SetupParser.default_block = 'HPC'
    SetupParser.init()

    exp_name = 'ITN_trial'
    numseeds = 10
    years = 2

    cb = DTKConfigBuilder.from_defaults('MALARIA_SIM')
    configure_site(cb, 'Namawala')

    cb.update_params( {
        'Simulation_Duration' : 365*years,
        'logLevel_SusceptibilityMalaria' : 'ERROR'
    })

    builder = ModBuilder.from_list([[ModFn(DTKConfigBuilder.set_param, 'Run_Number', seed),
                                     ModFn(configure_ITN, start_day=150, coverage=coverage)
                                     ]
                                    for seed in range(numseeds)
                                    for coverage in [0, 1]])

    run_sim_args = {
        'exp_name': exp_name,
        'config_builder': cb,
        'exp_builder': builder
    }
    exp_manager = ExperimentManagerFactory.init()
    exp_manager.run_simulations(**run_sim_args)
    # Wait for the simulations to be done
    exp_manager.wait_for_finished(verbose=True)
    assert (exp_manager.succeeded())
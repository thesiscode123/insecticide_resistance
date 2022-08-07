from dtk.utils.core.DTKConfigBuilder import DTKConfigBuilder
#from dtk.vector.study_sites import configure_site
from simtools.ExperimentManager.ExperimentManagerFactory import ExperimentManagerFactory
from simtools.SetupParser import SetupParser
from simtools.ModBuilder import ModBuilder, ModFn
from dtk.interventions.itn import add_ITN
from dtk.interventions.itn_age_season import add_ITN_age_season
from dtk.vector.species import set_species_param, set_species, set_species_genes
from dtk.utils.reports import BaseVectorGeneticsReport
from simtools.Utilities.Experiments import retrieve_experiment
#import json
import os
#import pandas as pd
#from dtk.utils.reports.VectorReport import add_vector_migration_report

def setup_simulation(cb) :
    cb.update_params({
        'Custom_Individual_Events': ['Bednet_Got_New_One', 'Bednet_Using', 'Bednet_Discarded'],
        'Birth_Rate_Dependence': 'FIXED_BIRTH_RATE',
        'Demographics_Filenames': ['demographics.json'],
        'Enable_Vector_Migration': 1,
        'Enable_Vector_Migration_Local': 1,
        'Enable_Vector_Aging': 1,
        'Adult_Life_Expectancy': 20,
        'x_Vector_Migration_Local': 0.01,  # scale factor to fix average # of trips per vector, per day
        'Vector_Migration_Filename_Local': 'vector_migration_local.bin',
        'Vector_Migration_Modifier_Equation': 'LINEAR',
        'Vector_Migration_Food_Modifier': 0,
        'Vector_Migration_Habitat_Modifier': 0,
        'Vector_Migration_Stay_Put_Modifier': 0,
        'x_Temporary_Larval_Habitat': 2,
    })

def manage_serialization(cb, serialize, pull_from_serialization, years, burnin='958bfb3d-caec-ec11-a9f9-b88303911bc1') :

    cb.update_params({
        "Serialized_Population_Reading_Type": 'NONE',
        'Serialization_Type': 'TIMESTEP',
        "Serialized_Population_Writing_Type": 'TIMESTEP',
        'Serialization_Mask_Node_Write': 0,
        'Serialization_Precision': 'REDUCED',
    })

    if serialize :
        years = 40
        cb.update_params({
            "Serialization_Time_Steps": [years * 365],
            "Serialized_Population_Writing_Type": 'TIMESTEP',
            "Serialized_Population_Reading_Type": 'NONE',
            "Enable_Random_Generator_From_Serialized_Population": 0,
            'Serialization_Precision': 'REDUCED',
        })

    if pull_from_serialization :
        expt = retrieve_experiment(burnin)
        output_paths = [sim.get_path() for sim in expt.simulations]
        cb.update_params({
            "Serialized_Population_Path": os.path.join(output_paths[0], 'output'),    #//internal.idm.ctr/IDM/Home/jgerardin/output/IH ITN Combinations_20220609_182333/74b/81a/562/74b81a56-21e8-ec11-a9f9-b88303911bc1/output',
            "Serialization_Mask_Node_Read": 0,
            'Serialized_Population_Filenames': ['state-14600.dtk'],
            "Serialized_Population_Reading_Type": 'READ',
            "Serialized_Population_Writing_Type": 'NONE',
            "Enable_Random_Generator_From_Serialized_Population": 0,
        })

    cb.update_params( {
        'Simulation_Duration' : 365*years,
        'Climate_Model' : 'CLIMATE_BY_DATA'
    })

def set_up_genetics(cb) :

    set_species(cb, ['gambiae'])

    genes = {"gambiae": [
            {
                "Alleles": {
                    "a0": 0.95,
                    "a1": 0.05
                },
                "Mutations": {
                    "a0:a1": 0.001,
                    "a1:a0": 0.00
                }
            },
            {
                "Alleles": {
                    "b0": 1.00,
                    "b1": 0.00
                },
                "Mutations": {
                    "b0:b1": 0.001,
                    "b1:b0": 0.00
                }
            },
            {
                "Alleles": {
                    "c0": 0.99,
                    "c1": 0.01
                },
                "Mutations": {
                    "c0:c1": 0.001,
                    "c1:c0": 0.00
                }
            }
        ]}
    for species, gene in genes.items():
        set_species_param(cb, species, 'Genes', gene)

    set_species_param(cb, 'gambiae', 'Indoor_Feeding_Fraction', 0.8)

    cb.add_reports(BaseVectorGeneticsReport(type='ReportVectorGenetics',
                                            species='gambiae',
                                            gender='VECTOR_FEMALE',
                                            include_vector_state_columns=0,
                                            stratify_by='ALLELE_FREQ'))

def set_up_insecticide(cb):

    cb.update_params({
        "Insecticides": [
            {
                "Name": "pyrethroid",
                "Resistances": [
                    {
                        "Allele_Combinations": [
                            [
                                "a1",
                                "a1"
                            ],
                        ],
                        "Blocking_Modifier": 1.0,
                        "Killing_Modifier": 0.4,
                        "Larval_Killing_Modifier": 0,
                        "Repelling_Modifier": 0,
                        "Species": "gambiae"
                    },
                    {
                        "Allele_Combinations": [
                            [
                                "a0",
                                "a1"
                            ],
                        ],
                        "Blocking_Modifier": 1.0,
                        "Killing_Modifier": 0.7,
                        "Larval_Killing_Modifier": 0,
                        "Repelling_Modifier": 0,
                        "Species": "gambiae"
                    },
                ]
            },
            {
                "Name": "pyrethroid-PBO",
                "Resistances": [
                    {
                        "Allele_Combinations": [
                            [
                                "c1",
                                "c1"
                            ],
                            [
                                "a1",
                                "a1"
                            ],
                        ],
                        "Blocking_Modifier": 1.0,
                        "Killing_Modifier": 0.3,
                        "Larval_Killing_Modifier": 0.02,
                        "Repelling_Modifier": 0.01,
                        "Species": "gambiae"
                    }
                ]
            },
            {
                "Name": "Interceptor G2",
                "Resistances": [
                    {
                        "Allele_Combinations": [
                            [
                                "a1",
                                "a1"
                            ],
                            [
                                "b1",
                                "b1"
                            ],
                        ],
                        "Blocking_Modifier": 1.0,
                        "Killing_Modifier": 0.2,  # killing modifier lower
                        "Larval_Killing_Modifier": 0.04,
                        "Repelling_Modifier": 0.03,
                        "Species": "gambiae"
                    }
                ]
            }
        ]
    })


def configure_ITN_scenario(cb, scenario, start_day=0, coverage=0.8, gap=3*365, biggap=6*365) :

    if scenario == 0 :
        scenario_name = 'No ITNs'
    elif scenario == 1 :
        scenario_name = 'ITN Rotation with no resistance'
        add_ITN(cb, start=start_day, coverage_by_ages=[{'min': 0, 'max': 100, 'coverage': coverage}])
        add_ITN(cb, start=3*365, coverage_by_ages=[{'min': 0, 'max': 100, 'coverage': coverage}])
        add_ITN(cb, start=6*365, coverage_by_ages=[{'min': 0, 'max': 100, 'coverage': coverage}])
        add_ITN(cb, start=9*365, coverage_by_ages=[{'min': 0, 'max': 100, 'coverage': coverage}])
    elif scenario == 2 :
        scenario_name = "Sequence of Pyrethroid and Pyrethroid-PBO"
        set_up_insecticide(cb)
        add_ITN_age_season(cb, start=start_day, demographic_coverage=0.8, age_dependence=None,
                           insecticide='pyrethroid')
        add_ITN_age_season(cb, start=6*365, demographic_coverage=0.8, age_dependence=None,
                           insecticide='pyrethroid-PBO')
    elif scenario == 3 :
        scenario_name = "Sequence of Pyrethroid and IG2"
        set_up_insecticide(cb)
        add_ITN_age_season(cb, start=start_day, demographic_coverage=0.8, age_dependence=None,
                           insecticide='pyrethroid')
        add_ITN_age_season(cb, start=6*365, demographic_coverage=0.8, age_dependence=None,
                           insecticide='Interceptor G2')
    elif scenario == 4 :
        scenario_name = "Rotation of Pyrethroid and Pyrethroid-PBO"
        set_up_insecticide(cb)
        add_ITN_age_season(cb, start=start_day, demographic_coverage=0.8, age_dependence=None,
                           insecticide='pyrethroid')
        add_ITN_age_season(cb, start=start_day + gap, demographic_coverage=0.8, age_dependence=None,
                           insecticide='pyrethroid-PBO')
        add_ITN_age_season(cb, start=6*365, demographic_coverage=0.8, age_dependence=None,
                           insecticide='pyrethroid')
        add_ITN_age_season(cb, start=9*365, demographic_coverage=0.8, age_dependence=None,
                           insecticide='pyrethroid-PBO')
    elif scenario == 5 :
        scenario_name = 'Rotation of Pyrethroid and IG2'
        set_up_insecticide(cb)
        add_ITN_age_season(cb, start=start_day, demographic_coverage=0.8, age_dependence=None,
                           insecticide='pyrethroid')
        add_ITN_age_season(cb, start=start_day + gap, demographic_coverage=0.8, age_dependence=None,
                           insecticide='Interceptor G2')
        add_ITN_age_season(cb, start=start_day + biggap, demographic_coverage=0.8, age_dependence=None,
                           insecticide='pyrethroid')
        add_ITN_age_season(cb, start=9*365, demographic_coverage=0.8, age_dependence=None,
                           insecticide='Interceptor G2')
    elif scenario == 6 :
        scenario_name = 'Mosaic of Pyrethroid and Pyrethroid-PBO'
        set_up_insecticide(cb)
        add_ITN_age_season(cb, start=start_day, demographic_coverage=0.8, age_dependence=None,
                           ind_property_restrictions=[{"InterventionStatus":"Pyrethroid"}],
                           insecticide='pyrethroid')
        add_ITN_age_season(cb, start=start_day, demographic_coverage=0.8, age_dependence=None,
                           ind_property_restrictions=[{"InterventionStatus":"Pyrethroid-PBO"}],
                           insecticide='pyrethroid-PBO')
    elif scenario == 7 :
        scenario_name = 'Mosaic of Pyrethroid and IG2'
        set_up_insecticide(cb)
        add_ITN_age_season(cb, start=start_day, demographic_coverage=0.8, age_dependence=None,
                           ind_property_restrictions=[{"Accessibility":"Pyrethroid"}],
                           insecticide='pyrethroid')
        add_ITN_age_season(cb, start=start_day, demographic_coverage=0.8, age_dependence=None,
                           ind_property_restrictions=[{"Accessibility":"Interceptor G2"}],
                           insecticide='Interceptor G2')
    elif scenario == 8 :
        scenario_name = 'Interceptor G2 Rotation'
        set_up_insecticide(cb)
        add_ITN_age_season(cb, start=start_day, demographic_coverage=0.8, age_dependence=None,
                           insecticide='Interceptor G2')
        add_ITN_age_season(cb, start=start_day + gap, demographic_coverage=0.8, age_dependence=None,
                           insecticide='Interceptor G2')
        add_ITN_age_season(cb, start=6*365, demographic_coverage=0.8, age_dependence=None,
                           insecticide='Interceptor G2')
        add_ITN_age_season(cb, start=9*365, demographic_coverage=0.8, age_dependence=None,
                           insecticide='Interceptor G2')
    elif scenario == 9 :
        scenario_name = 'Pyrethroid Rotation'
        set_up_insecticide(cb)
        add_ITN_age_season(cb, start=start_day, demographic_coverage=0.8, age_dependence=None,
                           insecticide='pyrethroid')
        add_ITN_age_season(cb, start=start_day + gap, demographic_coverage=0.8, age_dependence=None,
                           insecticide='pyrethroid')
        add_ITN_age_season(cb, start=6 * 365, demographic_coverage=0.8, age_dependence=None,
                           insecticide='pyrethroid')
        add_ITN_age_season(cb, start=9 * 365, demographic_coverage=0.8, age_dependence=None,
                           insecticide='pyrethroid')
    else :
        scenario_name = 'scenario not found'
    return {'ITN_coverage' : coverage,
            'scenario' : scenario_name}


if __name__ == "__main__":
    SetupParser.default_block = 'HPC'
    SetupParser.init()

    exp_name = 'IH ITN Combinations'
    numseeds = 3
    years = 10
    serialize = False
    pull_from_serialization = True
    burnin = '958bfb3d-caec-ec11-a9f9-b88303911bc1'

    cb = DTKConfigBuilder.from_defaults('MALARIA_SIM')
    manage_serialization(cb, serialize=serialize, pull_from_serialization=pull_from_serialization,
                         years=years, burnin=burnin)

    set_up_genetics(cb)
    setup_simulation(cb)

    cb.update_params({
        'logLevel_SusceptibilityMalaria' : 'ERROR'
    })


    input_file_name = '9node'
    cb.update_params(
        {"Air_Temperature_Filename": os.path.join(input_file_name, '%s_air_temperature_daily.bin' % input_file_name),
         "Land_Temperature_Filename": os.path.join(input_file_name, '%s_air_temperature_daily.bin' % input_file_name),
         "Rainfall_Filename": os.path.join(input_file_name, '%s_rainfall_daily.bin' % input_file_name),
         "Relative_Humidity_Filename": os.path.join(input_file_name, '%s_relative_humidity_daily.bin' % input_file_name)
         })

    cb.update_params({'Vector_Sampling_Type': 'VECTOR_COMPARTMENTS_NUMBER'  # to get number of vectors moving
                      })
    #add_vector_migration_report(cb)

    if not serialize:
        builder = ModBuilder.from_list([[ModFn(DTKConfigBuilder.set_param, 'Run_Number', seed),
                                         ModFn(configure_ITN_scenario, scenario=scenario, start_day=0, coverage=0.8)
                                        ]
                                        for seed in range(numseeds)
                                        for scenario in range(10)])
        run_sim_args = {
            'exp_name': exp_name,
            'config_builder': cb,
            'exp_builder': builder
        }

    else :
        run_sim_args = {
            'exp_name': exp_name,
            'config_builder': cb,
        }

    # exit(0)
    exp_manager = ExperimentManagerFactory.init()
    exp_manager.run_simulations(**run_sim_args)
    # Wait for the simulations to be done
    exp_manager.wait_for_finished(verbose=True)
    assert (exp_manager.succeeded())


import json
from dtk.tools.demographics.DemographicsGenerator import DemographicsGenerator
import os
import pandas as pd
from dtk.tools.demographics.DemographicsGeneratorConcern import DefaultIndividualAttributesConcern
from input_file_generation.convert_txt_to_bin import convert_txt_to_bin

# working_dir = 'C:\hunagi\Documents\insecticide-resistance'
#
user_path = os.path.expanduser('~')
home_path = os.path.join(user_path, 'Box', 'NU-malaria-team')
data_path = os.path.join(home_path, 'insecticide_resistance')
project_path = os.path.join(home_path, 'projects', 'insecticide_resistance')

inputs_path = os.path.join(project_path,'simulation_input')
#'C:\hunagi\Documents\insecticide-resistance'
    #os.path.join(working_dir, 'demographics.csv')

# def generate_demographics(demo_df, demo_fname) :
#     chain = [
#         DefaultIndividualAttributesConcern(),
#     ]
#     current = DemographicsGenerator.from_dataframe(demo_df,
#                                                    population_column_name='population',
#                                                    nodeid_column_name='nodeid',
#                                                    latitude_column_name='lat',
#                                                    longitude_column_name='long',
#                                                    node_id_from_lat_long=False,
#                                                    concerns=chain,
#                                                    load_other_columns_as_attributes=False)
#     with open(demo_fname, 'w') as fout:
#         json.dump(current, fout, sort_keys=True, indent=4, separators=(',', ': '))
#
# df = pd.read_csv(os.path.join(inputs_path,'demographics.csv'))
# demo_fname = os.path.join(inputs_path, 'demographics.json')
# generate_demographics(df, demo_fname)


demo_fname = "C:/Users/hunagi/OneDrive - Nexus365/insecticide_resistance/simulation_input/demographics.json"
with open(demo_fname) as fin:
    demo = json.loads(fin.read())
id_reference = demo['Metadata']['IdReference']

os.chdir('C:/Users/hunagi/OneDrive - Nexus365/insecticide_resistance/simulation_input')
convert_txt_to_bin('vector_migration_local.csv',
                   'vector_migration_local.bin',
                   mig_type='LOCAL_MIGRATION',
                   id_reference=id_reference)










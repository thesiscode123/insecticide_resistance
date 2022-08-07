from dtk.tools.climate.ClimateGenerator import ClimateGenerator
from simtools.SetupParser import SetupParser
import os

user_path = os.path.expanduser('~')
home_path = os.path.join(user_path, 'Documents')
data_path = os.path.join(home_path, 'insecticide-resistance')

def generate_climate(demo_fname, input_file_name):
    if not SetupParser.initialized:
        SetupParser.init('HPC')

    cg = ClimateGenerator(demographics_file_path=demo_fname, work_order_path='./wo.json',
                          climate_files_output_path=os.path.join(inputs_path, input_file_name),
                          climate_project='IDM-Tanzania',
                          start_year='2016', num_years='1')
    cg.generate_climate_files()


# Point to existing demographics file
inputs_path = os.path.join(data_path)  # Modify PROJECTPATH
input_file_name = '9node'  # Modify FILENAME
demo_fname = os.path.join(inputs_path, 'demographics.json')


# Generate climate files from selected project
generate_climate(demo_fname, input_file_name)

# Rename climate files and metadata
for tag in ['air_temperature', 'rainfall', 'relative_humidity']:
    os.replace(os.path.join(inputs_path, input_file_name, 'Tanzania_30arcsec_%s_daily.bin' % tag),
               os.path.join(inputs_path, input_file_name, '%s_%s_daily.bin' % (input_file_name, tag)))
    os.replace(os.path.join(inputs_path, input_file_name, 'Tanzania_30arcsec_%s_daily.bin.json' % tag),
               os.path.join(inputs_path, input_file_name, '%s_%s_daily.bin.json' % (input_file_name, tag)))
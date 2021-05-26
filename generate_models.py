#!/usr/bin/env python3

import os
import shutil
import subprocess
from pathlib import Path
import glob

ROOT_PATH = Path()
FHIR_PARSER_PATH = ROOT_PATH / 'fhir-parser'
MAPPINGS_FILE = 'mappings.py'
SETTINGS_FILE = 'settings.py'
GENERATE_PATH = FHIR_PARSER_PATH/'generate'
SAMPLE_PATH = FHIR_PARSER_PATH/'Sample'

# TODO: I'm following the instructions of the fhir-parser readme on how to integrate fhir parser into the project.
#  However, this approach makes for a very confusing package structure, especially now we're calling the fhirspec
#  module directly instead of running generate.py. Think about integrating fhir-parser in a cleaner way.
def main():
    # Copy mappings and settings to fhir-parser submodule
    shutil.copy(ROOT_PATH / MAPPINGS_FILE, FHIR_PARSER_PATH / MAPPINGS_FILE)
    shutil.copy(ROOT_PATH / SETTINGS_FILE, FHIR_PARSER_PATH / SETTINGS_FILE)
    GENERATE_PATH.mkdir(exist_ok=True)

    template_files = glob.glob(rf'{str(SAMPLE_PATH)}/template-*')
    for f in template_files:
        shutil.copy(f, GENERATE_PATH)

    os.chdir(FHIR_PARSER_PATH)


    subprocess.run('./generate.py')


if __name__ == '__main__':
    main()

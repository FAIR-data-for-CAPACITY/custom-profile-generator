#!/usr/bin/env python3

import os
import shutil
import subprocess
from pathlib import Path
import glob
from urllib import request
from zipfile import ZipFile
import generate

ROOT_PATH = Path()
FHIR_PARSER_PATH = ROOT_PATH / 'fhir-parser'
MAPPINGS_FILE = 'mappings.py'
SETTINGS_FILE = 'settings.py'
GENERATE_PATH = FHIR_PARSER_PATH / 'generate'
SAMPLE_PATH = FHIR_PARSER_PATH / 'Sample'
DOWNLOADS_PATH = FHIR_PARSER_PATH / 'downloads'


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

    generate.main()


def retrieve_definitions(definitions_url):
    archive_name = definitions_url.split('/')[-1]

    # Remove ".zip" to get base name
    base_name = archive_name[:-4]

    cache_dir = Path(DOWNLOADS_PATH)
    print(cache_dir.absolute())
    archive_path = cache_dir / archive_name
    zip_target_path = cache_dir / base_name
    cache_dir.mkdir(exist_ok=True)
    retrieve_archive(archive_path, definitions_url)
    unpack_archive(archive_path, zip_target_path)

    yield from zip_target_path.iterdir()


def retrieve_archive(archive_path, definitions_url):
    if not archive_path.exists():
        print('Downloading definitions...')
        request.urlretrieve(definitions_url, str(archive_path))
        print('Done.')


def unpack_archive(archive_path, zip_target_path):
    # Unpack spec
    print('Unpacking definitions...')
    with ZipFile(archive_path, 'r') as z:
        z.extractall(str(zip_target_path))
    print('Done.')


if __name__ == '__main__':
    main()

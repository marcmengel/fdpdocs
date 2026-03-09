# Using MetaCat

This document describes how to set up and get started with MetaCat for FDP. The general MetaCat documentation can be found [here](https://fermitools.github.io/metacat/index.html).

## Prerequisites

1. Obtain access to amsc VO.  <!-- add link to documentation on getting added to amsc vo once it exists -->
1. Set up the software environment.

Create a python environment.

    python3 -m venv ~/.venv/metacat

Create a script called `activate-metacat.sh` that activates the environment and sets the required environment variables with the following contents:

    #!/usr/bin/env bash
    source ~/.venv/metacat/bin/activate
    export METACAT_SERVER_URL="https://metacat.fnal.gov:9443/amsc_meta_prod/app"
    export METACAT_AUTH_SERVER_URL="https://metacat.fnal.gov:8143/auth/amsc"

Note that these instructions assume a bash-compatible shell. If you are using another shell, run the script using bash.

Activate the environment and install the metacat client and htgettoken packages:

    source activate-metacat.sh
    pip install metacat-client
    pip install htgettoken

Every time you want to use MetaCat, do

    source activate-metacat.sh

When you're done using MetaCat,

    deactivate

## Login to MetaCat

To login to MetaCat:

    htgettoken -i amsc -a htvaultprod.fnal.gov
    metacat auth login -m token <username>

The first time, and occasionally after, doing the htgettoken step, the command will prompt you to login using your web browser. Follow the instructions as prompted.

Now you are ready to use any metacat commands. Test with

    metacat version

This should show something like 

    MetaCat Server URL:         https://metacat.fnal.gov:9443/amsc_meta_prod/app
    Authentication server URL:  https://metacat.fnal.gov:8143/auth/amsc
    Server version:             4.1.4
    Client version:             4.1.4

## Metadata format

MetaCat requires all metadata field names to be of the format

    <category>.<name>
    <category>.<subcategory>.<name>
    etc

See more details in the [MetaCat documentation](https://fermitools.github.io/metacat/concepts.html#file-attributes)

## Example scripts

1. Generating metadata in MetaCat format

    [This script](https://github.com/FNAL-SCD/fdpdocs/examples/generate_metadata.py) generates metadata for files in a given directory in the format required by MetaCat.

        python generate_metadata.py --data-directory /path/to/dataset --extension .h5 --namespace my_namespace --outfile metadata.json

    The extension and outfile are optional arguments. If not given an extension, it will use everything in the given directory. If not given an output file, it will write the metadata to `data-directory/metadata/metadata.json`.

    This script can be modified to add any additional metadata as desired.

1. Declaring metadata to MetaCat and adding it to a dataset. Also creates a namespace and dataset if they do not already exist.

    [This script](https://github.com/FNAL-SCD/fdpdocs/examples/declare_to_metacat.py) declares files to MetaCat.

        python declare_to_metacat.py --dataset my_dataset --namespace my_namespace --metadatafile metadata.json

    It creates the namespace and dataset if they do not already exist, and uses the metadata file that was created by generate_metadata.py, which must be a .json file.

1. Updating metadata that has already been declared to MetaCat.



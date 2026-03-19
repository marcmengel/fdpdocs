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

The web interface is here: https://metacat.fnal.gov:9443/amsc_meta_prod/app/gui

To login to MetaCat via the command line:

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

### MetaCat requirements

MetaCat requires all metadata field names to be of the format

    <category>.<name>
    <category>.<subcategory>.<name>
    etc

See more details in the [MetaCat documentation](https://fermitools.github.io/metacat/concepts.html#file-attributes)

### AmSC catalog requirements

There are some metadata fields that are required by the central AmSC catalog.

The following fields need to be included for both datasets and files:

    AmSC.common.type
    AmSC.common.description
    AmSC.common.location

For datasets, the `AmSC.common.type` is `scientificWork` and for files, the `AmSC.common.type` is `artifact`.

There are additional optional metadata fields that can be included in the central AmSC catalog:

    AmSC.common.display_name

For now only the above fields are used by the central AmSC data catalog. If you would like any other information to appear there, you can add it in the description field.

## Example scripts

1. Generating metadata in MetaCat format

    [This script](https://github.com/FNAL-SCD/fdpdocs/blob/main/examples/generate_metadata.py) generates metadata for files in a local directory in the format required by MetaCat, while
    [this one](https://github.com/FNAL-SCD/fdpdocs/blob/main/examples/generate_remote_metadata.py) generates metadata for files already uploaded to amsc.fnal.gov DCache.

    It takes a directory where the data files are located and extracts information such as the name, size, and checksum of each file. It also includes the metadata fields required by the central AmSC catalog. You can modify the script to add extra metadata fields as desired. The output is a json file that can be used to declare the files to MetaCat. The usage is as follows:

        python generate_metadata.py --data-directory /path/to/dataset --extension .ext --namespace my_namespace --dataset my_dataset --outfile metadata.json

    The extension and outfile are optional arguments. If not given an extension, it will use everything in the given directory. If not given an output file, it will write the metadata to `data-directory/metadata/metadata.json`.

    An example of running this script:

        python generate_metadata.py --data-directory /amsc/cms/aoj/data/ --extension .h5 --namespace cms --dataset aoj --outfile aoj_metadata.json

    Example json output looks like this:

        [
            {
                "namespace": "cms",
                "name": "RunG_batch0.h5",
                "size": 2379411451,
                "checksums": {
                    "sha256": "c2058846a224b1a915d65e89cec6eb9586db780eab6e83b1822ff5c22f63e143"
                },
                "metadata": {
                    "AmSC.common.type": "artifact",
                    "AmSC.common.description": "This is a file from the aoj dataset",
                    "AmSC.common.location": "https://amsc.fnal.gov:2880/amsc/cms/aoj/data/RunG_batch0.h5",
                    "fn.path": "/amsc/cms/aoj/data/RunG_batch0.h5",
                    "fn.locations": [
                        "https://amsc.fnal.gov:2880/amsc/cms/aoj/data/RunG_batch0.h5",
                        "root://amsc.fnal.gov/amsc/cms/aoj/data/RunG_batch0.h5"
                    ]
                }
            },
            {
                "namespace": "cms",
                "name": "RunG_batch1.h5",
                "size": 2478381156,
                "checksums": {
                    "sha256": "72f0ba03a4b50e3cd415fc65ba934adc10c18095eee20db7fc185e167fab71fb"
                },
                "metadata": {
                    "AmSC.common.type": "artifact",
                    "AmSC.common.description": "This is a file from the aoj dataset",
                    "AmSC.common.location": "https://amsc.fnal.gov:2880/amsc/cms/aoj/data/RunG_batch1.h5",
                    "fn.path": "/amsc/cms/aoj/data/RunG_batch1.h5",
                    "fn.locations": [
                        "https://amsc.fnal.gov:2880/amsc/cms/aoj/data/RunG_batch1.h5",
                        "root://amsc.fnal.gov/amsc/cms/aoj/data/RunG_batch1.h5"
                    ]
                }
            },
            ...

1. Declaring metadata to MetaCat and adding it to a dataset. Also creates a namespace and dataset if they do not already exist.

    [This script](https://github.com/FNAL-SCD/fdpdocs/blob/main/examples/declare_to_metacat.py) declares files to MetaCat.

    It takes the json file generated from `generate_metadata.py` and adds the files to MetaCat. You can also include a json file that contains metadata about the dataset itself. The usage is as follows:

        python declare_to_metacat.py --dataset my_dataset --namespace my_namespace --metadatafile metadata.json --datasetmetadata ds_metadata.json

    It creates the namespace and dataset if they do not already exist, and uses the metadata file that was created by generate_metadata.py, which must be a .json file.

    An example of running this script:

        python declare_to_metacat.py --dataset aoj --namespace cms --metadatafile aoj_metadata.json

    After running it, you should be able to see the namespace, dataset, and files in MetaCat.

1. Updating metadata that has already been declared to MetaCat.

    [This script](https://github.com/FNAL-SCD/fdpdocs/blob/main/examples/update_metadata.py) updates the metadata in MetaCat from a given json file.

    It takes as input a json file with updated metadata fields and updates the file metadata in MetaCat. The usage is as follows:

        python update_metadata.py --inputfile updated_metadata.json

    After running this script, you should be able to see the updated metadata in MetaCat.


import json
import subprocess
import logging
import argparse
from metacat.webapi import MetaCatClient

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize metacat client
client = MetaCatClient("https://metacat.fnal.gov:9443/amsc_meta_prod/app")

# create namespace if it does not already exist
def metacat_namespace(name):
    # check if namespace already exists
    ns = client.get_namespace(name)
    if ns is not None:
        logger.info(f"Namespace {name} already exists, skipping creation")
    else:
        # create the namespace
        result = client.create_namespace(name)
        logger.info(result)

# create dataset if it does not already exist
def metacat_dataset(name, ns, dsmdfile):
    # check if dataset already exists
    did = ns+":"+name
    ds = client.get_dataset(did)
    if ds is not None:
        logger.info(f"Dataset {name} already exists, skipping creation")
    else:
        # create the dataset
        with open(dsmdfile, "r") as f:
            dsmd = json.load(f)
        result = client.create_dataset(did, metadata=dsmd)
        logger.info(result)

# declare the files from the metadata file and add them to metacat; returns the number of files added
def metacat_declare_add(dataset, batchfile, ns):
    with open(batchfile, "r") as f:
        files = json.load(f)
    did = ns+":"+dataset
    result = client.declare_files(did, files, namespace=ns)
    result2 = client.add_files(did, files, namespace=ns)
    return len(files)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", "-d", required=True, help="MetaCat dataset where metadata will be added")
    parser.add_argument("--namespace", "-n", required=True, help="MetaCat namespace where metadata will be added")
    parser.add_argument("--metadatafile", "-m", required=True, help="Name of the json file that contains the generated metadata")
    parser.add_argument("--datasetmetadata", "-s", required=False, help="Name of the json file that contains metadata fields for the dataset.")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

    namespace = args.namespace
    dataset = args.dataset
    batchfile = args.metadatafile
    dsmdfile = args.datasetmetadata

    # creates the namespace and dataset and adds the files to metacat
    logging.info("Creating namespace and dataset")
    metacat_namespace(namespace)
    metacat_dataset(dataset, namespace, dsmdfile)
    logging.info("Declaring and adding files to dataset")
    num_files = metacat_declare_add(dataset, batchfile, namespace)
    logging.info(f"Added {num_files} to dataset {dataset}")


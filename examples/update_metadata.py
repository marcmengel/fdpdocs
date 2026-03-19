import json
import subprocess
import logging
import argparse
from metacat.webapi import MetaCatClient

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize metacat client
client = MetaCatClient("https://metacat.fnal.gov:9443/amsc_meta_prod/app")

# update the file metadata
def metacat_update_file(namespace, filename, metadata):
    ns = client.get_namespace(namespace)
    if ns is None:
        logger.info(f"Namespace {name} does not exist")
    file = client.get_file(filename, namespace, with_metadata=False)
    if file is None:
        logger.info(f"File {filename} does not exist")
    did = namespace+":"+filename
    client.update_file(did, replace=False, metadata=metadata)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument("--dataset", "-d", required=True, help="MetaCat dataset where metadata will be added")
    #parser.add_argument("--namespace", "-n", required=True, help="MetaCat namespace where metadata will be added")
    parser.add_argument("--inputfile", "-i", required=True, help="Name of the json file that contains the updated metadata")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

    #namespace = args.namespace
    #dataset = args.dataset
    inputfile = args.inputfile

    with open(inputfile, "r") as f:
        mdfile = json.load(f)

    # update the metadata with the information from the file
    counter = 0
    for item in mdfile:
        namespace = item["namespace"]
        filename = item["name"]
        metadata = item["metadata"]
        result = metacat_update_file(namespace, filename, metadata)
        counter += 1

    logging.info(f"Updated {counter} files")


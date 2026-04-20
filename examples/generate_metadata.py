import json
import logging
import argparse
import os
import zlib
import glob

# Initialize logger
logger = logging.getLogger(__name__)

def nsubdirs(n, path):
    rl = []
    for i in range(n):
        path = os.path.dirname(path)
        rl.insert(0,os.path.basename(path))
    if rl:
        return "/".join(rl) + "/"
    else:
        return ""

# Generate file checksum
def checksum(filepath):
    adler = 1
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            adler = zlib.adler32(chunk, adler)
    return f"{adler:08x}"

# Look up the uuid of the corresponding globus collection to add to the globus location
def globus_uuid(namespace):
    if namespace=="dune":
        uuid = "5ba77b68-8077-454f-b126-2c5567645e88"
    else:
        uuid = "b35955d3-14d1-4aab-a1c9-189989f7d8d0"
    return uuid

# Generate metadata in metacat format
def generate_metadata(namespace, dsname, filename, directory):
    # basic file metadata required for metacat
    filepath = os.path.join(directory, os.path.basename(filename))
    filesize = os.path.getsize(filepath)
    chksm = checksum(filepath)
    checksum_dict = {"adler32": chksm}

    # globus collection uuid
    uuid = globus_uuid(namespace)

    # file metadata required for amsc
    description = f"This is a file from the {dsname} dataset"
    # add list of locations where file can be accessed
    webdav_url = "https://amsc.fnal.gov:2880"+filepath
    xrootd_url = "root://amsc.fnal.gov"+filepath
    globus_loc = f"globus://{uuid}"+filepath
    file_locations = [webdav_url, xrootd_url, globus_loc]

    # create the metadata dictionary
    md = {
        "name": filename,
        "namespace": namespace,
        "size": filesize,
        "checksums": checksum_dict,
        "metadata" : {
            "AmSC.common.type" : "artifact",
            "AmSC.common.description" : description,
            "AmSC.common.location" : webdav_url,

            # insert your own metadata here

            "fn.path" : filepath,
            "fn.locations" : file_locations
        }
    }

    # return the metadata dictionary
    return md
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-directory", "-d", required=True, help="Directory containing data files that need metadata generated (required)")
    parser.add_argument("--extension", "-e", help="Extension of data files that need metadata generated. If not provided, all files in data-directory are used.")
    parser.add_argument("--namespace", "-n", required=True, help="MetaCat namespace where metadata will be added (required)")
    parser.add_argument("--dataset", "-s", required=True, help="Name of the MetaCat dataset where metadata will be added (required)")
    parser.add_argument("--outfile", "-o", help="Name of the json file to contain the generated metadata. If not provided, it will be written to data-directory/metadata/metadata.json")
    parser.add_argument("--nsubdirs", "-N", help="Number of subdirectories to include in name for uniqueness", type=int, default=0)
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

    directory = args.data_directory
    extension = args.extension
    namespace = args.namespace
    dsname = args.dataset
    outfile = args.outfile
    
    # handle input arguments
    if extension and extension[0] != ".":
        extension = "." + extension

    if outfile is None:
        outfile = directory + "metadata/metadata.json"
        # create metadata directory if it doesn't already exist
        metadatadir = os.path.join(directory, "metadata")
        os.makedirs(metadatadir, exist_ok=True)

    # generate the metadata files
    if extension:
        pattern = os.path.join(directory, f"*{extension}")
    else:
        pattern = os.path.join(directory, "*")
    files = glob.glob(pattern)
    num_files = len(files)
    logger.info(f"Generating metadata for {num_files} files")

    md = []
    for file in files:
        filename = nsubdirs(args.nsubdirs, file ) + os.path.basename(file)
        try:
            file_metadata = generate_metadata(namespace, dsname, filename, directory)
        except IsADirectoryError:
            continue
        md.append(file_metadata)

    # write the metadata to json file
    with open(outfile, "w") as f:
        json.dump(md, f, indent=4)

    logger.info(f"Wrote metadata file {outfile}")



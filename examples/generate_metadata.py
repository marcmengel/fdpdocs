import json
import logging
import argparse
import os
import hashlib
import glob

# Initialize logger
logger = logging.getLogger(__name__)

# Generate file checksum
def checksum(filepath):
    hash_func = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

# Generate metadata in metacat format
def generate_metadata(namespace, filename, directory):
    # basic file metadata required for metacat
    filepath = os.path.join(directory, filename)
    filesize = os.path.getsize(filepath)
    chksm = checksum(filepath)
    checksum_dict = {"sha256": chksm}

    # add list of locations where file can be accessed
    webdav_url = "https://amsc.fnal.gov:2880"+filepath
    xrootd_url = "root://amsc.fnal.gov"+filepath
    file_locations = [webdav_url, xrootd_url]

    # return the metadata dictionary
    return {
        "namespace": namespace,
        "name": filename,
        "size": filesize,
        "checksums": checksum_dict,
        "metadata" : {
            "fn.path" : filepath,
            "fn.location" : file_locations
        }
    }
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-directory", "-d", required=True, help="Directory containing data files that need metadata generated (required)")
    parser.add_argument("--extension", "-e", help="Extension of data files that need metadata generated. If not provided, all files in data-directory are used.")
    parser.add_argument("--namespace", "-n", required=True, help="MetaCat namespace where metadata will be added (required)")
    parser.add_argument("--outfile", "-o", help="Name of the json file to contain the generated metadata. If not provided, it will be written to data-directory/metadata/metadata.json")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

    directory = args.data_directory
    extension = args.extension
    namespace = args.namespace
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
        filename = os.path.basename(file)
        file_metadata = generate_metadata(namespace, filename, directory)
        md.append(file_metadata)

    # write the metadata to json file
    with open(outfile, "w") as f:
        json.dump(md, f, indent=4)

    logger.info(f"Wrote metadata file {outfile}")



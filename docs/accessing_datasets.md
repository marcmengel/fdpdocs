# Accessing Datasets on Fermi Data Platform 

FDP supports data access utilizing the following protocols:

* HTTP(s)/WebDAV
* XRootD
* Globus
* NFS (for local access)

The data is organized in hierarchical directory tree structure with parts of the tree
publicly accessible for reads. All write access  and read access to some parts of the tree 
requires authentication and authorization. 

## Authentication and Authorization

To allow authorized access to the data  FDP utilizes OpenID Connect (OIDC) authentication
protocol within overall authorization flow  implemented using Oauth2 authorization framework. 

## Globus 

To access the data, the user needs to be mapped to an account on the server. This is currently a manual process done on a case-by-case basis. 

### From globus.org

https://www.globus.org/ 

Log in with Fermilab credentials 

Search for the “Fermi Data Platform” collection 

The data is under the `/amsc` directory 

### From the command line: 

    globus transfer [source-endpoint-ID]:[/path/to/source] [destination-ID]:[/path/to/destination] 

The Fermi Data Platform endpoint ID is `b35955d3-14d1-4aab-a1c9-189989f7d8d0` and the path is `/amsc` 

## Https/WebDAV

### Download public data using browser

https://amsc.fnal.gov:2880/amsc 

Allows to browse and download publicly available data. 


### Download public data to local host using curl

    curl -s -f –L https://amsc.fnal.gov:2880/[source_path] -o [destination_path] 

The `source_path` is the path to the data on amsc 

### Download public data to local host using gfal

Using gfal, which requires the `gfal2-*` packages: 

    gfal-ls https://amsc.fnal.gov:2880/amsc 

    gfal-copy https://amsc.fnal.gov:2880/amsc/[source_path] [destination_path]

### Download project specific data requiring authorization using curl

Below is an example of using OIDC token authirized to access dune project directories for read:

    htgettoken -a htvaultprod.fnal.gov -i amsc -r duneread 
    export BEARER_TOKEN=$(< $XDG_RUNTIME_DIR/bt_u$(id -u))
    curl -f -L -s -H "Authorization: Bearer ${BEARER_TOKEN}" https://amsc.fnal.gov:2880/[source_path] -o [destination_path]

### Download project specific data requiring authorization using gfal

Below is an example of using OIDC token authirized to access dune project directories for read:

    htgettoken -a htvaultprod.fnal.gov -i amsc -r duneread 
    export BEARER_TOKEN=$(< $XDG_RUNTIME_DIR/bt_u$(id -u))
    gfal-copy https://amsc.fnal.gov:2880/[source_path] [destination_path]

### Upload data from local host using curl

Below is an example of using OIDC token to upload data to FDP using dunewrite role:

    htgettoken -a htvaultprod.fnal.gov -i amsc -r dunewrite
    export BEARER_TOKEN=$(< $XDG_RUNTIME_DIR/bt_u$(id -u))
    curl -f -L -s -H "Authorization: Bearer ${BEARER_TOKEN}"  -T[source_path]  https://amsc.fnal.gov:2880/[destination_path]

### Upload data from local host using gfal

Below is an example of using OIDC token to upload data to FDP using dunewrite role:

    htgettoken -a htvaultprod.fnal.gov -i amsc -r dunewrite
    export BEARER_TOKEN=$(< $XDG_RUNTIME_DIR/bt_u$(id -u))
    gfal-copy [source_path]  https://amsc.fnal.gov:2880/[destination_path]

### Copy data from public dCache to FDP

    htgettoken -a htvaultprod.fnal.gov -i dune
    export TOKEN_SRC=$(< $XDG_RUNTIME_DIR/bt_u$(id -u))

    htgettoken -a htvaultprod.fnal.gov -i amsc -r dunewrite
    export TOKEN_DST=$(< $XDG_RUNTIME_DIR/bt_u$(id -u))

PULL mode copy:
    
    curl -s --capath /etc/grid-security/certificates -L -X COPY \
          -H 'Secure-Redirection: 1' -H 'X-No-Delegate: 1' -H 'Credential: none' \
          -H "Authorization: Bearer $TOKEN_DST" -H "TransferHeaderAuthorization: Bearer $TOKEN_SRC" \
          -H "Source: https://fndcadoor.fnal.gov:2880/[source_path]" https://amsc.fnal.gov:2880/[destination_path]

PUSH mode copy:

    curl -s --capath /etc/grid-security/certificates -L -X COPY \
          -H 'Secure-Redirection: 1' -H 'X-No-Delegate: 1' -H 'Credential: none' \ 
          -H "Authorization: Bearer $TOKEN_SRC" -H "TransferHeaderAuthorization: Bearer $TOKEN_DST" \
          -H "Destination: https://amsc.fnal.gov:2880/[destinaion_path]"  https://fndcadoor.fnal.gov:2880/[source_path] 
 
## XRootD 

Requires the `xrootd-client` package 

From the command line: 

Copy a file: 

    xrdcp root://amsc.fnal.gov/[source_path] [destination_path] 

List a directory: 

    xrdfs root://amsc.fnal.gov ls –l /amsc 

Using gfal, which requires the `gfal2-*` packages: 

    gfal-ls root://amsc.fnal.gov/amsc 

    gfal-copy root://amsc.fnal.gov/amsc/[source_path] [destintation_path] 


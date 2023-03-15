# Web API gap analysis

![GitHub release (latest by date)](https://img.shields.io/github/v/release/CIAT-DAPA/spcat_webapi) ![](https://img.shields.io/github/v/tag/CIAT-DAPA/spcat_webapi)

This repository is a web API developed in Python which is responsible for collecting information from the gap database. It contains the endpoints that will be in charge of obtaining the data of countries, crops and accessions, the get crops endpoint is in charge of obtaining the information of crops, the get countries endpoint is in charge of obtaining the information of countries and the get accessions endpoint is in charge of obtaining all the information of accessions.

**Important notes**

This web api must be used in conjunction with the ORM that was developed for the project, which you can find in this [repository](https://github.com/CIAT-DAPA/spcat_orm).

## Getting Started

To use the wep api, it is necessary to have an instance of MongoDB running, either locally or on a server that is accessible from the internet.

### Prerequisites

- Python 3.x
- MongoDB

## Installation

To use the wep api, it is necessary to have an instance of MongoDB running. It is also recommended to create a virtual environment to work with this project and make sure that the dependencies are installed in the virtual environment instead of the global system.

1. Clone the repository
````sh
git clone https://github.com/CIAT-DAPA/spcat_webapi.git
````

2. Create a virtual environment
````sh
python -m venv env
````

3. Activate the virtual environment
- Linux
````sh
source env/bin/activate
````
- windows
````sh
env\Scripts\activate.bat
````

4. Install the required packages

````sh
pip install -r requirements.txt
````

## Usage

### Configuration

The parameters to be configured are found in the `config.py` file. This file has information on how to connect to the database, when deploying the web api on a production server these data must be configured as environment variables. Let's see what it has:

| Parameter     |type   | Description|
|---------------|-------|------------|
|DEBUG          |boolean|boolean that defines whether you are in a test environment or in production.|
|HOST           |string |IP or hostname of the server in which is the wep api. By default is: 0.0.0.0|
|PORT           |string |Port in which is available the wep api in the server. By default is: 5000   |
|CONNECTION_DB  |string |utl for connection to the database                                          |

## Endpoint

### Get crops

Endpoints for retrieving crop data and corresponding subgroups in the database

for crops and groups three endpoints were created, one lists all the crops registered in the database, another one lists all the groups registered in the database and the last one lists the groups according to the id(s) of the crops.

1. endpoint to list the crops, it does not receive any parameters: 

    route: `/crops`

    response: 

    ````
    [
        {
            "id": "64094b58b307071b4e72e907",
            "name": "african_maize",
            "ext_id": "1",
            "base_name": "maize",
            "app_name": "Maize (Africa)"
        },
        ...
    ]
    ````

2. endpoint to list all groups, it does not receive any parameters: 

    route `/groups`

    response:

    ````
    [
        {
            "id": "64094b58b307071b4e72e92b",
            "group_name": "g1",
            "ext_id": "1_1",
            "crop": "64094b58b307071b4e72e907"
        },
        ...
    ]
    ````

3. endpoint to list all the groups of one or more crops, it receives a parameter that is id this can be one or more ids of crops for which you must first consult the endpoint that lists the crops.

    route: `/groupsbyids?id=64094b58b307071b4e72e908`  or 
    `/groupsbyids?id=64094b58b307071b4e72e908,64094b58b307071b4e72e907,...`

    response:
    

    if a single id is sent

    ````
    [
        {
            "id": "64094b58b307071b4e72e92f",
            "group_name": "Musa",
            "ext_id": "2_1",
            "crop": "64094b58b307071b4e72e908"
        },
        ...
    ]
    ````

    if two or more ids are sent

    ````
    [
        {
            "crop_id": "64094b58b307071b4e72e908",
            "groups": [
                {
                    "id": "64094b58b307071b4e72e92f",
                    "group_name": "Musa",
                    "ext_id": "2_1"
                }
            ]
        },
        {
            "crop_id": "64094b58b307071b4e72e907",
            "groups": [
                {
                    "id": "64094b58b307071b4e72e92b",
                    "group_name": "g1",
                    "ext_id": "1_1"
                },
                {
                    "id": "64094b58b307071b4e72e92c",
                    "group_name": "g2",
                    "ext_id": "1_2"
                },
                ... 
            ]
        },
        ...
    ]
    ````

-----------

### Get countries

Endpoint for retrieving countries data in the database

An endpoint was created from which all the countries registered in the database are listed, this endpoint does not receive any parameter. 

endpoint:

`/countries`

response:

````
[
    {
        "id": "640945c244d7c73ce4090301",
        "name": "Afghanistan",
        "iso_2": "AF"
    },
    {
        "id": "640945c244d7c73ce4090302",
        "name": "Åland Islands",
        "iso_2": "AX"
    },
    {
        "id": "640945c244d7c73ce4090303",
        "name": "Albania",
        "iso_2": "AL"
    },
    ...
]
````

-------------

### Get accessions

Endpoints for retrieving accession data in the database

2 endpoints were created for the accessions, one to query the accessions according to one or more crop ids and another one to query them according to one or more group ids. Endpoints receive one or more comma-separated ids.

endpoint to list accessions from crop id(s)

route: `/accessionsbyidcrop?id=64094b58b307071b4e72e908` or
`/accessionsbyidcrop?id=64094b58b307071b4e72e908,64094b58b307071b4e72e907,...`

response

if a single id is sent

````
[
    {
        "id": "640961b88e2f0a85741ec2f6",
        "species_name": "Musa sp.",
        "ext_id": "GNS_1",
        "crop": "64094b58b307071b4e72e908",
        "landrace_group": "64094b58b307071b4e72e92f",
        "institution_name": "Bioversity International Musa Germplasm Transit Centre",
        "source_database": "genesys",
        "latitude": -10.516667,
        "longitude": 150.416667,
        "accession_id": "ITC1023",
        "other_attributes": {
            "atrribute_1": "value_1",
            "atrribute_2": "value_2"
        }
    },
    ...
]
````

if two or more ids are sent

````
[
    {
        "crop_id": "64094b58b307071b4e72e908",
        "accessions": [
            {
                "id": "640961b88e2f0a85741ec2f6",
                "species_name": "Musa sp.",
                "ext_id": "GNS_1",
                "crop": "64094b58b307071b4e72e908",
                "landrace_group": "64094b58b307071b4e72e92f",
                "institution_name": "Bioversity International Musa Germplasm Transit Centre",
                "source_database": "genesys",
                "latitude": -10.516667,
                "longitude": 150.416667,
                "accession_id": "ITC1023",
                "other_attributes": {
                    "atrribute_1": "value_1",
                    "atrribute_2": "value_2"
                }
            },
            ...
            ]
    },
    {
        "crop_id": "64094b58b307071b4e72e907",
        "accessions": [...]
    }
]
````
       
endpoint to list accessions from group id(s)

route: `/accessionsbyidgroup?id=64094b58b307071b4e72e929` or
`/accessionsbyidgroup?id=64094b58b307071b4e72e929,64094b58b307071b4e72e92f,...`

response

if a single id is sent

````
[
    {
        "id": "640961b88e2f0a85741ec2f6",
        "species_name": "Musa sp.",
        "ext_id": "GNS_1",
        "crop": "64094b58b307071b4e72e908",
        "landrace_group": "64094b58b307071b4e72e92f",
        "institution_name": "Bioversity International Musa Germplasm Transit Centre",
        "source_database": "genesys",
        "latitude": -10.516667,
        "longitude": 150.416667,
        "accession_id": "ITC1023",
        "other_attributes": {
            "atrribute_1": "value_1",
            "atrribute_2": "value_2"
        }
    },
    ...
]
````

if two or more ids are sent

````
[
    {
        "group_id": "64094b58b307071b4e72e92f",
        "accessions": [
            {
                "id": "640961b88e2f0a85741ec2f6",
                "species_name": "Musa sp.",
                "ext_id": "GNS_1",
                "crop": "64094b58b307071b4e72e908",
                "landrace_group": "64094b58b307071b4e72e92f",
                "institution_name": "Bioversity International Musa Germplasm Transit Centre",
                "source_database": "genesys",
                "latitude": -10.516667,
                "longitude": 150.416667,
                "accession_id": "ITC1023",
                "other_attributes": {
                    "atrribute_1": "value_1",
                    "atrribute_2": "value_2"
                }
            },
            ...
            ]
    },
    {
        "group_id": "64094b58b307071b4e72e76a",
        "accessions": [...]
    }
]
````



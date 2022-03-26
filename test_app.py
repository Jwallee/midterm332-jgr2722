#!/usr/bin/python
from markupsafe import string
import pytest
from flask import Flask
import json

from app import hello_world
from app import download_data
from app import epochs
from app import epochData
from app import countries
from app import countryData
from app import countryRegion
from app import countryRegionData
from app import countryRegionCity
from app import countryRegionCityData

def test_hello_world():
    yo = hello_world()
    assert type(yo) is str

def test_download_data():
    yo = download_data(iss = 'ISS.OEM_J2K_EPH.xml', sightings = 'XMLsightingData_citiesUSA02.xml')
    assert yo == "Data Successfully Downloaded\n"

def test_epochs():
    yo = epochs()
    assert type(yo) is dict

def test_epochData():
    yo = epochData("2022-045T05:52:00.000Z")
    assert type (yo) is dict

def test_countries():
    yo = countries()
    assert type (yo) is dict

def test_countryData():
    yo=countryData("United_States")
    assert type (yo) is dict

def test_countryRegion():
    yo=countryRegion("United_States")
    assert type (yo) is dict

def test_countryRegionData():
    yo=countryRegionData("United_States","DC")
    assert type (yo) is dict

def test_countryRegionCity():
    yo=countryRegionCity("United_States","DC")
    assert type (yo) is dict

def test_countryRegionCityData():
    yo=countryRegionCityData("United_States","DC","Washington")
    assert type (yo) is dict

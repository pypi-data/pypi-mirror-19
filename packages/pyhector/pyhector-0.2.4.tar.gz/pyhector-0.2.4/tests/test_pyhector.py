# -*- coding: utf-8 -*-

import os

import pandas as pd

import pyhector
from pyhector import Hector, rcp26, rcp45, rcp60, rcp85, read_hector_input


path = os.path.dirname(__file__)
rcps = {
    'rcp26': rcp26,
    'rcp45': rcp45,
    'rcp60': rcp60,
    'rcp85': rcp85
}


def read_hector_output(csv_file):
    """
    Reads a Hector output stream csv and returns a wide DataFrame with
    Hector output data.
    """
    # Filter out spin-up values. In Hector 1.x RCP output streams years are
    # given as end of simulation year. This will change in Hector 2.x.
    # See https://github.com/JGCRI/hector/issues/177
    start_year = 1746
    output_stream = pd.read_csv(csv_file, skiprows=1)

    wide = output_stream[output_stream.year >= start_year].pivot_table(
        index="year", columns="variable", values="value")

    return wide


def test_read_hector_input():
    rcp26 = read_hector_input(
        os.path.join(os.path.dirname(__file__),
        '../pyhector/emissions/RCP26_emissions.csv')
    )
    assert isinstance(rcp26, pd.DataFrame)
    assert rcp26.index[-1] == 2500
    assert rcp26.name == "RCP26_emissions"


def test_rcps():
    # Compare output of Pyhector with original Hector output streams for RCPs.
    for name, scenario in rcps.items():
        original = read_hector_output(
            os.path.join(path, "./data/outputstream_{}.csv".format(name))
        )
        output, _ = pyhector.run(scenario)
        assert output["temperature.Tgav"].round(2).equals(
            original.Tgav.round(2))


def test_default_options():
    with Hector() as h:
        parameters = h.config()
        assert parameters["core"]["endDate"] == "2300"


def test_changed_default_options():
    config_options = {
        "core": {"endDate": "2100"}
    }
    with Hector() as h:
        parameters = h.config(config_options)
        assert parameters["core"]["endDate"] == "2100"


def test_default_options():
    assert pyhector.default_config["core"]["endDate"] == "2300"
    pyhector.run(rcp26, {"core": {"endDate": "2100"}})
    assert pyhector.default_config["core"]["endDate"] == "2300"


def test_units():
    assert pyhector.units["anthroEmissions"] == 'GtC/yr'
    assert pyhector.units["lucEmissions"] == 'GtC/yr'
    assert pyhector.units["NOX_emissions"] == 'MtN/yr'


def test_output_variables():
    results, _ = pyhector.run(rcp26)
    assert len(results.columns) == 3
    results, _ = pyhector.run(rcp26, outputs="all")
    assert len(results.columns) == len(pyhector.variables.keys())

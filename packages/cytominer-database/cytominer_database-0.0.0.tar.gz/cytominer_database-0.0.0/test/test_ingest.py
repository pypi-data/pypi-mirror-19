"""

"""

import configparser
import odo
import os
import pandas as pd
import cytominer_database.ingest
import pkg_resources
import subprocess
import tempfile


def test_seed(dataset):
    munge_file = pkg_resources.resource_filename(__name__, "../cytominer_database/scripts/munge.sh")

    if dataset["munge"]:
        subprocess.call([munge_file, dataset["data_dir"]])

    config_file = os.path.join(dataset["data_dir"], "config.ini")

    config = configparser.ConfigParser()

    config.read(config_file)

    with tempfile.TemporaryDirectory() as temp_dir:
        sqlite_file = os.path.join(temp_dir, "test.db")

        cytominer_database.ingest.seed(config=config, source=dataset["data_dir"], target="sqlite:///{}".format(str(sqlite_file)))

        for (k, v) in dict({"cells": "Cells.csv", "cytoplasm": "Cytoplasm.csv", "nuclei": "Nuclei.csv"}).items():
            config["filenames"][k] = v

        for table_key in ["image", "cells", "cytoplasm", "nuclei"]:
            csv_filename = os.path.join(temp_dir, config["filenames"][table_key])

            table_name = config["filenames"][table_key].split(".")[0]

            odo.odo("sqlite:///{}::{}".format(str(sqlite_file), table_name), csv_filename)

            df = pd.read_csv(csv_filename)

            assert df.shape[0] == dataset["ingest"]["{}_nrows".format(table_name)]

            assert df.shape[1] == dataset["ingest"]["{}_ncols".format(table_name)] + 1

            if table_key != "image":
                assert df.groupby(["TableNumber", "ImageNumber"]).size().sum() == dataset["ingest"]["{}_nrows".format(table_name)]

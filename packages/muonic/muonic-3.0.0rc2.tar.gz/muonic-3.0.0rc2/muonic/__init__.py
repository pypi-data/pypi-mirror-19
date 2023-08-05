"""
The muonic package
"""
from os import getenv, path, pardir

AUTHORS = [
    ("Robert Franke", "robert.franke@desy.de"),
    ("Achim Stoessl", "achim.stoessl@desy.de"),
    ("Basho Kaminsky", "basho.kaminsky@desy.de"),
    ("Martin Ohmann", "martin@mohmann.de"),
    ("Hans-Peter Bretz", "hans-peter.bretz@desy.de")
]

DOC_PATH = path.abspath(path.join(
        path.dirname(__file__), pardir, 'docs', 'html'))

DATA_PATH = path.join(getenv('HOME'), 'muonic_data')

__all__ = ["util", "daq", "analysis", "gui"]

__version__ = "3.0.0-rc2"
__author__ = ", ".join([author[0] for author in AUTHORS])
__author_email__ = ", ".join([author[1] for author in AUTHORS])

__description__ = ("Software to work with QNet DAQ cards. " +
                   "This is a TRUNK version")

__source_location__ = "https://github.com/CosmicLabDESY/muonic/"
__docs_hosted_at__ = "http://achim1.github.io/muonic/"
__download_url__ = ("https://github.com/CosmicLabDESY/muonic/archive/" +
                    "release2.zip")
__manual_hosted_at__ = ("http://physik-begreifen-zeuthen.desy.de/angebote/" +
                        "kosmische_teilchen/schuelerexperimente/" +
                        "cosmo_experiment/index_ger.html")
__license__ = "GPLv3"

# -*- coding: utf-8 -*-

# Set default logging handler to avoid "No handler found" warnings.
import logging
from my_python_project.MyClassManager import MyClassManager


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format="%(levelname)s %(asctime)s [%(process)d] %(name)s %(filename)s:%(lineno)d %(message)s",
                        )
    try:
        logging.info("Start my class manager")
        myclassmanager = MyClassManager()
        myclassmanager.run()
    except Exception as exception:
        logging.info("MyClassManager exception: %s", exception)
        logging.info("Try to finish...")

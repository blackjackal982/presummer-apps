import logging

logger_m4 = logging.getLogger(__name__)
logger_m4.setLevel(logging.INFO)
def f6():
    logger_m4.info("entering p1.m4.f6")
    logger_m4.warning("warning at p1.m4.f6")
    logger_m4.error("error in p1.m4.f6")
    logger_m4.info("exiting p1.m4.f6")
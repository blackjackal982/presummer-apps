import logging

logger_m3 = logging.getLogger(__name__)
logger_m3.setLevel(logging.INFO)
def f5():
    logger_m3.info("entering p1.m3.f5")
    logger_m3.warning("warning at p1.m3.f5")
    logger_m3.error("error in p1.m3.f5")
    logger_m3.info("exiting p1.m3.f5")
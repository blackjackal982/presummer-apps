import logging
logger_m1 = logging.getLogger(__name__)
logger_m1.setLevel(logging.INFO)
def f3():
    logger_m1.info("entering p1.m2.f3")
    logger_m1.warning("warning at p1.m2.f3")
    logger_m1.error("error in p1.m2.f3")
    logger_m1.info("exiting p1.m2.f3")

def f4():
    logger_m1.info("entering p1.m2.f4")
    logger_m1.warning("warning at p1.m2.f4")
    logger_m1.error("error in p1.m2.f4")
    logger_m1.info("exiting p1.m2.f4")

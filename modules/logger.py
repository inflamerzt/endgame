import logging, os


def dbg(x):
    logging.debug(x)


def inf(x):
    logging.info(x)


def warn(x):
    logging.warning(x)


def err(x):
    logging.error(x)


def loglevel(level):
    logger = logging.getLogger()
    logger.setLevel(level)


def init():
    pid = os.getpid()
    logging.basicConfig(
        filename="endgame.log",
        encoding="utf-8",
        format=f"%(asctime)s -=ENDGAME=- (PID:{pid}) %(levelname)s: %(message)s",
    )

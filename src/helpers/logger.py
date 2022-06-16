import logging
from pathlib import Path

main = logging.getLogger('main')
main.setLevel(logging.INFO)
sim_logger = logging.getLogger('sim_logger')
sim_logger.setLevel(logging.INFO)
sim_copy_logger = logging.getLogger('sim_copy_logger')
sim_copy_logger.setLevel(logging.CRITICAL)
algo_first_available = logging.getLogger('algo_first_available')
algo_first_available.setLevel(logging.INFO)
algo_short_mode = logging.getLogger('algo_short_mode')
algo_short_mode.setLevel(logging.INFO)
algo_short_mode_critical = logging.getLogger('algo_short_mode_critical')
algo_short_mode_critical.setLevel(logging.CRITICAL)
algo_long_mode = logging.getLogger('algo_long_mode')
algo_long_mode.setLevel(logging.INFO)
algo_genetic = logging.getLogger('algo_genetic')
algo_genetic.setLevel(logging.INFO)

loggers = [sim_logger, sim_copy_logger, algo_first_available, algo_short_mode, algo_long_mode, algo_genetic, main]


def config_logger(filename):
    Path("../output/logs").mkdir(parents=True, exist_ok=True)

    fileh = logging.FileHandler(f"../output/logs/{filename}.log", 'a')
    formatter = logging.Formatter('[%(filename)s %(funcName)s()]   %(message)s')
    fileh.setFormatter(formatter)

    for logger in loggers:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        logger.addHandler(fileh)






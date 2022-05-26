import logging

logging.basicConfig(filename="../../logs/test.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

sim_logger = logging.getLogger('sim_logger')
sim_copy_logger = logging.getLogger('sim_copy_logger')
algo_first_available = logging.getLogger('algo_first_available')


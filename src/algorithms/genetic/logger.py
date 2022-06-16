import logging

logging.basicConfig(filename="./genetic.log",
                    format='[%(filename)s %(funcName)s()]   %(message)s')

cross = logging.getLogger('cross')
cross.setLevel(logging.DEBUG)
evaluate = logging.getLogger('evaluate')
evaluate.setLevel(logging.DEBUG)
ga = logging.getLogger('ga')
ga.setLevel(logging.DEBUG)
individual = logging.getLogger('individual')
individual.setLevel(logging.DEBUG)
mutate = logging.getLogger('mutate')
mutate.setLevel(logging.DEBUG)
population = logging.getLogger('population')
population.setLevel(logging.DEBUG)
select = logging.getLogger('select')
select.setLevel(logging.DEBUG)

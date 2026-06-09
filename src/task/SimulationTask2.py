from ok import Logger
from src.task.EnhancedUtils import hijack_use_stamina, revise_count
from src.task.SimulationTask import SimulationTask

logger = Logger.get_logger(__name__)


class SimulationTask2(SimulationTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = '⭐ Simulation Challenge'
        self.default_config.update({'Simulation Challenge Count': 0})
        self.config_description.update({'Simulation Challenge Count': 'farm Simulation Challenge N time(s), 40 stamina per time, set a large number to use all stamina'})

    def farm_simulation(self, config=None):
        if config is None:
            config = self.config
        self.make_sure_in_world()
        try:
            hijack_use_stamina(self) # 劫持
            count = revise_count(task_class=self, input_count=config.get('Simulation Challenge Count'))
            if count > 0:
                used_stamina = 180 - count * self.stamina_once
                super().farm_simulation(daily=True, used_stamina=used_stamina, config=config)
        finally:
            self.__dict__.pop('use_stamina', None) # 还原
        self.make_sure_in_world()

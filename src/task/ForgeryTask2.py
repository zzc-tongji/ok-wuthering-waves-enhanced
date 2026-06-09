from ok import Logger
from src.task.EnhancedUtils import hijack_use_stamina, revise_count
from src.task.ForgeryTask import ForgeryTask

logger = Logger.get_logger(__name__)


class ForgeryTask2(ForgeryTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = '⭐ Forgery Challenge'
        self.default_config.update({'Forgery Challenge Count': 0})
        self.config_description.update({'Forgery Challenge Count': 'farm Forgery Challenge N time(s), 40 stamina per time, set a large number to use all stamina'})

    def farm_forgery(self, config=None):
        if config is None:
            config = self.config
        self.make_sure_in_world()
        try:
            hijack_use_stamina(self) # 劫持
            count = revise_count(task_class=self, input_count=config.get('Forgery Challenge Count'))
            if count > 0:
                used_stamina = 180 - count * self.stamina_once
                super().farm_forgery(daily=True, used_stamina=used_stamina, config=config)
        finally:
            self.__dict__.pop('use_stamina', None) # 还原
        self.make_sure_in_world()

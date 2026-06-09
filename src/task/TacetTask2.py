from ok import Logger
from src.task.EnhancedUtils import hijack_use_stamina, revise_count
from src.task.TacetTask import TacetTask

logger = Logger.get_logger(__name__)


class TacetTask2(TacetTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = '⭐ Tacet Suppression'
        self.default_config.update({'Tacet Suppression Count': 0})
        self.config_description.update({'Tacet Suppression Count': 'farm Tacet Suppression N time(s), 60 stamina per time, set a large number to use all stamina'})

    def farm_tacet(self, config=None):
        if config is None:
            config = self.config
        self.ensure_main()
        try:
            hijack_use_stamina(self) # 劫持
            count = revise_count(task_class=self, input_count=config.get('Tacet Suppression Count'))
            if count > 0:
                used_stamina = 180 - count * self.stamina_once
                super().farm_tacet(daily=True, used_stamina=used_stamina, config=config)
        finally:
            self.__dict__.pop('use_stamina', None) # 还原
        self.ensure_main()

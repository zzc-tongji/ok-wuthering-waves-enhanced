from ok import Logger
from types import MethodType

logger = Logger.get_logger(__name__)

def hijack_use_stamina(task_class):
    #
    def use_stamina(self, once, must_use=0):
        self.sleep(1)
        current, back_up, total = self.get_stamina()
        y = 0.62
        if must_use >= once * 2 and total >= once * 2:
            used = once * 2
            x = 0.67
            logger.info(f"当前加备用大于日常剩余所需, 使用双倍, {must_use} >= {once * 2} and {total} >= {once * 2}")
        else:
            used = once
            x = 0.32
            logger.info(f"使用单倍体力")
        self.click(x, y, after_sleep=1)
        if self.wait_feature('gem_add_stamina', horizontal_variance=0.4, vertical_variance=0.05,
                             time_out=2, settle_time=0.5):  # 看是否需要使用备用体力
            self.click(0.70, 0.71, after_sleep=1)  # 点击确认
            self.click(0.70, 0.71, after_sleep=1)
            self.back(after_sleep=1)
            self.click(x, y, after_sleep=1)

        current -= used
        must_use -= used
        total -= used
        if total < once:
            logger.info(f"current stamina: {current} not enough to continue")
            can_continue = False
        elif must_use <= 0:
            can_continue = False
            logger.info(f"current stamina: {current} must_use completed")
        else:
            can_continue = True
        return can_continue, used
    #
    task_class.use_stamina = MethodType(use_stamina, task_class)

def revise_count(task_class, input_count):
    if input_count <= 0:
        return 0
    gray_book_boss = task_class.openF2Book("gray_book_boss")
    task_class.click_box(gray_book_boss, after_sleep=1)
    _, _, total = task_class.get_stamina()
    task_class.ensure_main()
    if total < 0:
        raise RuntimeError("fail to get stamina")
    return min(input_count, total // task_class.stamina_once)

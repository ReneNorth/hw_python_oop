from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Родительский класс тренировок."""
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: float = 60

    def __init__(self: float,
                 action: float,
                 duration: float,
                 weight: float):
        self.action: float = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получаем преодолённую дистацию."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_time_min(self) -> float:
        return self.duration * self.MIN_IN_HOUR

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Обозначаю метод расчёта калорий в родительском классе."""
        raise NotImplementedError('Определите функцию расчёта калорий')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Субкласс: Беговая тренировка."""
    COEFF_CALORIE_RUNNING_1: float = 18
    COEFF_CALORIE_RUNNING_2: float = 20

    def __init__(self, action, duration, weight):
        super().__init__(action, duration, weight)

    def get_spent_calories(self):
        """Переопределяем расчёт расхода калорий для плавания."""
        return ((self.COEFF_CALORIE_RUNNING_1
                 * self.get_mean_speed() - self.COEFF_CALORIE_RUNNING_2)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_HOUR))


class SportsWalking(Training):
    """Субкласс: Тренировка по спортивной ходьбе."""
    COEFF_CALORIE_WALKING_1: float = 0.035
    COEFF_CALORIE_WALKING_2: float = 0.029

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Переопределяю метод расчтёта калорий для спортивной ходьбы."""
        return ((self.COEFF_CALORIE_WALKING_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEFF_CALORIE_WALKING_2 * self.weight)
                * self.get_time_min())


class Swimming(Training):
    """Субкласс: Тренировка по плаванию."""
    LEN_STEP: float = 1.38
    COEFF_CALORIE_SWIM_1: float = 1.1
    COEFF_CALORIE_SWIM_2: float = 2

    def __init__(self, action,
                 duration, weight, length_pool,
                 count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Переопределяю расчёт средней скорости плавания."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / (self.duration))

    def get_spent_calories(self) -> float:
        """Переопределяю расчёт расхода калорий для плавания."""
        return ((self.get_mean_speed() + self.COEFF_CALORIE_SWIM_1)
                * self.COEFF_CALORIE_SWIM_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_types = {'RUN': Running,
                      'SWM': Swimming,
                      'WLK': SportsWalking}
    return training_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

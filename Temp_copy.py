
# from itertools import count <- как я опять случайно это сделал?


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, speed, distance,
                 spent_calories):
        self.training_type = training_type
        self.duration: float = duration
        self.speed = speed
        self.distance = distance
        self.spent_calories = spent_calories

    def get_message(self):
        return f'Тип тренировки: {self.training_type}; Длительность: {self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км; Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: {self.spent_calories:.3f}.'


class Training:
    M_IN_KM = 1000
    LEN_STEP = 0.65  # не забыть поменять в зависимости от типа активности
    MIN_IN_HOUR = 60

    def __init__(self,
                 training_type,
                 action,
                 duration: float,
                 weight):
        self.training_type = training_type
        self.action = action
        self.duration: float = duration
        self.weight = weight
    # сделать метод для расчёта времени тренировки в минутах

    def __str__(self):
        return f'{self.action}, {self.duration}, {self.weight}'

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        return 1+1  # сделать здесь общую фрмулу?

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.training_type,
                           self.duration,
                           self.get_mean_speed(),
                           self.get_distance(),
                           self.get_spent_calories())


class Running(Training):
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def __init__(self, training_type, action, duration, weight):
        super().__init__(training_type, action, duration, weight)
    # может проблема в том как я наследую методы

    def get_spent_calories(self):
        return ((self.coeff_calorie_1
                 * self.get_mean_speed() - self.coeff_calorie_2)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, training_type, action, duration, weight, height):
        super().__init__(training_type, action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (0.035 * self.weight + (self.get_mean_speed() ** 2
                // self.height) * 0.029 * self.weight) * (self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self, training_type, action,
                 duration, weight, lenght_pool,
                 count_pool):
        super().__init__(training_type, action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.lenght_pool * self.count_pool
                / self.M_IN_KM / (self.duration))
        # скобки наверное убрать

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    # https://app.slack.com/client/TPV9DP0N4/C039ZK7F75Z/thread/C039ZK7F75Z-1650581999.845099

    dict = {'RUN': Running,
            'SWM': Swimming,
            'WLK': SportsWalking}

    for train_head, train_type in dict.items():
        if workout_type == train_head:
            training = dict[train_type](*data)
        
    return training
    
    # if workout_type == 'RUN':
    #     return Running(training_type='Running', action=data[0], duration=data[1], weight=data[2])
    # elif workout_type == 'SWM':
    #     return Swimming(training_type='Swimming', action=data[0], duration=data[1], weight=data[2], lenght_pool=data[3], count_pool=data[4])
    # elif workout_type == 'WLK':
    #     return SportsWalking(training_type='SportsWalking', action=data[0], duration=data[1], weight=data[2], height=data[3])
    # Распаковать аргументы в функцию из списка можно * foo(*a)
    # раньше везде было training_type=workout_type
    # else:
    #   print('There is no such calss')

    # У тебя внутри функции должен быть словарь (dict)
    # который ассоциативно связывает “Код тренировки”
    # с самим классом тренировки.
    # Входные параметры у функции это ведь код тренировки
    # и данные необходимые для ее создания
    # (пример для Бега, количество шагов, время и.т.д.)
    # От тебя требуется, по коду тренировки определить (сматчить)
    # из словаря необходимый класс,
    # и создать (инициализировать) по этому классу, по данным в data свою
    # тренировку.


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())
    # про main https://app.slack.com/client/TPV9DP0N4/C039ZK7F75Z/thread/C039ZK7F75Z-1650750544.396519
    # print(training.show_training_info().get_message())
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        # изначальный датасет ('RUN', [15000, 1, 75]),
        ('RUN', [1206, 12, 6]),  # этот из тестового для дебага
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
# распаковщик передаёт в main данные о тренировке,
# а та дёргает show_training_info в классе Training

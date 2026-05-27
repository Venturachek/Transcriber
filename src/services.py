from enum import Enum

class Services(str, Enum):
    COMPUTER_DIAGNOSTICS = "Комп'ютерна діагностика"
    OIL_CHANGE = "Заміна оливи ДВЗ + масляний фільтр"
    COMPLEX_DIAGNOSTICS = "Комплексна діагностика"
    ENDOSCOPY = "Ендоскопія"
    AIR_FILTER = "Заміна повітряного фільтра ДВЗ"
    CABIN_FILTER = "Заміна фільтра салону в салонному відділенні"
    SILENT_BLOCK = "Заміна сайлентблоку"
    LEVER_INSTALL = "Зняття / встановлення важіля"
    CARDAN_COUPLING = "Заміна еластичної муфти карданного валу"
    LOCKSMITH = "Слюсарні роботи"
    SUSPENSION_DIAGNOSTICS = "Діагностика підвіски (НЕ ВИКОРИСТОВУЄМ)ВИКОРИСТОВУЄМ КОМПЛЕКСНУ"
    FRONT_LEVER = "Зняття / встановлення важіля прд."
    FRONT_SHOCK = "Заміна амортизатора переднього"
    GEARBOX_OIL = "Заміна оливи АКПП"
    WASH = "Мийка / чистка деталі"
    AIR_HOSE = "Зняття / встановлення повітряного патрубка"
    COOLANT = "Заміна охолоджувальної рідини"
    BRAKE_FLUID = "Заміна гальмівної рідини з прокачкою"
    REAR_DIFF_OIL = "Заміна оливи в зд. редукторі"
    CODING = "Кодування опцій"
    REAR_SHOCK = "Заміна амортизатора зд."
    FRONT_BRAKES = "Заміна гальмівних дисків та колодок прд."

    @classmethod
    def values(cls) -> list[str]:
        return [e.value for e in cls]
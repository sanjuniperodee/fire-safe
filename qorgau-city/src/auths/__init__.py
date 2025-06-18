from django.db import models
from django.db.models import TextChoices


class Role(models.TextChoices):
    CITIZEN = 'CITIZEN', 'Гражданин'
    OBJECT_OWNER = 'OBJECT_OWNER', 'Собственник объекта'
    INSPECTOR = 'INSPECTOR', 'Инспектор'
    PROVIDER = 'PROVIDER', 'Поставщик'
    ADMIN = 'ADMIN', 'Админ'
    OPERATOR = 'OPERATOR', 'Оператор'
    FIRE_DEPARTMENT = 'FIRE_DEPARTMENT', 'Пожарная часть'


class Status(TextChoices):
    ACCEPTED = 'ACCEPTED', 'Принято'
    NOT_ACCEPTED = 'NOT_ACCEPTED', 'Не принято'


class UserCategoryType(models.TextChoices):
    PROVIDER = 'PROVIDER', 'Provider'
    # OBJECT_OWNER = 'OBJECT_OWNER', 'Object Owner'


class INSPECTOR_RANK(models.TextChoices):
    Private_Civil_Protection = "Private civil protection", "Рядовой гражданской защиты"
    Junior_Sergeant_of_Civil_Protection = "Junior Sergeant of Civil Protection", "Младший сержант гражданской защиты"
    Civil_Protection_Sergeant = "Civil Protection Sergeant", "Сержант гражданской защиты"
    Senior_Sergeant_of_Civil_Protection = "Senior Sergeant of Civil Protection", "Старший сержант гражданской защиты"
    Civil_Protection_Foreman = "Civil Protection Foreman", "Старшина гражданской защиты"
    Second_Lieutenant_of_Civil_Protection = "Second Lieutenant of Civil Protection", "Младший лейтенант гражданской защиты"
    Lieutenant_of_Civil_Protection = "Lieutenant of Civil Protection", "Лейтенант гражданской защиты"
    Senior_Lieutenant_of_Civil_Protection = "Senior Lieutenant of Civil Protection", "Старший лейтенант гражданской защиты"
    Captain_of_Civil_Protection = "Captain of Civil Protection", "Капитан гражданской защиты"
    Major_of_Civil_Protection = "Major of Civil Protection", "Майор гражданской защиты"
    Lieutenant_Colonel_of_Civil_Protection = "Lieutenant Colonel of Civil Protection", "Подполковник гражданской защиты"
    Colonel_of_Civil_Protection = "Colonel of Civil Protection", "Полковник гражданской защиты"
    Major_General_of_Civil_Protection = "Major General of Civil Protection", "Генерал-майор гражданской защиты"
    Lieutenant_General_of_Civil_Protection = "Lieutenant General of Civil Protection", "Генерал-лейтенант гражданской защиты"
    Colonel_General_of_Civil_Protection = "Colonel-General of Civil Protection", "Генерал-полковник гражданской защиты"


class INSPECTOR_POSITION(models.TextChoices):
    Chief_State_Inspector_for_Fire_Control = ("Chief State Inspector for Fire Control",
                                              "Главный государственный инспектор по пожарному контролю")
    Chief_Inspector_of_Fire_Control = "Chief Inspector of Fire Control", "Старший инспектор по пожарному контролю"
    Fire_Control_Inspector = "Fire Control Inspector", "Инспектор по пожарному контролю"


class ORGANIZATION_MAIN_TYPE(models.TextChoices):
    Commercial_Organizations = "Commercial Organizations", "Коммерческие Организации"
    Non_Commercial_Organizations = "NonCommercial Organizations", "Не Коммерческие Организации"


class ORGANIZATION_TYPE(models.TextChoices):
    State_Owned_Enterprises = "State-owned enterprises(Commercial)", "Государственные предприятия(Коммерческая)"
    Business_Partnerships = "Business partnerships(Commercial)", "Хозяйственные товарищества(Коммерческая)"
    Joint_Stock_Company_Commercial = "Joint stock company(Commercial)", "Акционерное общество(Коммерческая)"
    Production_Cooperative = "Production cooperative(Commercial)", "Производственный кооператив(Коммерческая)"

    Institutions = "Institutions(NonCommercial)", "Учреждения(Не Коммерческая)"
    Public_Association = "Public Association(NonCommercial)", "Общественное объединение(Не Коммерческая)"
    Joint_Stock_Company_NonCommercial = "Joint stock company(NonCommercial)", "Акционерное общество(Не Коммерческая)"
    Consumer_Cooperative = "Consumer Cooperative(NonCommercial)", "Потребительский кооператив(Не Коммерческая)"
    Fund = "Fund(NonCommercial)", "Фонд(Не Коммерческая)"
    Religious_Associations = "Religious associations(NonCommercial)", "Религиозные объединения(Не Коммерческая)"
    Associations_Of_Individual_Entrepreneurs = \
        (
            "Associations of individual entrepreneurs and (or) legal entities in the form of an association (union)(NonCommercial)",
            "Объединения индивидуальных предпринимателей и (или) юридических лиц в форме ассоциации (союза)(Не Коммерческая)"
        )
    OtherForms = (
            "Other forms provided for by law(NonCommercial)",
            "Иные формы, предусмотренные законодательством(Не Коммерческая)"
        )


ALLOWED_ROLES = {
    'object_owner': ['OBJECT_OWNER'],
    'provider': ['PROVIDER']
}

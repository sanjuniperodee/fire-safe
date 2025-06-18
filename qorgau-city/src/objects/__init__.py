# from django.db.models import TextChoices
#
#
# class ObjectMainOrganizationType(TextChoices):
#     Commercial_Organizations = "Commercial Organizations", "Коммерческие Организации"
#     Government_Agencies = "Government Agencies", "Государственные учреждения"
#     Residential_Buildings = "Residential Buildings", "Жилые здания"
#     Industrial_Facilities = "Industrial Facilities", "Промышленные объекты"
#     Public_Buildings = "Public Buildings", "Общественные здания"
#     Transport_Infrastructure = "Transport Infrastructure", "Транспортная инфраструктура"
#     Educational_Institutions = "Educational Institutions", "Образовательные учреждения"
#     High_risk_Facilities = "High-risk Facilities", "Объекты повышенной опасности"
#     Special_Objects = "Special Objects", "Специальные объекты"
#     Agricultural_Facilities = "Agricultural Facilities", "Сельскохозяйственные объекты"
#     Religious_Sites = "Religious Sites", "Религиозные объекты"
#     Sports_Facilities = "Sports Facilities", "Спортивные сооружения"
#
#
# class MaterialOfTheExteriorWalls(TextChoices):
#     BRICK = "BRICK", "Кирпич"
#     CONCRETE = "CONCRETE", "Бетон"
#     STONE = "STONE", "Камень"
#     WOOD = "WOOD", "Дерево"
#     METAL = "METAL", "Металл"
#     GLASS = "GLASS", "Стекло"
#     COMPOSITE_MATERIALS = "COMPOSITE_MATERIALS", "Композитные материалы"
#     POLYMER_MATERIALS = "POLYMER_MATERIALS", "Полимерные материалы"
#     PLASTER = "PLASTER", "Штукатурка"
#     CERAMIC_MATERIALS = "CERAMIC_MATERIALS", "Керамические материалы"
#     THERMAL_INSULATION_MATERIALS = "THERMAL_INSULATION_MATERIALS", "Теплоизоляционные материалы"
#     MIXED_DESIGNS = "MIXED_DESIGNS", "Смешанные конструкции"
#     NATURAL_MATERIALS = "NATURAL_MATERIALS", "Природные материалы"
#     MODERN_ENVIRONMENTAL_MATERIALS = "MODERN_ENVIRONMENTAL_MATERIALS", "Современные экологические материалы"
#
#
# class LightingType(TextChoices):
#     NATURAL_LIGHTING = "NATURAL_LIGHTING", "Естественное освещение"
#     ARTIFICIAL_LIGHTING = "ARTIFICIAL_LIGHTING", "Искусственное освещение"
#     #EMERGENCY_LIGHTING = "EMERGENCY_LIGHTING", "Аварийное освещение"
#
#
# class VentilationType(TextChoices):
#     SUPPLY_VENTILATION = "SUPPLY_VENTILATION", "Приточная вентиляция"
#     EXHAUST_VENTILATION = "EXHAUST_VENTILATION", "Вытяжная вентиляция"
#     SUPPLY_AND_EXHAUST_SYSTEM = "SUPPLY_AND_EXHAUST_SYSTEM", "Приточно-вытяжная вентиляция"
#     NATURAL_VENTILATION = "NATURAL_VENTILATION", "Естественная вентиляция"
#     ABSENT = "ABSENT", "Отсутствует"
#
#
# class HeatingType(TextChoices):
#     AUTONOMOUS = "AUTONOMOUS", "Автономный"
#     FURNACE = "FURNACE", "Печное"
#
#     ABSENT = "ABSENT", "Отсутствует"
#
#
# class SecurityType(TextChoices):
#     DEPARTMENTAL = "DEPARTMENTAL", "Ведомственная"
#     PRIVATE_SECURITY = "PRIVATE_SECURITY", "Вневедомственная охрана"
#     PRIVATE_SECURITY_COMPANY = "PRIVATE_SECURITY_COMPANY", "Частное охранное предприятие (ЧОП)"
#     OWN_STRENGTH = "OWN_STRENGTH", "Собственными силами"
#     NOT_GUARDED = "NOT_GUARDED", "Не охраняется"
#
#
# class SubBuildingType(TextChoices):
#     BUILDING = 'BUILDING', 'Здание'
#     CONSTRUCTION = 'CONSTRUCTION', 'Сооружение'
#     PREMISES = "PREMISE", "Помещение"
#     DIFFERENT_CONSTRUCTION = 'DIFFERENT CONSTRUCTION', 'Иная конструкция'
#
#
# class Rating(TextChoices):
#     ONE = '1', '1'
#     TWO = '2', '2'
#     THREE = '3', '3'
#
#
# class Status(TextChoices):
#     PENDING = 'PENDING', 'Ожидает ответа'
#     ANSWERED = 'ANSWERED', 'Отвечено'
#     EXPIRED = 'EXPIRED', 'Истек срок'
#     NOT_ANSWERED = 'NOT_ANSWERED', 'Не отвечено'




from django.db.models import TextChoices


class ObjectMainOrganizationType(TextChoices):
    Commercial_Organizations = "Commercial Organizations", "Коммерческие Организации"
    Government_Agencies = "Government Agencies", "Государственные учреждения"
    Residential_Buildings = "Residential Buildings", "Жилые здания"
    Industrial_Facilities = "Industrial Facilities", "Промышленные объекты"
    Public_Buildings = "Public Buildings", "Общественные здания"
    Transport_Infrastructure = "Transport Infrastructure", "Транспортная инфраструктура"
    Educational_Institutions = "Educational Institutions", "Образовательные учреждения"
    High_risk_Facilities = "High-risk Facilities", "Объекты повышенной опасности"
    Special_Objects = "Special Objects", "Специальные объекты"
    Agricultural_Facilities = "Agricultural Facilities", "Сельскохозяйственные объекты"
    Religious_Sites = "Religious Sites", "Религиозные объекты"
    Sports_Facilities = "Sports Facilities", "Спортивные сооружения"


class MaterialOfTheExteriorWalls(TextChoices):
    BRICK = "Кирпич"
    CONCRETE = "Бетон"
    STONE = "Камень"
    WOOD = "Дерево"
    METAL = "Металл"
    GLASS = "Стекло"
    COMPOSITE_MATERIALS = "Композитные материалы"
    POLYMER_MATERIALS = "Полимерные материалы"
    PLASTER = "Штукатурка"
    CERAMIC_MATERIALS = "Керамические материалы"
    THERMAL_INSULATION_MATERIALS = "Теплоизоляционные материалы"
    MIXED_DESIGNS = "Смешанные конструкции"
    NATURAL_MATERIALS = "Природные материалы"
    MODERN_ENVIRONMENTAL_MATERIALS = "Современные экологические материалы"


class LightingType(TextChoices):
    NATURAL_LIGHTING = "Естественное освещение"
    ARTIFICIAL_LIGHTING = "Искусственное освещение"
    #EMERGENCY_LIGHTING = "Аварийное освещение"


class VentilationType(TextChoices):
    SUPPLY_VENTILATION = "Приточная вентиляция"
    EXHAUST_VENTILATION = "Вытяжная вентиляция"
    SUPPLY_AND_EXHAUST_SYSTEM = "Приточно-вытяжная вентиляция"
    NATURAL_VENTILATION = "Естественная вентиляция"
    ABSENT = "Отсутствует"


class HeatingType(TextChoices):
    AUTONOMOUS = "Автономный"
    FURNACE = "Печное"
    ABSENT = "Отсутствует"


class SecurityType(TextChoices):
    DEPARTMENTAL = "Ведомственная"
    PRIVATE_SECURITY = "Вневедомственная охрана"
    PRIVATE_SECURITY_COMPANY = "Частное охранное предприятие (ЧОП)"
    OWN_STRENGTH = "Собственными силами"
    NOT_GUARDED = "Не охраняется"


class StairsClassificationType(TextChoices):
    N_1 = "Н1", "Лестничные клетки с входом на лестничную клетку с этажа через наружную воздушную зону по открытым переходам"
    N_2 = "Н2", "Лестничные клетки с подпором воздуха на лестничную клетку при пожаре"
    L_1 = "L1", "Лестничные клетки с естественным освещением через остекленные или открытые проемы в наружных стенах на каждом этаже"
    L_2 = "L2", "Лестничные клетки с естественным освещением через остекленные или открытые проемы в покрытии"
    L_3 = "L3", "Лестничные клетки с естественным освещением через остекленные или открытые проемы в наружных стенах на каждом этаже и в покрытии"


class SubBuildingType(TextChoices):
    BUILDING = 'BUILDING', 'Здание'
    CONSTRUCTION = 'CONSTRUCTION', 'Сооружение'
    PREMISES = "PREMISE", "Помещение"
    DIFFERENT_CONSTRUCTION = 'DIFFERENT CONSTRUCTION', 'Иная конструкция'


class Rating(TextChoices):
    ONE = '1', '1'
    TWO = '2', '2'
    THREE = '3', '3'


class Status(TextChoices):
    PENDING = 'PENDING', 'Ожидает ответа'
    ANSWERED = 'ANSWERED', 'Отвечено'
    EXPIRED = 'EXPIRED', 'Истек срок'
    NOT_ANSWERED = 'NOT_ANSWERED', 'Не отвечено'
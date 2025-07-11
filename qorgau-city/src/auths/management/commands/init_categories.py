from django.core.management.base import BaseCommand
from auths.models import Category


class Command(BaseCommand):
    help = 'Initialize categories for services'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Initializing categories...'))
        
        # Категории услуг из фронтенда
        categories_data = [
            {
                "id": 1, 
                "name": "Определение качества огнезащитной обработки деревянных конструкций и материалов на её основе", 
                "measurement_unit": "каждые 1000 м2"
            },
            {
                "id": 2, 
                "name": "Определение качества огнезащитной обработки деревянных конструкций и материалов на её основе", 
                "measurement_unit": "до 500 м2"
            },
            {
                "id": 3, 
                "name": "Определение качества огнезащитной обработки стальных конструкций", 
                "measurement_unit": "каждые 1000 м2"
            },
            {
                "id": 4, 
                "name": "Определение качества огнезащитной обработки стальных конструкций", 
                "measurement_unit": "до 500 м2"
            },
            {
                "id": 5, 
                "name": "Определение прочности стационарной наружной вертикальной (без ограждения) пожарной лестницы", 
                "measurement_unit": "1 п/м длины лестницы"
            },
            {
                "id": 6, 
                "name": "Определение прочности стационарной наружной вертикальной (с ограждением свыше 6м) пожарной лестницы", 
                "measurement_unit": "1 п/м длины лестницы"
            },
            {
                "id": 7, 
                "name": "Определение прочности стационарной наружной маршевой пожарной лестницы", 
                "measurement_unit": "1 п/м длины"
            },
            {
                "id": 8, 
                "name": "Определение прочности ограждения кровли.", 
                "measurement_unit": "1 п/м длины"
            },
            {
                "id": 9, 
                "name": "Текстильные материалы, ткани декоративные, промышленные и технические (воспламеняемость и классификация)", 
                "measurement_unit": "каждые 1000 м2 (20 МРП)"
            },
            {
                "id": 10, 
                "name": "Определение качества пенообразователей В зависимости от типа и назначения (ТТХ)", 
                "measurement_unit": ""
            },
            {
                "id": 11, 
                "name": "Герметизирующий, огнезащитный материал применяемый в качестве обработки кабельных линий, стыков (качество и толщина огнезащитного покрытия, стыка)", 
                "measurement_unit": "п/м, шт."
            },
            {
                "id": 12, 
                "name": "Материалы и изделия строительные пожарные, теплоизоляционные и звукоизоляционные, минеральная вата и аналогичные минеральные ваты (включая их смеси), навалом, в листах или рулонах (линейные размеры, внешний вид, толщина)", 
                "measurement_unit": "п/м, шт."
            },
            {
                "id": 13, 
                "name": "Герметизирующий, огнезащитный материал применяемый в качестве наружного (внутреннего) слоя монтажного шва, стыка, узлов примыкания оконных блоков к стеновым проемам", 
                "measurement_unit": "п/м"
            },
            {
                "id": 14, 
                "name": "Вентиляционная система, дымоудаления и система подпора воздуха (Измерение фактического расхода воздуха)", 
                "measurement_unit": "-"
            },
            {
                "id": 15, 
                "name": "Эффективность огнезащитного средства", 
                "measurement_unit": "шт."
            },
            {
                "id": 16, 
                "name": "Пенообразователи (внешний вид и качество)", 
                "measurement_unit": "шт."
            },
            {
                "id": 17, 
                "name": "Кабели, провода, шнуры (Сопротивление изоляций)", 
                "measurement_unit": "шт."
            },
            {
                "id": 18, 
                "name": "Конструкции строительные. Противопожарные двери и ворота - предельные состояния (E, I)", 
                "measurement_unit": "единица"
            },
            {
                "id": 19, 
                "name": "Конструкции строительные. Несущие и ограждающие конструкции. - предельные состояния (R, E, I)", 
                "measurement_unit": "единица"
            },
            {
                "id": 20, 
                "name": "Обучение по пожарно-техническому минимуму (ПТМ)", 
                "measurement_unit": "1 человек"
            },
            {
                "id": 21, 
                "name": "Обучение промышленной безопасности", 
                "measurement_unit": "1 человек"
            },
            {
                "id": 22, 
                "name": "Обучение по технике безопасности и охране труда (ТБ и ОТ)", 
                "measurement_unit": "1 человек"
            },
            {
                "id": 23, 
                "name": "Обработка деревянных конструкции огнезащитным составом", 
                "measurement_unit": "1 м2"
            },
            {
                "id": 24, 
                "name": "Обработка металлических конструкции огнезащитным составом", 
                "measurement_unit": "1 м2"
            },
            {
                "id": 25, 
                "name": "Перемотка пожарных рукавов", 
                "measurement_unit": "1 шт"
            },
            {
                "id": 26, 
                "name": "Проверка на водоотдачу пожарных кранов", 
                "measurement_unit": "1 шт"
            },
            {
                "id": 27, 
                "name": "Проверка на водоотдачу пожарных гидрантов", 
                "measurement_unit": "1 шт"
            },
            {
                "id": 28, 
                "name": "Монтаж охранно-пожарных сигнализаций, видеонаблюдение",
                "measurement_unit": ""
            },
            {
                "id": 29, 
                "name": "Автоматические установки систем пожаротушения",
                "measurement_unit": ""
            },
            {
                "id": 30, 
                "name": "Разработка плана эвакуации",
                "measurement_unit": ""
            },
            {
                "id": 31, 
                "name": "Аудит в области пожарной безопасности",
                "measurement_unit": ""
            },
            {
                "id": 32, 
                "name": "Услуги по монтажу, пуско-наладке и техническому обслуживанию различных систем безопасности",
                "measurement_unit": ""
            },
            {
                "id": 33, 
                "name": "Системы периметровых средств обнаружения",
                "measurement_unit": ""
            },
            {
                "id": 34, 
                "name": "Системы охранной и пожарной сигнализации",
                "measurement_unit": ""
            },
            {
                "id": 35, 
                "name": "Системы контроля доступа",
                "measurement_unit": ""
            },
            {
                "id": 36, 
                "name": "Системы автоматического пожаротушения",
                "measurement_unit": ""
            },
            {
                "id": 37, 
                "name": "Системы оповещения",
                "measurement_unit": ""
            },
            {
                "id": 38, 
                "name": "Системы противодымной вентиляции",
                "measurement_unit": ""
            },
            {
                "id": 39, 
                "name": "Системы видеонаблюдения",
                "measurement_unit": ""
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(
                id=category_data['id'],
                defaults={
                    'name': category_data['name'],
                    'measurement_unit': category_data['measurement_unit'] or None
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'  ✓ Created category {category.id}: {category.name[:50]}...')
            else:
                # Обновляем существующую категорию, если данные изменились
                if (category.name != category_data['name'] or 
                    category.measurement_unit != (category_data['measurement_unit'] or None)):
                    category.name = category_data['name']
                    category.measurement_unit = category_data['measurement_unit'] or None
                    category.save()
                    updated_count += 1
                    self.stdout.write(f'  ↻ Updated category {category.id}: {category.name[:50]}...')
                else:
                    self.stdout.write(f'  - Category {category.id} already exists and up to date')
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('✅ Categories initialization completed!'))
        self.stdout.write('='*60)
        self.stdout.write(f'📊 Created: {created_count} categories')
        self.stdout.write(f'📊 Updated: {updated_count} categories')
        self.stdout.write(f'📊 Total categories in database: {Category.objects.count()}')
        self.stdout.write('='*60) 
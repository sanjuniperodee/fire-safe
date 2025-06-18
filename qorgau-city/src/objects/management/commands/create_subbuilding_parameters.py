from django.core.management.base import BaseCommand
from django.db import transaction
# from objects.models import (
#     Building, SubBuilding
# )
from specifications.models import (
    ExternalWallMaterialChoice, InnerWallMaterialChoice,
    RoofChoice, StairsMaterialChoice, StairsTypeChoice, LightingTypeChoice,
    VentilationTypeChoice, HeatingChoice, SecurityChoice, StairsClassificationChoice
)
from objects import (
    ObjectMainOrganizationType, MaterialOfTheExteriorWalls, LightingType, VentilationType,
    HeatingType, SecurityType, SubBuildingType, Rating, StairsClassificationType
)
import random

class Command(BaseCommand):
    help = 'Populates the database with sample SubBuilding data'

    def get_or_create_choices(self, model, choices):
        return [
            model.objects.get_or_create(name=choice)[0]
            for choice in choices
        ]

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create choices for related models
        external_wall_materials = self.get_or_create_choices(
            ExternalWallMaterialChoice, MaterialOfTheExteriorWalls.values)

        inner_wall_materials = self.get_or_create_choices(
            InnerWallMaterialChoice, ["Гипсокартон", "Штукатурка", "Кирпич", "Бетон"])

        roofs = self.get_or_create_choices(
            RoofChoice, ["Черепица", "Металл", "Мягкая кровля", "Плоская крыша"])

        stairs_materials = self.get_or_create_choices(
            StairsMaterialChoice, ["Дерево", "Бетон", "Металл", "Стекло"])

        stairs_types = self.get_or_create_choices(
            StairsTypeChoice, ["Прямая", "Г-образная", "П-образная", "Винтовая"])

        lighting_types = self.get_or_create_choices(
            LightingTypeChoice, LightingType.values)

        ventilation_types = self.get_or_create_choices(
            VentilationTypeChoice, VentilationType.values)

        heating_types = self.get_or_create_choices(
            HeatingChoice, HeatingType.values)

        security_types = self.get_or_create_choices(
            SecurityChoice, SecurityType.values)

        # Create StairsClassificationChoice objects
        stairs_classifications = self.get_or_create_choices(
            StairsClassificationChoice, [choice[0] for choice in StairsClassificationType.choices])

        self.stdout.write(self.style.SUCCESS('Successfully created sample data'))

        # Uncomment the following section if you want to create sample Buildings and SubBuildings
        """
        # Create a sample Building
        building, created = Building.objects.get_or_create(
            organization_type=ObjectMainOrganizationType.Commercial_Organizations,
            organization_name="Sample Building",
            iin="123456789012",
            defaults={
                'address': "123 Sample St, Sample City",
                'rating': Rating.ONE
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Created new Building'))
        else:
            self.stdout.write(self.style.SUCCESS('Using existing Building'))

        # Create sample SubBuildings
        for i in range(5):
            subbuilding, created = SubBuilding.objects.get_or_create(
                building=building,
                title=f"Пример Подздания {i+1}",
                defaults={
                    'subbuilding_type': random.choice(SubBuildingType.choices)[0],
                    'subbuilding_subtype': f"Подтип {i+1}",
                    'functional_purpose': f"Назначение {i+1}",
                    'date_commissioning': "2024-01-01",
                    'fire_resistance_rating': f"Рейтинг {i+1}",
                    'structural_po_class': f"Класс {i+1}",
                    'functional_po_class': f"Класс {i+1}",
                    'rating': random.choice(Rating.choices)[0],
                    'floor_number': random.randint(1, 10),
                    'total_floors': random.randint(1, 20),
                    'building_foundation': "Бетон",
                    'building_height': random.uniform(3, 50),
                    'area': random.uniform(50, 1000),
                    'volume': random.uniform(150, 5000),
                    'year_construction_reconstruction': random.randint(1950, 2024)
                }
            )

            if created:
                # Add related objects only if the SubBuilding is newly created
                subbuilding.external_walls_material.add(random.choice(external_wall_materials))
                subbuilding.inner_walls_material.add(random.choice(inner_wall_materials))
                subbuilding.roof.add(random.choice(roofs))
                subbuilding.stairs_material.add(random.choice(stairs_materials))
                subbuilding.stairs_type.add(random.choice(stairs_types))
                subbuilding.lighting.add(random.choice(lighting_types))
                subbuilding.ventilation.add(random.choice(ventilation_types))
                subbuilding.heating.add(random.choice(heating_types))
                subbuilding.security.add(random.choice(security_types))
                subbuilding.stairs_classification.add(random.choice(stairs_classifications))
                self.stdout.write(self.style.SUCCESS(f'Created new SubBuilding: {subbuilding.title}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'SubBuilding already exists: {subbuilding.title}'))
        """
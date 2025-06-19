from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from auths.models import CustomUserRole, UserRole, Category
from objects.models import Document, DocumentKey
from objects.management.commands.create_documents import Command as CreateDocumentsCommand
from objects.management.commands.create_document_keys import Command as CreateDocumentKeysCommand
from auths.management.commands.init_categories import Command as InitCategoriesCommand
import auths

User = get_user_model()

class Command(BaseCommand):
    help = 'Initialize project with all necessary data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Initializing project...'))
        
        # 1. Создаем роли
        self.create_roles()
        
        # 2. Создаем администратора
        self.create_admin()
        
        # 3. Создаем инспекторов для каждого города
        self.create_inspectors()
        
        # 4. Создаем документы и ключи документов
        self.create_documents()
        
        # 5. Создаем категории услуг
        self.create_categories()
        
        self.stdout.write(self.style.SUCCESS('✅ Project initialization completed!'))
        self.print_credentials()

    def create_roles(self):
        """Создание ролей пользователей"""
        self.stdout.write('📝 Creating user roles...')
        
        # Создаем роли из auths.Role
        for role_choice in auths.Role.choices:
            role_name, display_name = role_choice
            role, created = CustomUserRole.objects.get_or_create(
                role=role_name
            )
            if created:
                self.stdout.write(f'  ✓ Created role: {display_name}')
            else:
                self.stdout.write(f'  - Role exists: {display_name}')



    def create_admin(self):
        """Создание администратора"""
        self.stdout.write('👤 Creating admin user...')
        
        admin_phone = '+77758489538'
        admin_password = 'u4DwQw04'
        
        admin_user, created = User.objects.get_or_create(
            phone=admin_phone,
            defaults={
                'email': 'admin@qorgau.kz',
                'first_name': 'Админ',
                'last_name': 'Системы',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            }
        )
        
        if created:
            admin_user.set_password(admin_password)
            admin_user.save()
            self.stdout.write(f'  ✓ Created admin: {admin_phone}')
        else:
            self.stdout.write(f'  - Admin exists: {admin_phone}')
        
        # Добавляем роль администратора
        admin_role = CustomUserRole.objects.get(role=auths.Role.ADMIN)
        user_role, created = UserRole.objects.get_or_create(
            user=admin_user,
            role=admin_role,
            defaults={'status': auths.Status.ACCEPTED}
        )
        if created:
            self.stdout.write('  ✓ Added ADMIN role')
        else:
            self.stdout.write('  - ADMIN role already exists')

    def create_inspectors(self):
        """Создание инспекторов для каждого города"""
        self.stdout.write('👨‍💼 Creating inspectors for each city...')
        
        inspector_role = CustomUserRole.objects.get(role=auths.Role.INSPECTOR)
        cities = [
            'Алматы',
            'Нур-Султан',
            'Шымкент',
            'Актобе',
            'Тараз',
            'Павлодар',
            'Усть-Каменогорск',
            'Семей',
            'Атырау',
            'Костанай',
            'Кызылорда',
            'Уральск',
            'Петропавловск',
            'Актау',
            'Темиртау',
        ]
        
        inspector_data = []
        
        for i, city_name in enumerate(cities, 1):
            phone = f'+7775848{i:04d}'  # +77758481001, +77758481002, etc.
            password = f'inspector{i:02d}'  # inspector01, inspector02, etc.
            
            inspector, created = User.objects.get_or_create(
                phone=phone,
                defaults={
                    'email': f'inspector.{city_name.lower()}@qorgau.kz',
                    'first_name': f'Инспектор',
                    'last_name': city_name,
                    'is_active': True,
                    'inspector_jurisdiction_city': city_name,
                    'iin': f'{i:012d}',  # Уникальный 12-значный IIN
                }
            )
            
            if created:
                inspector.set_password(password)
                inspector.save()
                self.stdout.write(f'  ✓ Created inspector for {city_name}: {phone}')
            else:
                self.stdout.write(f'  - Inspector exists for {city_name}: {phone}')
            
            # Добавляем роль инспектора
            user_role, role_created = UserRole.objects.get_or_create(
                user=inspector,
                role=inspector_role,
                defaults={'status': auths.Status.ACCEPTED}
            )
            if role_created:
                self.stdout.write(f'    ✓ Added INSPECTOR role')
            else:
                self.stdout.write(f'    - INSPECTOR role already exists')
            
            inspector_data.append({
                'city': city_name,
                'phone': phone,
                'password': password,
                'email': inspector.email
            })
        
        # Сохраняем данные инспекторов для README
        self.inspector_credentials = inspector_data

    def create_documents(self):
        """Создание документов и ключей документов"""
        self.stdout.write('📋 Creating documents and document keys...')
        
        # Создаем документы
        if not Document.objects.exists():
            create_docs_command = CreateDocumentsCommand()
            create_docs_command.handle()
            self.stdout.write('  ✓ Created documents')
        else:
            self.stdout.write('  - Documents already exist')
        
        # Создаем ключи документов
        if not DocumentKey.objects.exists():
            create_keys_command = CreateDocumentKeysCommand()
            create_keys_command.handle()
            self.stdout.write('  ✓ Created document keys')
        else:
            self.stdout.write('  - Document keys already exist')

    def create_categories(self):
        """Создание категорий услуг"""
        self.stdout.write('📋 Creating service categories...')
        
        # Создаем категории
        if not Category.objects.exists():
            init_categories_command = InitCategoriesCommand()
            init_categories_command.handle()
            self.stdout.write('  ✓ Created service categories')
        else:
            self.stdout.write('  - Service categories already exist')

    def print_credentials(self):
        """Вывод учетных данных"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('🔑 УЧЕТНЫЕ ДАННЫЕ СИСТЕМЫ'))
        self.stdout.write('='*60)
        
        self.stdout.write('\n👤 АДМИНИСТРАТОР:')
        self.stdout.write('  Телефон: +77758489538')
        self.stdout.write('  Пароль: u4DwQw04')
        self.stdout.write('  Email: admin@qorgau.kz')
        
        self.stdout.write('\n👨‍💼 ИНСПЕКТОРЫ ПО ГОРОДАМ:')
        for inspector in self.inspector_credentials:
            self.stdout.write(f"  {inspector['city']}:")
            self.stdout.write(f"    Телефон: {inspector['phone']}")
            self.stdout.write(f"    Пароль: {inspector['password']}")
            self.stdout.write(f"    Email: {inspector['email']}")
        
        self.stdout.write('\n📊 СТАТИСТИКА:')
        self.stdout.write(f"  Ролей: {CustomUserRole.objects.count()}")
        self.stdout.write(f"  Назначений ролей: {UserRole.objects.count()}")
        self.stdout.write(f"  Пользователей: {User.objects.count()}")
        self.stdout.write(f"  Документов: {Document.objects.count()}")
        self.stdout.write(f"  Ключей документов: {DocumentKey.objects.count()}")
        self.stdout.write(f"  Категорий услуг: {Category.objects.count()}")
        
        self.stdout.write('\n' + '='*60) 
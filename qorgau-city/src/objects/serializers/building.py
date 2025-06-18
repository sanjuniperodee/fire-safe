from rest_framework import serializers
from objects.models.document import Document, OrganizationType

from auths.serializers import (
    InspectorSerializer,
    UserShortSerializer
)
from objects.models import (
    Building,
    Document,
    BuildingRemark,
    DocumentKey,
    DocumentKeyFile,
    DocumentComment,

    DocumentRemark,

    BuildingPDFDocument,
)

from .escape_ladder import EscapeLadderImageSerializer
from .document import DocumentListSerializer
from .image import BuildingImageSerializer
from .subbuilding import SubBuildingSerializer


class BuildingCreateSerializer(serializers.ModelSerializer):
    owner = UserShortSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    # Принимаем строку, ищем OrganizationType по name
    organization_type = serializers.CharField(required=True)

    class Meta:
        model = Building
        fields = (
            'id',
            'organization_type',         # Получаем строку, храним ForeignKey
            'organization_sub_type',     # Остается обычное текстовое поле
            'organization_characteristics',
            'organization_optional_type',
            'organization_name',
            'iin',
            'owner',
            'address',
            'rating',
            'created_at',
            'escape_ladder',
        )

    def validate_organization_type(self, value):
        """Принимаем строку, ищем OrganizationType по name. Создаем если не найден."""
        try:
            org_type = OrganizationType.objects.get(name=value)
        except OrganizationType.DoesNotExist:
            # Автоматически создаем тип организации если не найден
            org_type = OrganizationType.objects.create(
                name=value,
                # Можно добавить другие поля по умолчанию если нужно
            )
            print(f"Created new organization type: {value}")
        return org_type

    def create(self, validated_data):
        """
        1) Забираем объект OrganizationType из валидации
        2) Создаем Building, устанавливая organization_type=org_type_obj
        3) Добавляем документы, которые поддерживают org_type_obj (через ManyToMany)
        """
        org_type_obj = validated_data.pop('organization_type', None)

        # Создаем Building с найденным OrganizationType
        building = Building.objects.create(
            organization_type=org_type_obj,
            **validated_data
        )

        # Если хотите обернуть organization_name в кавычки (как в вашем примере)
        building.organization_name = f'"{building.organization_name}"'
        building.save()

        # Фильтруем только документы, у которых в supported_organization_types есть org_type_obj
        documents_data = Document.objects.all()
        supported_docs = DocumentKey.objects.filter(supported_organization_types=org_type_obj)
        building.documents.add(*documents_data)
        building.document_keys.add(*supported_docs)

        return building


class BuildingListSerializer(serializers.ModelSerializer):
    owner = UserShortSerializer()
    inspector = InspectorSerializer()
    images = BuildingImageSerializer(many=True, read_only=True)
    escape_ladder_images = EscapeLadderImageSerializer(many=True, read_only=True)

    class Meta:
        model = Building
        fields = (
            'id',
            'organization_type',
            'organization_sub_type',
            'organization_characteristics',
            'organization_optional_type',
            'organization_name',
            'iin',
            'owner',
            'inspector',
            'address',
            'rating',
            'created_at',
            'images',
            'escape_ladder',
            'escape_ladder_images',
        )

        def to_representation(self, instance):
                """
                Изменяем представление поля organization_type, чтобы возвращать name вместо ID.
                """
                representation = super().to_representation(instance)
                if instance.organization_type:
                    # Заменяем organization_type на название типа организации
                    representation['organization_type'] = instance.organization_type.name
                return representation



class BuildingDetailSerializer(serializers.ModelSerializer):
    owner = UserShortSerializer()
    inspector = InspectorSerializer()
    escape_ladder_images = EscapeLadderImageSerializer(many=True, read_only=True)

    class Meta:
        model = Building
        fields = (
            'id',
            'organization_type',           # str field
            'organization_sub_type',       # FK -> OrganizationType
            'organization_characteristics',
            'organization_optional_type',
            'organization_name',
            'iin',
            'owner',
            'inspector',
            'address',
            'rating',
            'created_at',
            'documents',       # M2M -> Document
            'escape_ladder',
            'escape_ladder_images',
        )

    def to_representation(self, instance):
        # Базовая сериализация полей (из fields)
        representation = super().to_representation(instance)

        # Пример, если нужно дополнительно отдать sub_type_name
        # if instance.organization_sub_type:
        #     representation['organization_sub_type_name'] = instance.organization_sub_type.name
        # else:
        #     representation['organization_sub_type_name'] = None

        # --- Собираем информацию о документах (главы) и их "ключах" ---
        document_data_map = {}
        info = []

        # Проходим по всем Document, которые хранятся в building.documents
        for document in instance.documents.all():
            # Фильтруем DocumentKey ТОЛЬКО те, что реально привязаны к building через building.document_keys
            allowed_keys = document.keys.filter(
                pk__in=instance.document_keys.values_list('pk', flat=True)
            )

            keys_data = []
            for key in allowed_keys:
                # Ищем файлы, которые привязаны к этому building и конкретному document_key
                files = [
                    {"id": item.id, "name": item.name}
                    for item in DocumentKeyFile.objects.filter(
                        building=instance, document_key=key
                    )
                ]
                # Ищем замечания/комментарии инспектора (DocumentRemark) к этому key для данного building
                inspector_comment_obj = DocumentRemark.objects.filter(
                    building=instance, document_key=key
                )
                if inspector_comment_obj.exists():
                    latest_remark = inspector_comment_obj.latest('created_at')
                    inspector_comment = latest_remark.content
                    inspector_comment_updated_date = latest_remark.updated_at
                else:
                    inspector_comment = ''
                    inspector_comment_updated_date = None

                # Ищем обычные комментарии (DocumentComment) к этому key для данного building
                comment_obj = DocumentComment.objects.filter(
                    building=instance, document_key=key
                )
                if comment_obj.exists():
                    latest_comment = comment_obj.latest('created_at')
                    comment = latest_comment.body
                    comment_updated_date = latest_comment.updated_at
                else:
                    comment = ''
                    comment_updated_date = None

                keys_data.append({
                    "id": key.id,
                    "title": key.title,
                    "comment": comment,
                    "comment_updated_date": comment_updated_date,
                    "inspector_comment": inspector_comment,
                    "inspector_comment_updated_date": inspector_comment_updated_date,
                    "files": files,
                })

            # Собираем результат для каждой Document
            document_data_map[document.id] = {
                'id': document.id,
                'title': document.title,
                'keys': keys_data
            }

        # Если нужно, поддерживаем иерархию "глава -> subParagraphs"
        for document in instance.documents.all():
            if document.parent_id and document.parent_id in document_data_map:
                parent_data = document_data_map[document.parent_id]
                # сам дочерний документ
                child_doc = document_data_map.pop(document.id, None)
                if child_doc:
                    parent_data.setdefault('subParagraphs', []).append(child_doc)

        # Преобразуем document_data_map в список
        for doc_data in document_data_map.values():
            info.append(doc_data)

        # --- Подздания ---
        subbuildings_list = instance.subbuildings.all()
        subbuildings_data = SubBuildingSerializer(subbuildings_list, many=True).data

        # Документы "верхнего уровня" (уже разобранные в info)
        documents_data = DocumentListSerializer(info, many=True).data

        # Добавляем новые ключи в результирующее представление
        representation['subbuildings'] = subbuildings_data
        representation['documents'] = documents_data

        return representation


class BuildingPDFDocumentSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = BuildingPDFDocument
        fields = ('id', 'created_at', 'download_url')

    def get_download_url(self, obj):
        request = self.context.get('request')
        if request and obj.file:
            return request.build_absolute_uri(obj.file.url)
        return None
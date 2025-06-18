from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_alpha(value):
    if not all(char.isalpha() or char.isspace() for char in value):
        raise ValidationError(_('Для ввода разрешены только буквы.'))


def validate_multilingual(value):
    allowed_languages = ['ru', 'en', 'kz']

    language_chars = set(char.lower() for char in value if char.isalpha())
    if not any(lang_chars.issubset(language_chars) for lang_chars in allowed_languages):
        raise ValidationError(_('Ввод поддерживается для следующих языков: казахский, русский, английский.'))


def validate_file_extension(value):
    allowed_extensions = ['png', 'jpg', 'jpeg']
    extension = value.name.split('.')[-1].lower()
    if extension not in allowed_extensions:
        raise ValidationError(_('Поддерживается добавление изображений для расширений: png, jpg, jpeg.'))


def validate_files_extension(value):
    allowed_extensions = ['png', 'jpg', 'jpeg', 'mp4', 'mov', 'avi']
    extension = value.name.split('.')[-1].lower()
    if extension not in allowed_extensions:
        raise ValidationError(
            _('Поддерживается добавление изображений/видео для расширений: png, jpg, jpeg, mp4, mov, avi.'))


def validate_documents_extension(value):
    allowed_extensions = ['png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx', 'tiff', 'bmp']
    extension = value.name.split('.')[-1].lower()
    if extension not in allowed_extensions:
        raise ValidationError(_(
            'Поддерживается добавление файлов для расширений: '
            'png, jpg, jpeg, pdf, doc, docx, tiff, bmp.'
        ))

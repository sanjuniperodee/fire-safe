import os
import base64
import mimetypes
from django.http import HttpResponse

# from rest_framework.views import APIView


class BaseViewSet:
    def get_header_with_file(self, docx_file_path):
        with open(docx_file_path, 'rb') as docx_file:
            encoded_file = base64.b64encode(docx_file.read()).decode('utf-8')
            mimetype, _ = mimetypes.guess_type(docx_file_path)

            try:
                response = HttpResponse(encoded_file, content_type=mimetype)
            except TypeError:
                response = HttpResponse(docx_file.read(),
                                        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(docx_file_path)}"'
            os.remove(docx_file_path)

            return response

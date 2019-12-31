from rest_framework.serializers import ModelSerializer
from .models import Documents

class DocumentPatientSerializer(ModelSerializer):

    class Meta:
        model = Documents
        fields = [
            'document_id',
            'documents'
        ]
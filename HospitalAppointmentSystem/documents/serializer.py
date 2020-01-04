from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import Documents

class DocumentPatientSerializer(ModelSerializer):
    name = SerializerMethodField()
    class Meta:
        model = Documents
        fields = [
            'document_id',
            'documents',
            'name'
        ]

    def get_name(self, obj):
        name =  obj.documents.name
        name = name.split('/')
        name =  name[1]
        l = name.split('_')
        l[-1]=''
        res = "".join(l)
        return res
from .models import *
from rest_framework.serializers import ModelSerializer


class AppDetailSerailizer(ModelSerializer):
    
    class Meta:
        model = AppDetail
        fields = ('Application', 'appEndPoint',)
        
class InterfaceSerailizer(ModelSerializer):

    class Meta:
        model = Interface
        fields = ('target', 'status', 'message')

class AppDataSerailizer(ModelSerializer):

    application = AppDetailSerailizer(many=False, read_only=True)
    targets = InterfaceSerailizer(many=True, read_only=True)

    class Meta:
        model = AppData
        fields = ('application', 'status', 'targets',)
        depth = 1  

class AppDataLoadSerializer(ModelSerializer): 
    class Meta:
        model = AppData
        fields = ('application', 'status',)
        
class InterfaceLoadSerailizer(ModelSerializer):
    class Meta:
        model = Interface
        fields = ('target', 'status', 'message', 'targets',)
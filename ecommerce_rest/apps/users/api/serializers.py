from rest_framework import serializers
from apps.users.models import User

#El serializador sirve para hacer consultas/escrituras en la base de datos, y traerlas como response.
#Ya que al tratarse de un orm, lo traduce de alguna manera a codigo sql.
#?Tambien para tratar la informacion de la request, ya que este trabajo debe hacerlo el serializador y no la vista.
#Usamos modelSerializer porque nuestro serializador esta basado en un modelo llamado "User"
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
    def create(self, validated_data):
        user = User(**validated_data)
        #Encriptamos contraseña:
        user.set_password(validated_data['password'])
        user.save()
        print('usuario creado correctamente! serializers/19')
        return user
    
    def update(self, instance, validated_data):
        #super es el constructor
        update_user = super().update(instance, validated_data)
        update_user.set_password(validated_data['password'])
        update_user.save()
        
        print('usuario actualizado correctamente! serializers/28')
        return update_user
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        
    #?to_representation es para modificar la forma en la que nos muestra los registros
    #Si no queremos modificar la manera, va a tomar "fields" de arriba.
    #aqui podemos hacer un return {id:instance['id'],etc}
    #Luego en objects.values('id'), asi especificamos que campos queremos que se vean cuando hacemos un GET.
    #Esto sirve por ej si el cliente nos pide que quiere que en vezde username sea user_name
    #Se utiliza instance['id'] cuando usamos values, si es objects.all o filter, debemos usar instance.id 
    
    # def to_representation(self, instance):
    #     print(instance)
    #     return {}        
    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'nombre_usuario': instance['username'],
            'correo': instance['email'],
            'contraseña': instance['password']
        }
        
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
class InputSerializer(serializers.Serializer): 
    username  = serializers.CharField()
    email     = serializers.EmailField()
    password  = serializers.CharField()
    name      = serializers.CharField()
    last_name = serializers.CharField()
    is_active = serializers.BooleanField(default = True)
    is_staff  = serializers.BooleanField(default = True)
    
#aca usamos serializers.Serializer porque puede estar basado en un modelo como no lo puede, como vamos a ver a continuacion:
#Que campos hay en un serializador sin modelo? Existen todos los campos que hay en un serializador, asi de sencillo.

class TestUserSerializer(serializers.Serializer):
    name  = serializers.CharField(max_length = 200)
    email = serializers.EmailField()
    
    # Aquí podemos hacer metodos "caseros", se escribe validate_nombredelcampo y hacemos la validacion que querramos para el mismo.
    def validate_name(self,value):
        #! self.context es toda la data enviada en la request.
        #validacion customizada.
        if 'leansilva' in value:
            raise serializers.ValidationError('El nombre lean no puede ser utilizado.')
        return value
    
    def validate_email(self,value):
        if value == '':
            raise serializers.ValidationError('El campo no puede estar vacio.')
        return value
    
    def validate(self, data):
        if data['name'] in data['email']:
            raise serializers.ValidationError("El nombre no se debe encontrar en el email")
        print('Finalmente paso todas las validaciones.')
        return data
    
    #Luego de las validaciones, pasa al metodo "create"
    #Las validaciones se ejecutan tanto para actualizar tanto como para crear.
    
    #cuando hacemos Test(**validated_data) estamos asignando los valores del objeto en el orden que esté, a un modelo de una clase por ej "Test"
    def create(self, validated_data):
        #Usamos el modelo User,accedemos a su manager "objects" le decimos que cree al usuario, con los datos validados previamente
        #Esto se traduce a codigo sql mediante el ORM de django.
        #devuelve la instancia
        return User.objects.create(**validated_data)
        # return super().create(validated_data)
        
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
        # return super().update(instance, validated_data)
        
    # #Podemos sobreescrivir el metodo save
    # def save(self, **kwargs):
    #     #Aqui podemos enviar un email por ejemplo, una vez que se registra alguien en la base de datos.
    #     return super().save(**kwargs)
    
    #Es mejor sobreescrivir el metodo save del Modelo y no del Serializador.
    #Ya que primero se ejecutaria el metodo "save" del model y luego del serializador, asi no modificamos la escritura en la db
from rest_framework import generics

class GeneralListAPIView(generics.ListAPIView):
    serializer_class = None
    
    #Esto es para evitar repetir codigo en los serializadores, y generalizar los get donde el estado es True.
    def get_queryset(self):
        model = self.get_serializer().Meta.model
        return model.objects.filter(state = True)
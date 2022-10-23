from .models import UsersProf
from .serializers import UserSerializer
from rest_framework.generics import ListAPIView
# Create your views here.
class UserViews(ListAPIView):
    queryset = UsersProf.objects.all()
    serializer_class = UserSerializer
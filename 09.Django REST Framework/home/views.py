from rest_framework.decorators import api_view  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.views import APIView  # type: ignore
from rest_framework import viewsets # type: ignore
from rest_framework import status # type: ignore
from home.models import Person
from home.serializers import LoginSerializer, PeopleSerializer, RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token # type: ignore

# Create your views here.
class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors,
            },   status.HTTP_400_BAD_REQUEST)

        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        if not user:
            return Response({
                'status': False,
                'message': 'Invalid username or password',
            },   status.HTTP_400_BAD_REQUEST)
        
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
                'status': True,
                'message': 'User Logged Inn',
                'token': str(token),
            },  status.HTTP_201_CREATED) 



class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors,
            },   status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
                'status': True,
                'message': 'User Created',
            },  status.HTTP_201_CREATED)

@api_view(['GET', 'POST', 'PUT'])
def index(request):
    courses = {
        "course_name": "Python",
        "learning": ["Flask", "Django", "Tornado", "FastAPI"],
        "course_provider": "Scaler"
    }
    if request.method == "GET":
        print("YOU HIT A GET METHOD")
        return Response(courses)
    elif request.method == "POST":
        data = request.data
        print("********************************")
        print(data)
        print("********************************")
        print("YOU HIT A POST METHOD")
        return Response(courses)
    elif request.method == "PUT":
        print("YOU HIT A PUT METHOD")
        return Response(courses)


@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data=data)
    if serializer.is_valid():
        data = serializer.validated_data
        print(data)
        return Response({"message": "Success"})
    return Response(serializer.errors)

# *************** CRUD methods using SERIALIZERS in Django REST Framework *****************
# Class-Based views for Person model
class PersonAPI(APIView):
    def get(self, request):
        objs = Person.objects.filter(color__isnull=False)
        serializer = PeopleSerializer(objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])  # Fetch the existing object
        serializer = PeopleSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])  # Fetch the existing object
        serializer = PeopleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({"message": "Person object deleted"}, status=status.HTTP_200_OK)


# *************** CRUD methods using SERIALIZERS in Django REST Framework *****************
# Function-Based views for Person model
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == "GET":
        objs = Person.objects.filter(color__isnull=False)
        serializer = PeopleSerializer(objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":  # put doesn't support partial update
        data = request.data
        obj = Person.objects.get(id=data['id'])  # Fetch the existing object
        serializer = PeopleSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":  # patch supports partial update
        data = request.data
        obj = Person.objects.get(id=data['id'])  # Fetch the existing object
        serializer = PeopleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({"message": "Person object deleted"}, status=status.HTTP_200_OK)


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)

        serializer = PeopleSerializer(queryset, many=True)
        return Response({"status": 200, "data":serializer.data})
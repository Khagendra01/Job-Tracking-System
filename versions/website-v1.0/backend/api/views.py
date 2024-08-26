from rest_framework import generics
from .serializers import UserSerializer, JobSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Job
from rest_framework_simplejwt.views import TokenObtainPairView
from django.test import RequestFactory
from .tasks import fetch_job_updates
from django.contrib.auth import get_user_model

User = get_user_model()

class JobListCreate(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Job.objects.filter(author=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class JobDelete(generics.DestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Job.objects.filter(author=user)

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Store request data to reuse later
        data = request.data
        username = data.get('username')
        password = data.get('password')

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            # Create a new HttpRequest for token generation without re-accessing the body
            factory = RequestFactory()
            token_data = {'username': username, 'password': password}
            token_request = factory.post('/api/token/', token_data)

            # Set session and other request attributes if needed
            token_request.user = request.user
            token_request.session = request.session

            #run celery here
            fetch_job_updates.delay(username, password)

            # Call the token view directly with the HttpRequest object
            token_view = TokenObtainPairView.as_view()
            return token_view(token_request, *args, **kwargs)

        # If user doesn't exist, proceed with normal registration
        return super().post(request, *args, **kwargs)
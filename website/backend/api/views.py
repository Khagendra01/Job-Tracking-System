from rest_framework import generics
from .serializers import UserSerializer, JobSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Job
from rest_framework_simplejwt.views import TokenObtainPairView
from django.test import RequestFactory
from .tasks import fetch_job_updates
from django.contrib.auth import get_user_model
import imaplib
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()

def is_OK(user, password):
    try:
        imap_url = 'imap.gmail.com'
        with imaplib.IMAP4_SSL(imap_url) as my_mail:
            my_mail.login(user, password)
        return True
    except (imaplib.IMAP4.error, Exception) as e:
        print(f"Error validating credentials: {e}")
        return False  

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

            #run celery here
            fetch_job_updates.delay(username, password)

            # Call the token view directly with the HttpRequest object
            token_view = TokenObtainPairView.as_view()
            return token_view(token_request, *args, **kwargs)
        else:
            response = super().create(request, *args, **kwargs)
            
            # If user creation was successful, generate token
            if response.status_code == 201:
                # Create a new HttpRequest for token generation
                factory = RequestFactory()
                token_data = {'username': username, 'password': password}
                token_request = factory.post('/api/token/', token_data)

                # Run celery task
                fetch_job_updates.delay(username, password)

                # Call the token view directly with the HttpRequest object
                token_view = TokenObtainPairView.as_view()
                return token_view(token_request, *args, **kwargs)
            
            return response

class UpdateUserView(APIView):
    def patch(self, request, username):
        user = User.objects.get(username=username)
        get_pa = request.data.get('web_pa')
        if is_OK(username, get_pa):
            user.web_pa = get_pa
            user.save()
            return Response({'message': 'okay'})
        else:
            return Response({'message': 'Password does not match! please try again'})
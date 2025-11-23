from rest_framework_simplejwt import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain JWT token pair.
    You can extend this class to add custom claims or modify the response.
    """
    pass


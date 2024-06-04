from django.urls import path
from .views import *

urlpatterns = [
    path('', Login.as_view(), name='Login'),
    path('Register/', Register.as_view(), name='Register'),
    path('Home/', Home.as_view(), name='Home'),
    path('Delete/<int:id>/', Delete, name='Delete'),
    path('Delete_Document/<int:id>/', Delete_Document, name='Delete_Document'),
    path('download/<int:pk>/', Dowload_Document.as_view(), name='file_download'),
    path('Post/', Post.as_view(), name='Post'),
    path('Document/', Document.as_view(), name='Document'),
    path('Logout/', Logout, name='Logout')
]

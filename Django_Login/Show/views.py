from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from .models import Model_Post, Model_File
from django.shortcuts import get_object_or_404
from django.http import FileResponse

# Create your views here.
class Login(View):
    def get(self, request):
        return render(request, 'Login.html')
    def post(self, request):
        if request.method == "POST":
            username = request.POST.get('UserName')
            Password = request.POST.get('Password')
            user = authenticate(username=username, password=Password)
            if user is not None:
                login(request, user)
                messages_ = username
                return redirect('/Home/', {'messages':username})
            else:
                try:
                    # Kiểm tra điều kiện tên người dùng nhập vào có tồn tại hay không
                    User.objects.get(username=username)
                    # Nếu người dùng có tồn tại, nhưng mật khẩu sai ==> Reload lại trang web để người dùng đăng nhập lại
                    messages.error(request, "Sai thông tin đăng nhập!!!!")
                    return redirect('/')
                except User.DoesNotExist:
                    messages.error(request, "Không tồn tại tài khoản này")
                    return redirect('/')

class Register(View):
    def get(self, request):
        return render(request, 'Register.html')
    def post(self, request):
        if request.method == "POST":
            Username = request.POST.get('Username')
            Email = request.POST.get('Email')
            Password = request.POST.get('Password')
            Conf_Password = request.POST.get('Conf_Password')
            if User.objects.filter(username=Username):
                messages.error(request, "Tài khoản đã tồn tại! Hãy đăng ký tài khoản khác")
                return render(request, 'Register.html')
            if User.objects.filter(email=Email).exists():
                messages.error(request, "Email đã tồn tại")
                return render(request, 'Register.html')
            if Password!=Conf_Password:
                messages.error(request, "Mật khẩu không khớp!")
                return render(request, 'Register.html')
            MyUser = User.objects.create_user(Username, Email, Password)
            print(Username, Email, Password)
            MyUser.save()
            return redirect('/')
        return render(request, 'Register.html')
            

class Home(View):
    def get(self, request):
        All_Post = Model_Post.objects.all()
        return render(request, 'Home.html', {'All_Post':All_Post})

class Document(View):
    def get(self, request):
        Doc = Model_File.objects.all()
        return render(request, 'Document.html', {'Doc':Doc})
    def post(self, request):
        if request.method == 'POST':
            author = request.user
            file = request.FILES.get('formFile')
            image = request.FILES.get('image')
            name = request.POST.get('Name')
            name_author = request.POST.get('Author')
            print(file)
            save = Model_File(author=author, file=file, image=image, name=name, name_author=name_author)
            save.save()
            return redirect('/Document/')

class Dowload_Document(View):
    def get(self, request, pk):
        file_model = get_object_or_404(Model_File, pk=pk) # Dùng để lấy đối tượng Model_File từ cơ sở dữ liệu với khóa chính là pk. Nếu không tìm thấy đối tượng, nó sẽ trả về trang 404 (Page Not Found).
        file_path = file_model.file.path # Lấy đường dẫn đến tệp tin từ trường file của đối tượng Model_File. Đây là đường dẫn tuyệt đối đến tệp tin trên hệ thống tệp của máy chủ.
        response = FileResponse(open(file_path, 'rb')) # Tạo một đối tượng để trả về nội dung của tệp tin, thực hiện mở nội dung tệp tin ở chế độ đọc
        response['Content-Type'] = 'application/octet-stream' # Thiết lập nội dung phản hồi để báo trình duyệt xử lý dữ liệu tải xuống thay vì để hiển thị dữ liệu trực tiếp trên trình duyệt
        response['Content-Disposition'] = f'attachment; filename="{file_model.file.name}"' # Lấy tệp tin tải xuống, đặt tên cho tệp tin tải xuống là tên của file đó
        return response # Điều này thực hiện báo cho trình duyệt người dùng tải xuống

def Delete(request, id):
    if request.method == 'POST':
        id_delete = Model_Post.objects.get(pk=id)
        id_delete.delete()
        return redirect('Home')

def Delete_Document(request, id):
    if request.method == 'POST':
        id_delete = Model_File.objects.get(pk=id)
        id_delete.delete()
        return redirect('/Document/')
    
class Post(View):
    def get(self, request):
        return render(request, 'Post.html')
    def post(self, request):
        if request.method == 'POST':
            author = request.user
            image = request.FILES.get('image')
            title = request.POST.get('title')
            Description = request.POST.get('description')
            print(f'Auther: {author}, image: {image}, title: {title}, Description: {Description}')
            save = Model_Post(author=author, image=image, title=title, description=Description)
            save.save()
            return redirect('/Post/')

def Logout(request):
    logout(request)
    return redirect('/')
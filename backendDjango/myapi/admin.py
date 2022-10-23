from django.contrib import admin
from .models import UsersProf
# Register your models here.
@admin.register(UsersProf)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email']

    # ab humara admin me ye list dikhega Userprof ka , ab ise migrate kar sakte hai taki admin pannel pe dikhe.

    # ab UserProf Model ka table create karne k liye "python manage.py makemigrations" karne per Model migratin ho jayega or humara is model ka migration file generate ho jata hai.
 
    # ab migrate file se ise migrate karna hai to "python manage.py migrate" ye karne se humara table create ho jayga 

    # Ab ek Admin create karna hai uske liye "python manage.py createsuperuser"
    # ab server run "pyhton manage.py runserver" http://127.0.0.1:8000/admin/
    
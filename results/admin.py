from django.contrib import admin

from .models import User
from .models import Organization
from .models import Faculty
from .models import Cathedra
from .models import Sport_competition
from .models import Norm_gto
from .models import Results_sport_competition

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from results.models import Student
from results.models import Instructor

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'student'

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class InstructorInline(admin.StackedInline):
    model = Instructor
    can_delete = False
    verbose_name_plural = 'instructor'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    BaseUserAdmin.fields
    inlines = (StudentInline, InstructorInline)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)



#admin.site.register(Instructor)
admin.site.register(Organization)
admin.site.register(Faculty)
admin.site.register(Cathedra)
admin.site.register(Sport_competition)
admin.site.register(Norm_gto)
admin.site.register(Results_sport_competition)

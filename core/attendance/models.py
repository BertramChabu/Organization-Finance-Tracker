# from django.db import models
# from django.utils import timezone
# from users.models import User  # assuming teachers and deputies are from here
# from timetable.models import Class  # class the teacher is supposed to attend

# class TeacherAttendance(models.Model):
#     class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
#     date = models.DateField(default=timezone.now)
#     attended = models.BooleanField(default=False)
#     recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'deputy'})

#     class Meta:
#         unique_together = ('class_instance', 'date')  # prevent duplicate entries

from operator import attrgetter


student_attendance = {"Rolf": 96, "Bob": 80, "Anne": 100}

for student, attendance in student_attendance.items():
    print(f"{student}: {attendance}") 
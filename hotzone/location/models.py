from django.db import models

class Virus(models.Model):
    virus = models.CharField(max_length=20, unique=True)
    disease = models.CharField(max_length=20)
    inf_period = models.IntegerField()
    def __str__(self):
        return self.virus

class Locations(models.Model):
    place_name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=200)
    x_coord = models.FloatField()
    y_coord = models.FloatField()
    def __str__(self):
        return self.place_name

class Patient(models.Model):
    name = models.CharField(max_length=200)
    id_num = models.CharField(max_length=10, unique=True)
    birth_date = models.DateField()
    def __str__(self):
        return self.name

case_class_choice = [
    ("Local", "Local"),
    ("Imported", "Imported"),
]

category_choice = [
    ("Residence", "Residence"),
    ("Workplace", "Workplace"),
    ("Visit", "Visit"),
]

class Case(models.Model):
    class Meta:
        unique_together = (('infection', 'case_num'),)
    case_num = models.IntegerField()
    confirm_date = models.DateField()
    case_class = models.CharField(max_length=10, choices=case_class_choice)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    infection = models.ForeignKey(Virus, on_delete=models.CASCADE)
    visited = models.ManyToManyField(Locations, through="Visit_Info")
    def __str__(self):
        return f'{self.infection} Case {self.case_num}'

class Visit_Info(models.Model):
    case_visit = models.ForeignKey(Case, on_delete=models.CASCADE)
    location_visit = models.ForeignKey(Locations, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()
    category = models.CharField(max_length=20, choices=category_choice)
    def __str__(self):
        return f'{self.case_visit} visited {self.location_visit}'
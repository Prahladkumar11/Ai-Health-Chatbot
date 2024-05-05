from django.db import models

class HeartDiseaseData(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    age = models.IntegerField()
    sex = models.IntegerField()  # Assuming 0 for female and 1 for male
    cp = models.IntegerField()
    trestbps = models.IntegerField()
    chol = models.IntegerField()
    fbs = models.IntegerField()
    restecg = models.IntegerField()
    thalach = models.IntegerField()
    exang = models.IntegerField()
    oldpeak = models.FloatField()
    slope = models.IntegerField()
    ca = models.IntegerField()
    thal = models.IntegerField()
    target = models.IntegerField()

    def __str__(self):
        return f"Age: {self.age}, Sex: {self.sex}, CP: {self.cp}, Target: {self.target}"


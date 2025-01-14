from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class PPG(models.Model):
    date = models.DateTimeField('date inserted')
    time_stamp = models.IntegerField(default=0)
    ppg_signal = models.FloatField(default=0.0)

class Measures(models.Model):
    android_id = models.CharField(max_length=50, null=True)
    bpm = models.FloatField(default=-1, null=False)
    ibi = models.FloatField(default=-1, null=False)
    sdnn = models.FloatField(default=-1, null=False)
    sdsd = models.FloatField(default=-1, null=False)
    rmssd = models.FloatField(default=-1, null=False)
    pnn20 = models.FloatField(default=-1, null=False)
    pnn50 = models.FloatField(default=-1, null=False)
    hr_mad = models.FloatField(default=-1, null=False)
    sd1 = models.FloatField(default=-1, null=False)
    sd2 = models.FloatField(default=-1, null=False)
    s = models.FloatField(default=-1, null=False)
    sd1_sd2 = models.FloatField(default=-1, null=False)
    breathingrate = models.FloatField(default=-1, null=False)
    vlf = models.FloatField(default=-1, null=False)
    lf = models.FloatField(default=-1, null=False)
    hf = models.FloatField(default=-1, null=False)
    lf_hf = models.FloatField(default=-1, null=False)
    p_total = models.FloatField(default=-1, null=False)
    vlf_perc = models.FloatField(default=-1, null=False)
    lf_perc = models.FloatField(default=-1, null=False)
    hf_perc = models.FloatField(default=-1, null=False)
    lf_nu = models.FloatField(default=-1, null=False)
    hf_nu = models.FloatField(default=-1, null=False)
    timeStamp = models.DateTimeField(default=timezone.now, null=False)

    #Django 的 FloatField 类型对应 SQLite 的 NUMERIC 数据类型

    def __str__(self):
        return f"Measures object - ID: {self.id}"

    class Meta:
        db_table = 'measures'

        #将数据库表名定义为measures



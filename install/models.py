from django.db import models

# Create your models here.


class Scanner(models.Model):
    '''
    一个扫描器
    这个以后留作扩展，先只有token字段
    '''
    token = models.CharField(max_length=40)


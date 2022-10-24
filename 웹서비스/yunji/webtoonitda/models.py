from django.db import models

# Create your models here.
class Webtoon(models.Model):
    lang = models.CharField(max_length=100 , verbose_name="언어")
    platform = models.CharField(max_length=100, verbose_name="플랫폼")
    webtoon = models.CharField(max_length=100, verbose_name="웹툰")

    # page title	 point	participant
    # page = models.IntegerField(verbose_name="페이지번호")
    # title = models.CharField(max_length=100 , verbose_name="제목")
    #
    # # 표현할 수 있는 숫자의 수(max_digits)와 소수점 위치(decimal_places)를 지정
    # point = models.DecimalField( max_digits=3, decimal_places=2,verbose_name="평점")
    #
    # participant = models.IntegerField( verbose_name="참여자수")

    def __str__(self):
        return self.webtoon

    class Meta:
        db_table = 'Webtoon'
        verbose_name = "Webtoon"  #관리자페이지에 모델 관리에 표시되는 이름
        verbose_name_plural = "Webtoon"   #기본적으로 영어기준 복수로 모델명이 표시가 되므로

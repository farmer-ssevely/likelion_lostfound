from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
# Create your models here.

places = (('경영관', '경영관'), ('공학원', '공학원'), ('공A', '제1공학관'), ('공B', '제2공학관'), ('공C', '제3공학관'), ('과학관', '과학관'), ('과학원', '과학원'), ('광복관', '광복관'), ('교육과학관', '교육과학관'), ('대강당', '대강당'), ('대우관', '대우관'), ('무악1학사', '무악1학사'), ('무악2학사', '무악2학사'), ('무악3학사', '무악3학사'), ('무악4학사', '무악4학사'), ('미우관', '미우관'), ('백양관', '백양관'), ('백양누리', '백양누리'), ('백주년기념관', '백주년기념관'), ('빌링슬리관', '빌링슬리관'), ('삼', '삼성관'), ('상남경영원', '상남경영원'), ('성암관', '성암관'), ('스팀슨관', '스팀슨관'), ('스포츠과학관', '스포츠과학관'), ('신학관', '신학관'), ('아펜젤러관', '아펜젤러관'), ('알렌관', '알렌관'), ('언더우드관', '언더우드관'), ('연희관', '연희관'), ('외솔관', '외솔관'), ('우정원', '우정원'), ('운동선수기숙사', '운동선수기숙사'), ('위당관', '위당관'), ('음악관', '음악관'), ('중앙도서관', '중앙도서관'), ('청송대', '청송대'), ('체육관', '체육관'), ('학생회관', '학생회관'), ('학술정보원', '학술정보원'), ('한경관', '한경관'))

items = ( 
    ('필기류', '필기류'), ('지갑', '지갑'), ('전자기기', '전자기기'), ('의류', '의류'), ('신분증/카드', '신분증/카드'), ('기타', '기타') 
)

def no_future(value):
    today = date.today()
    if value > today:
        raise ValidationError('잘못된 날짜입니다.')

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="images/", blank=True)
    found_place = models.CharField(max_length=10, choices = places, default= '경영관')
    kept_place = models.CharField(max_length=10, choices = places, default= '경영관')
    item_type = models.CharField(max_length=10, choices = items, default='필기구')
    found_date = models.DateField(validators=[no_future])

    def __str__(self):
        return self.title

    def summary(self):
        return self.content[:100]

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.content
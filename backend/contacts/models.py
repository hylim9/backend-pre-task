from django.db import models
from django.conf import settings
from common.models import CommonModel


class Contact(CommonModel):
    """
    - 프로필 사진 : url 입력 방식
    - 이름
    - 이메일
    - 전화번호
    - 회사
    - 직책
    - 메모
    - 라벨
      - 사용자 정의 라벨
      - 연락처 1개에 라벨 다수 연결 가능
    - 기타 항목 추가
      - 주소
      - 생일
      - 웹사이트
    """

    profile_picture = models.URLField(
        blank=False,
        null=False,
        help_text="프로필사진",
    )
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        help_text="이름",
    )
    email = models.EmailField(
        blank=False,
        help_text="이메일주소",
    )
    phone_number = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        unique=True,
        help_text="전화번호",
    )
    company = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        help_text="회사",
    )
    job_title = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        help_text="직책",
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="메모",
    )
    label = models.ManyToManyField(
        "contacts.Label",
        related_name="contacts",
    )
    address = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        help_text="주소",
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
    )
    homepage_url = models.URLField(
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "contact"


class Label(CommonModel):
    """사용자 정의 라벨"""

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        help_text="라벨",
    )

    class Meta:
        db_table = "label"

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ListField, SerializerMethodField
from .models import (
    Contact,
    Label,
)

import re


class LabelSerializer(ModelSerializer):
    class Meta:
        model = Label
        fields = ("id", "name")


class ContactListSerializer(ModelSerializer):
    """
    - 프로필 사진
    - 이름
    - 이메일
    - 전화번호
    - 회사 (직책)
    - 라벨
    """

    label = LabelSerializer(
        many=True,
        read_only=True,
    )
    company_role = SerializerMethodField()

    class Meta:
        model = Contact
        fields = (
            "id",
            "profile_picture",
            "name",
            "email",
            "phone_number",
            "company_role",
            "label",
        )

    def get_company_role(self, contact):
        return f"{contact.company} ({contact.job_title})"


class ContactSerializer(ModelSerializer):
    # 연락처 생성 시 label ID 값 리스트로 생성
    label = ListField(child=serializers.IntegerField(required=False), required=False)

    def validate(self, data):
        website_pattern = r"(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)"
        email_pattern = r"[a-zA-Z0-9._+-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,4}"
        phone_num_pattern = r"\d{3}-\d{4}-\d{4}"
        reg_website = re.compile(website_pattern)
        reg_email = re.compile(email_pattern)
        reg_phone = re.compile(phone_num_pattern)

        # 전화번호 validation
        if reg_phone.search(data["phone_number"]) == None:
            raise serializers.ValidationError("전화번호 형식에 맞게 입력해주세요.")
        # 이메일 validation
        if reg_email.search(data["email"]) == None:
            raise serializers.ValidationError("이메일 형식에 맞게 입력해주세요.")
        # URL validation
        if reg_website.search(data["profile_picture"]) == None:
            raise serializers.ValidationError(
                "URL 형식에 맞게 프로필 사진을 입력해주세요."
            )

        # 전화번호 중복 체크
        if Contact.objects.filter(
            phone_number=data["phone_number"],
        ).exists():
            raise serializers.ValidationError("이미 등록 된 전화번호 입니다.")

        return data

    class Meta:
        model = Contact
        exclude = ("created_at", "updated_at")


class ContactDetailSerializer(ModelSerializer):
    label = LabelSerializer(
        many=True,
        read_only=True,
    )

    def validate(self, data):
        website_pattern = r"(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)"
        email_pattern = r"[a-zA-Z0-9._+-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,4}"
        phone_num_pattern = r"\d{3}-\d{4}-\d{4}"
        reg_website = re.compile(website_pattern)
        reg_email = re.compile(email_pattern)
        reg_phone = re.compile(phone_num_pattern)

        if "phone_number" in data:
            # 전화번호 validation
            if reg_phone.search(data["phone_number"]) == None:
                raise serializers.ValidationError("전화번호 형식에 맞게 입력해주세요.")

        if "email" in data:
            # 이메일 validation
            if reg_email.search(data["email"]) == None:
                raise serializers.ValidationError("이메일 형식에 맞게 입력해주세요.")

        if "profile_picture" in data:
            # URL validation
            if reg_website.search(data["profile_picture"]) == None:
                raise serializers.ValidationError(
                    "URL 형식에 맞게 프로필 사진을 입력해주세요."
                )

        return data

    class Meta:
        model = Contact
        fields = "__all__"

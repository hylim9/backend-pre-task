from django.shortcuts import render
from django.db import transaction
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    ContactSerializer,
    LabelSerializer,
    ContactListSerializer,
    ContactDetailSerializer,
)
from .models import Contact, Label


class Contacts(APIView):
    order_type = openapi.Parameter(
        "order_type",
        openapi.IN_QUERY,
        description="정렬 방식 (asc 또는 desc 입력)",
        required=False,
        type=openapi.TYPE_STRING,
    )
    order_item = openapi.Parameter(
        "order_item",
        openapi.IN_QUERY,
        description="정렬 기준 (name, email, phone_number 중 입력)",
        required=False,
        type=openapi.TYPE_STRING,
    )
    page = openapi.Parameter(
        "page",
        openapi.IN_QUERY,
        description="페이지 넘버",
        required=False,
        type=openapi.TYPE_INTEGER,
    )

    @swagger_auto_schema(
        tags=["전체 연락처 리스트 가져오기"],
        operation_description="GET /contacts",
        manual_parameters=[order_type, order_item, page],
        responses={
            status.HTTP_200_OK: ContactListSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_404_NOT_FOUND: "Not Found",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def get(self, request):
        """
        기본 출력은 등록 순서대로 정렬합니다.
            - 이름, 이메일, 전화번호 중 하나
            - 정렬은 오름차순/내림차순/해제 순
        - 페이징
            - 스크롤 이벤트지만 다음 페이지 호출 시 화면에서 page=1, page=2 로 넘겨준다고 가정
        """
        order_type = request.query_params.get("order_type")  # asc/ desc / none
        order_item = request.query_params.get("order_item")  # name, email, phone_number
        if order_type in ["asc", "desc"]:
            if order_item:
                if order_type == "asc":
                    contact = (
                        Contact.objects.prefetch_related("label")
                        .all()
                        .order_by(f"{order_item}")
                    )
                else:
                    contact = (
                        Contact.objects.prefetch_related("label")
                        .all()
                        .order_by(f"-{order_item}")
                    )
        else:
            contact = Contact.objects.prefetch_related("label").all().order_by("id")

        # pagination
        paginator = Paginator(contact, 3)
        page = request.query_params.get("page", 1)
        contact_list = paginator.get_page(page)

        serializer = ContactListSerializer(
            contact_list,
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["연락처 생성"],
        operation_description="POST /contacts",
        request_body=ContactSerializer,
        responses={
            status.HTTP_201_CREATED: ContactListSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def post(self, request):
        serializer = ContactSerializer(
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    contact = serializer.save()
                    labels = request.data.get("label")
                    # 라벨 등록
                    if labels:
                        for label_pk in labels:
                            label = Label.objects.get(pk=label_pk)
                            contact.label.add(label)

                    serializer = ContactListSerializer(
                        contact,
                    )
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise ParseError("연락처 저장 실패")

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactsDetail(APIView):
    def get_object(self, pk):
        try:
            return Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        tags=["연락처 가져오기"],
        operation_description="GET /contacts/<int:pk>",
        responses={
            status.HTTP_200_OK: ContactDetailSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_404_NOT_FOUND: "Not Found",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def get(self, request, pk):
        contact = self.get_object(pk)

        serializer = ContactDetailSerializer(
            contact,
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["연락처 수정"],
        operation_description="""
            PUT /contacts/<int:pk>

            partial=True
            수정하는 데이터만 전달하여도 수정 가능합니다.
        """,
        request_body=ContactSerializer,
        responses={
            status.HTTP_200_OK: ContactDetailSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def put(self, request, pk):
        contact = self.get_object(pk)
        serializer = ContactDetailSerializer(
            contact,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    contact = serializer.save()
                    labels = request.data.get("label")
                    if labels:
                        for label_pk in labels:
                            label = Label.objects.get(pk=label_pk)
                            contact.label.add(label)

                    serializer = ContactDetailSerializer(
                        contact,
                    )
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                raise ParseError(f"연락처 수정 실패: {e}")

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Labels(APIView):
    """라벨"""

    @swagger_auto_schema(
        tags=["전체 라벨 리스트 가져오기"],
        operation_description="GET /labels",
        responses={
            status.HTTP_200_OK: LabelSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_404_NOT_FOUND: "Not Found",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def get(self, request):
        try:
            label = Label.objects.all()
        except Label.DoesNotExist:
            raise NotFound

        serializer = LabelSerializer(
            label,
            many=True,
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["라벨 추가하기"],
        operation_description="POST /labels",
        request_body=LabelSerializer,
        responses={
            status.HTTP_201_CREATED: LabelSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_404_NOT_FOUND: "Not Found",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def post(self, request):
        serializer = LabelSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            label = serializer.save()
            serializer = LabelSerializer(label)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactLabels(APIView):
    @swagger_auto_schema(
        tags=["연락처 라벨 리스트 가져오기"],
        operation_description="GET /contacts/<int:pk>/labels",
        responses={
            status.HTTP_200_OK: LabelSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_404_NOT_FOUND: "Not Found",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def get(self, request, pk):
        try:
            label = Label.objects.filter(contacts__id=pk)
        except Label.DoesNotExist:
            raise NotFound

        serializer = LabelSerializer(
            label,
            many=True,
        )
        return Response(serializer.data)


# Template 테스트 용 화면
class Main(APIView):
    def get(self, request):
        contact_list = Contact.objects.all().order_by("id")
        paginator = Paginator(contact_list, 6)
        page = request.query_params.get("page", 1)
        contact_p = paginator.get_page(page)
        serializers = ContactListSerializer(
            contact_p,
            many=True,
        )

        return render(
            request,
            "contacts/main.html",
            context=dict(contacts=serializers.data, page_obj=contact_p),
        )


class ContactsTemplate(APIView):
    def post(self, request):
        serializer = ContactSerializer(
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    contact = serializer.save()
                    labels = request.data.getlist("label")
                    # 라벨 등록
                    if labels:
                        for label_pk in labels:
                            label = Label.objects.get(pk=label_pk)
                            contact.label.add(label)

                    serializer = ContactListSerializer(
                        contact,
                    )
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise ParseError("연락처 저장 실패")

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactsDetailTemplate(APIView):
    def get_object(self, pk):
        try:
            return Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        contact = self.get_object(pk)
        serializer = ContactDetailSerializer(
            contact,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    contact = serializer.save()
                    labels = request.data.getlist("label")
                    if labels:
                        for label_pk in labels:
                            label = Label.objects.get(pk=label_pk)
                            contact.label.add(label)

                    serializer = ContactDetailSerializer(
                        contact,
                    )
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                raise ParseError(f"연락처 수정 실패: {e}")

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import pytest


@pytest.fixture(autouse=True)
def create_contact(db):
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO contact (
            profile_picture,
            name,
            email,
            phone_number,
            company,
            job_title,
            description,
            address,
            birth_date,
            homepage_url,
            created_at,
            created_by,
            updated_at,
            updated_by
        )
        VALUES (
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnv42OT9xKWPPynLHlQPhYlIxWxxJNQBW7qbD-4AA5gQ&s',
            '테스트인물',
            'test@gmail.com',
            '010-1111-0000',
            '파이테스트',
            '사원',
            '테스트',
            null,
            null,
            null,
            datetime('now'),
            'pytest',
            datetime('now'),
            null
        );
        """
    )


@pytest.fixture(autouse=True)
def create_label():
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO label (
            name,
            created_at,
            created_by,
            updated_at,
            updated_by
        )
        VALUES (
            '기타',
            datetime('now'),
            'pytest',
            datetime('now'),
            null
        );
        """
    )

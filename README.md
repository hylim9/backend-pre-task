# Django + template 프로젝트

- 환경
- python : 3.9.4
- django : 3.2.20
- django-rest-framework : 3.14.0
- SQLite

---

### 프로젝트

1. 패키지 설치.
   `pip install -r requirements.txt`
2. DB migrate 부탁드립니다.
   `python backend/manage.py migrate `
3. 기본 데이터 INSERT 시 db/data.sql 참고하여 데이터 추가해주세요.
4. runserver
   `python backend/manage.py runserver`
5. swagger 로 API 문서 확인 가능합니다.
   ` 예시) http://127.0.0.1:8000/swagger/`
6. 간단한 테스트 pytest로 확인 해 주세요.
   ```
   cd backend
   pytest
   ```
7. 입력과 확인의 편의를 위해 화면 template을 만들었습니다. /main 에서 확인해주세요. 오직 입력과 확인의 편의를 위함이니 참고 부탁드립니다.
   `http://127.0.0.1:8000/main/`

---

### API 리스트

구현 된 API 리스트 입니다

```text
- GET /api/v1/contacts (전체 연락처 리스트)
- POST /api/v1/contacts (연락처 등록)
- GET /api/v1/contacts/<int:contact_id> (연락처 세부 정보)
- PUT /api/v1/contacts/<int:contact_id> (연락처 수정)
- GET /api/v1/contacts/labels (전체 라벨 리스트)
- POST /api/v1/contacts/labels (라벨 등록)
- GET /api/v1/contacts/<int:contac_id>/labels (연락처 내 라벨)
```

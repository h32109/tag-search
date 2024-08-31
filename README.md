
# Tag_search

## 목차
1. [프로젝트 실행 방법](#프로젝트-실행-방법)
2. [API 문서](#API-문서)


## 프로젝트 실행 방법
프로그램을 실행하기 위해선 다음과 같은 절차를 따릅니다.

### 로컬 실행 방법

#### 프로젝트 클론:
```bash
# 해당 프로젝트를 클론합니다.
git clone https://github.com/h32109/tag_search.git
```
#### 필요 라이브러리 설치:
```bash
# 필요한 라이브러리를 설치합니다.
pip install -r requirements.txt
```
#### 환경 변수 설정:
```bash
# DB 환경변수 설정
tag_search/searcher/config/prod.env
...
SQL_URL="mysql+asyncmy://user:password@host:port"
SQL_DATABASE="your_database_name"
...
```
#### 애플리케이션 실행:
```bash
# 애플리케이션을 시작합니다.
export PROFILE=prod && uvicorn main:app --lifespan=on
```

## API 문서
이 프로젝트의 API 문서는 다음과 같습니다.

### Search company
- **경로**: `/search`
- **메소드**: `get`
- **설명**: 회사 이름을 검색합니다. 이름의 일부만 검색해도 동작합니다. header의 x-wanted-language에 따라 해당 언어로 반환합니다.
- - #### 요청 본문
| 필드명                 | 위치           | 타입  | 설명                     | 필수 여부 |
|---------------------|--------------|-----|------------------------|-------|
| `query`             | query string | str | 검색할 쿼리                 | Y     |
| `x-wanted-language` | header       | str | 응답 데이터의 언어 (예: en, ko) | Y     |      
- **요청 예**:
  ```
  curl -H "x-wanted-language: ko" http://localhost:8000/search?query=링크
  ```
- **응답 예**:
  ```json
  [
      {
          "company_name": "주식회사 링크드코리아"
      },
      {
          "company_name": "스피링크"
      }
  ]
  ```

### Get company by name
- **경로**: `/companies/{company_name}`
- **메소드**: `get`
- **설명**: 회사 이름으로 회사를 검색합니다. header의 x-wanted-language에 따라 해당 언어로 응답 데이터를 반환합니다.
- #### 요청 본문
| 필드명            | 위치             | 타입  | 설명                     | 필수 여부 |
|----------------|----------------|-----|------------------------|-------|
| `company_name` | path parameter | str | 검색할 회사명                | Y     |
| `x-wanted-language` | header         | str | 응답 데이터의 언어 (예: en, ko) | Y     |                           | Y     |
- **요청 본문 예**:
  ```
  curl -H "x-wanted-language: ko" http://localhost:8000/companies/쿼드자산운용
  ```
- **응답 예**:
  ```json
  {
      "company_name": "쿼드자산운용",
      "tags": [
          "태그_24",
          "태그_23",
          "태그_29",
          "태그_26"
      ]
  }
  ```
  
- **오류 요청 본문 예**:
  ```
  curl -H "x-wanted-language: ko" http://localhost:8000/companies/없는회사이름
  ```
  
- **응답 예**:
  ```json
  404 Not Found
  {
      "detail": "Company not found"
  }
  ```
  
### Get companies by tag
- **경로**: `/tags`
- **메소드**: `get`
- **설명**: 태그로 회사를 검색합니다. header의 x-wanted-language에 따라 해당 언어로 반환합니다.
- - #### 요청 본문
| 필드명                 | 위치           | 타입  | 설명                     | 필수 여부 |
|---------------------|--------------|-----|------------------------|-------|
| `query`             | query string | str | 검색할 태그명                | Y     |
| `x-wanted-language` | header       | str | 응답 데이터의 언어 (예: en, ko) | Y     |      
- **요청 예**:
  ```
  curl -H "x-wanted-language: ko" http://localhost:8000/tags?query=タグ_22
- **응답 예**:
  ```json
  [
      {
          "company_name": "딤딤섬 대구점"
      },
      {
          "company_name": "마이셀럽스"
      },
      {
          "company_name": "Rejoice Pregnancy"
      },
      {
          "company_name": "삼일제약"
      },
      {
          "company_name": "투게더앱스"
      }
  ]
  ```

### Create company
- **경로**: `/companies`
- **메소드**: `post`
- **설명**: 새로운 회사를 추가합니다. 저장 완료후 header의 x-wanted-language에 따라 해당 언어로 응답 데이터를 반환합니다.
- #### 요청 본문
| 필드명            | 위치   | 타입   | 설명                                       | 필수 여부 |
|----------------|------|------|------------------------------------------|-------|
| `company_name` | body | json | 생성할 회사 {"language": "company_name", ...} | Y     |
| `tags`         | body | list | 생성할 태그목록                                 | Y     |
| `tag_name` | tags | json | 생성할 태그 {"language": "tag_name", ...}     | Y     |
| `x-wanted-language` | header | str  | 응답 데이터의 언어 (예: en, ko)                              | Y     |
- **요청 본문 예**:
  ```json
  header: {"x-wanted-language": "tw"}
  {
      "company_name": {
          "ko": "라인 프레쉬",
          "tw": "LINE FRESH",
          "en": "LINE FRESH"
      },
      "tags": [
          {
              "tag_name": {
                  "ko": "태그_1",
                  "tw": "tag_1",
                  "en": "tag_1"
              }
          },
          {
              "tag_name": {
                  "ko": "태그_8",
                  "tw": "tag_8",
                  "en": "tag_8"
              }
          },
          {
              "tag_name": {
                  "ko": "태그_15",
                  "tw": "tag_15",
                  "en": "tag_15"
              }
          }
      ]
  }
  ```
- **응답 예**:
  ```json
  {
      "company_name": "LINE FRESH",
      "tags": [
          "tag_1",
          "tag_8",
          "tag_15"
      ]
  }
  ```

### Update company tag
- **경로**: `/companies/{company_name}/tags`
- **메소드**: `put`
- **설명**: 회사 태그 정보를 추가합니다. 저장 완료후 header의 x-wanted-language에 따라 해당 언어로 응답 데이터를 반환합니다.
- #### 요청 본문
| 필드명            | 위치             | 타입   | 설명                                   | 필수 여부 |
|----------------|----------------|------|--------------------------------------|-------|
| `company_name` | path parameter | str  | 수정할 회사 이름                            | Y     |
| `tag_name` | body(list)     | json | 추가할 태그 {"language": "tag_name", ...} | Y     |
| `x-wanted-language` | header         | str  | 응답 데이터의 언어 (예: en, ko)               | Y     |
- **요청 본문 예**:
  ```json
  header: {"x-wanted-language": "tw"}
  [
      {
          "tag_name": {
              "ko": "태그_50",
              "jp": "タグ_50",
              "en": "tag_50"
          }
      },
      {
          "tag_name": {
              "ko": "태그_4",
              "tw": "tag_4",
              "en": "tag_4"
          }
      }
  ]
  ```
- **응답 예**:
  ```json
  {
      "company_name": "Persona Media",
      "tags": [
          "tag_4"
      ]
  }
  ```

### Delete company tag
- **경로**: `/companies/{company_name}/tags/{tag_name}`
- **메소드**: `delete`
- **설명**: 회사 태그 정보를 삭제합니다. 저장 완료후 header의 x-wanted-language에 따라 해당 언어로 응답 데이터를 반환합니다.
- #### 요청 본문
| 필드명            | 위치             | 타입  | 설명                     | 필수 여부 |
|----------------|----------------|-----|------------------------|-------|
| `company_name` | path parameter | str | 태그를 삭제할 회사 이름          | Y     |
| `tag_name` | path parameter           | str | 삭제할 태그 이름              | Y     |
| `x-wanted-language` | header         | str | 응답 데이터의 언어 (예: en, ko) | Y     |
- **요청 본문 예**:
  ```json
  header: {"x-wanted-language": "en"}
  ```
- **응답 예**:
  ```json
  {
      "company_name": "Persona Media",
      "tags": [
          "tag_26"
      ]
  }
  ```

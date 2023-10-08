## 개요.
'채용 서비스' 를 ERD, RDBMS로 개발중인 간이 프로젝트 입니다.

본 서비스는 기업의 채용을 위한 웹 서비스 입니다.

회사는 채용공고를 생성하고, 이에 사용자는 지원합니다.

## 사용 기술.
Django, PostgreSQL, DRF, flake8, black formatter

## Limitation.
Docker 컨테이너화 대신, 파이썬 가상환경 적용.

토큰 설정 생략.

## Git Convention:
feat – a new feature is introduced with the changes

fix – a bug fix has occurred

chore – changes that do not relate to a fix or feature and don't modify src or test 

files (for example updating dependencies)

refactor – refactored code that neither fixes a bug nor adds a feature

docs – updates to documentation such as a the README or other markdown files

style – changes that do not affect the meaning of the code, likely related to code 
formatting such as white-space, missing semi-colons, and so on.

test – including new or correcting previous tests

perf – performance improvements

ci – continuous integration related

build – changes that affect the build system or external dependencies

revert – reverts a previous commit
<!-- https://www.freecodecamp.org/news/how-to-write-better-git-commit-messages/ -->



## Known issue:

### 1. 점검 중, CompanyApp 에서 포착한 __init__ 마이그레이션 적용 문제.
특히 해당 부분의 DB migration을 초기화 한 후 재차 migrate 을 시도했지만, 유독 이 CompanyApp 에서만 migrate 가 적용되지 않았음. 해결 방법은 직접 psql 의 현 DB에 진입 후, 다음과 같이 쿼리문을 보내서 해당 문제되는 CompanyApp 모든 행 부분을 삭제.
`dbwanted=# DELETE FROM django_migrations WHERE app = 'CompanyApp';`
이로서 다시 migrate 적용이 가능 해 졌음.
원인은 최초에 해당 앱의 모델 변경 후, DB 초기화를 위해 삭제 했지만 알수 없는 이유로 마이그레이션 파일이 DB 쪽에서 예상대로 작동하지 않음. 이에, 직접 조치.

### 2. serializer 구조 문제로 인한, 생성된 채용 공고 조회 불가 문제.
문제 원인:
Serializer 구조: JobPostingSerializer 내에서 other_job_postings 필드는 현재 채용공고와 동일한 회사의 다른 채용공고를 나타내는데, 채용공고 생성 시에도 이 필드가 작동하게 됩니다.
DB 저장 시점: 새로운 채용공고를 생성할 때, 해당 채용공고는 아직 데이터베이스에 저장되지 않았습니다. 따라서 get_other_job_postings 메서드에서 해당 채용공고를 제외하려고 할 때, 아직 DB에 저장되지 않은 채용공고의 id를 알 수 없기 때문에 제외하지 못하게 됩니다.
해결 방법:
to_representation 오버라이딩: Serializer의 to_representation 메서드를 오버라이드하여, 채용공고가 아직 DB에 저장되지 않았을 경우 other_job_postings 필드를 반환하지 않게 조절하였습니다. 이를 통해 새로운 채용공고 생성 시 해당 필드가 빈 배열로 반환되는 문제를 해결하였습니다.
필드 조건 변경: 채용공고 생성 요청에서는 other_job_postings 필드가 필요 없으므로, 이 필드를 생성 시점에서 제외하였습니다.
이렇게 변경을 통해 채용공고 생성 시 other_job_postings 필드가 적절하게 작동하도록 조정하였습니다.

### 3. DB 와 마이그레이션 - JobPosting 모델에 관련된 마이그레이션 이슈.
1. 이슈
- 데이터베이스(DB)의 `JobPosting` 모델에 관련된 마이그레이션 이슈 발생.
- `tech_stack` 필드 관련하여 DB와의 일관성 문제로 에러 발생.
- 특히 `JobPostingApp_techstack` 및 `JobPostingApp_jobposting_tech_stack` 테이블과 관련하여 문제 발생.
  
2. 원인
- 마이그레이션 파일과 실제 DB 상태 간의 불일치: 즉, 마이그레이션은 실행되었지만, 실제 DB에 반영되지 않았거나, 예상치 못한 방식으로 반영되어 에러가 발생.
- `tech_stack` 필드의 정의 및 처리 방식과 관련한 이슈: `JobPostingSerializer`에서 `tech_stack` 필드가 명시적으로 정의되지 않아서 생기는 문제. 

3. 해결방법
- **마이그레이션 및 DB 초기화**: 
  - `makemigrations` 및 `migrate` 명령어를 사용하여 마이그레이션을 다시 생성하고 적용.
  - 필요한 경우, DB를 초기화하고 마이그레이션을 다시 적용.
- **모델 및 시리얼라이저 수정**:
  - `JobPostingSerializer`에 `tech_stack` 필드를 명시적으로 추가.
  - `tech_stack` 필드에 대한 적절한 검증 및 저장 로직을 구현.
  - `to_representation` 메서드를 사용하여 응답 형식을 조정.
  
이러한 해결 방법을 통해, 입력된 `tech_stack` 데이터를 정상적으로 처리하고, 응답 데이터에도 원하는 형태로 `tech_stack`을 포함시킬 수 있었습니다.

### 4. Serializers.py in JobPostingApp - tech_stack 의 출력 이상.
1. 이슈
- `JobPosting`을 생성하거나 수정할 때, `tech_stack` 필드에 대한 데이터가 올바르게 처리되지 않음.
- API 응답에서 `tech_stack` 필드가 비어 있거나, 원하는 형태로 출력되지 않음.

2. 원인
- `JobPostingSerializer`에서 `tech_stack` 필드가 초기값(initialisation)을 갖지 않았음.
- 따라서, 입력 데이터를 올바르게 처리하고, 해당 필드를 DB에 저장하는 로직이 누락되었음.

3. 해결방법
- `JobPostingSerializer`에 `tech_stack` 필드를 명시적으로 정의.
- 해당 필드에 대한 검증 및 저장 로직(`validate_tech_stack` 및 `create` 메서드)을 추가.
- `to_representation` 메서드를 사용하여 응답 데이터의 형태를 조정하여, `tech_stack`을 원하는 형태로 출력하도록 수정.

이를 통해 `tech_stack` 데이터가 올바르게 처리되었으며, API 응답에서도 원하는 형태로 `tech_stack` 정보가 출력되게 되었습니다.
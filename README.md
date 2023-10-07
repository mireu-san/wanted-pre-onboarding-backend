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
- 점검 중, CompanyApp 에서 포착한 __init__ 마이그레이션 적용 문제.
특히 해당 부분의 DB migration을 초기화 한 후 재차 migrate 을 시도했지만, 유독 이 CompanyApp 에서만 migrate 가 적용되지 않았음. 해결 방법은 직접 psql 의 현 DB에 진입 후, 다음과 같이 쿼리문을 보내서 해당 문제되는 CompanyApp 모든 행 부분을 삭제.
`dbwanted=# DELETE FROM django_migrations WHERE app = 'CompanyApp';`
이로서 다시 migrate 적용이 가능 해 졌음.
원인은 최초에 해당 앱의 모델 변경 후, DB 초기화를 위해 삭제 했지만 알수 없는 이유로 마이그레이션 파일이 DB 쪽에서 예상대로 작동하지 않음. 이에, 직접 조치.
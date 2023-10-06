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
# 3기_도서관대출서비스_조병민

도서관대출서비스 프로젝트 템플릿입니다.

## :clipboard: 개발환경
* Visual Studio Code
* WorkBench
* GitLab

## :clipboard: 사용기술
* Flask
* SQLAlchemy 
* JQuery
* MySQL
* HTML + Flask Jinja2

## :clipboard: 개발일지
### 2021-11-16
1. DB Table 설계 ([ERD](https://www.erdcloud.com/d/vbmL8bvNSgHjruJW5))
2. 개발목록 정리
* 비고
    * DB 설계 번경 될 수 있음
---
### 2021-11-17
1. 회원가입, 로그인, 로그아웃 기능 구현
2. Jinja2 extends(base.html) 구현
* 비고
    * 내일 DB 설계 다시 해야 함

---
### 2021-11-18
1. 책 리스트, 책 상세화면 구현
2. 대여기능 구현
3. data import
4. DB 설계 변경 ([ERD](https://www.erdcloud.com/d/vbmL8bvNSgHjruJW5))
* 비고
    * 전체적인 UI 흐름이 매끄럽지 않음 

### 2021-11-19
1. 책 대여목록, 책 반납목록 화면 구현
2. 반납 기능 구현
3. 상당 base.html 변경
* 비고
 * SQLAlchemy subquery, join 활용 - 아직 ORM이 익숙하지 않아서 사용하기 힘들었음.

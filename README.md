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

## 개발내용

 [필수] **로그인**
- [x]  사용자로부터 아이디(이메일)와 비밀번호 정보를 입력받아 로그인 합니다.
- [x]  아이디와 비밀번호는 필수 입력 사항 입니다.
- [x]  로그인한 유저에 대해 session으로 관리해야 합니다.

[선택] *로그인*
- [x]  비밀번호는 최소 8자리 이상의 길이로 입력 받아야 합니다.
- [x]  아이디는 이메일 형식으로만 입력 받아야 합니다.

[필수] **회원가입**
- [x]  사용자로부터 아이디(이메일), 비밀번호, 이름 정보를 입력받아 회원가입합니다.
- [x]  비밀번호와 비밀번호 확인의 값이 일치해야 합니다.

[선택] *회원가입*
- [x]  아이디는 이메일 형식으로만 정보를 입력 받아야 합니다.
- [ ]  이름은 한글, 영문으로만 입력 받아야 합니다.
- [x]  비밀번호는 영문, 숫자, 특수문자 중 2종류 이상을 조합하여 최소 10자리 이상 또는 3종류 이상을 조합하여 최소 8자리 이상의 길이로 구성합니다.

[필수] **로그아웃**
- [x]  현재 로그인한 사용자에 대해 로그아웃 합니다.
- [x]  로그아웃한 유저를 현재 session에서 제거해야 합니다.

[필수] **메인**
- [x]  현재 DB 상에 존재하는 모든 책 정보를 가져옵니다.
- [x]  현재 DB 상에 존재하는 남은 책의 수를 표기합니다.
- [x]  책 이름을 클릭 시 책소개 페이지로 이동합니다.
- [x]  책의 평점은 현재 DB 상에 담겨있는 모든 평점의 평균입니다. 숫자 한자리수로 반올림하여 표기합니다.

[선택] *메인*
- [x]  페이지네이션 기능을 추가합니다. 한 페이지 당 8권의 책만을 표기합니다.

[필수] **대여하기**
- [x]  메인 페이지의 대여하기 버튼을 클릭하여 실행합니다.
- [x]  현재 DB 상에 책이 존재 하지 않는 경우, 대여되지 않습니다.
- [x]  현재 DB 상에 책에 존재하는 경우, 책을 대여하고 책의 권수를 -1 합니다.

[선택] *대여하기*
- [x]  현재 DB 상에 책이 존재하지 않는 경우, 사용자에게 대여가 불가능하다는 메세지를 반환합니다.
- [x]  유저가 이미 이 책을 대여했을 경우, 이에 대한 안내 메세지를 반환합니다.

[필수] **반납하기**
- [x]  로그인한 유저가 대여한 책을 모두 보여줍니다.
- [x]  반납하기 버튼을 통해 책을 반납합니다. 책을 반납한 후 DB 상에 책의 권수를 +1 합니다.

[필수] **책소개**
- [x]  메인 페이지의 책 이름을 클릭하여 접근합니다.
- [x]  책에 대한 소개를 출력합니다.

[선택] *책소개*
- [x]  가장 최신의 댓글이 보이도록 sorting하여 보여줍니다.
- [x]  댓글을 작성함으로써 책에 대한 평가 점수를 기입합니다.
- [x]  댓글 내용과 평가 점수는 모두 필수 입력 사항입니다.

[선택] *대여기록*
- [x]  로그인한 유저가 대여 후 반납했던 책에 대한 모든 사항을 출력합니다.

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

### 2021-11-20
1. 책 리스트, 책 상세화면, 대여기능 구현
2. 오타수정

### 2021-11-21
1. 반납기능구현, 대여목록, 반납하기 ui 구현
3. book_borrow, table return_due_date 컬럼 추가

### 2021-11-22
1. 로그인, 회원가입, bootstrap 적용

### 2021-11-23
1. 대여기록, 반납목록, 북리스트,상세페이지, 댓글 bootstrap 적용

### 2021-11-24
1. rating기능 select -> radio(별) 변경
2. book_comment, comment_date 컬럼 추가
2. 댓글 삭제 기능 추가
3. 책목록 pagenation 기능 추가

### 2021-11-25
1. .evn 파일추가
* 비고
 * 검색기능을 만들었었으나 ssr이기때문에 페이지 전체가 로딩이 되어 비효율적이고, 검색 키워드가 사라짐 -> 이번 프로젝트에서는 검색기능 제외


# [Assginment 1] 에이모

9조 이태성, 임유선
> 원티드 지원 과제에 게시판 카테고리, 댓글, 대댓글, 조회수 기능을 추가하였고 RESTful API로 설계되었습니다.


## Publish Link
https://documenter.getpostman.com/view/18176091/UVBzn9Wi


## Built with
* Python
* Django
* Pipenv
* MongoDB
* Djongo


## Members
본 프로젝트는 pair programming으로 진행되었습니다.
- __이태성__ - Navigator
  1. Unit Test 구현
  2. 서버 배포
  3. API 설계
 
- __임유선__ - Driver
  1. 게시글 읽힘 수
  2. 게시글 카테고리
  3. 대댓글 기능
  4. 게시글 검색
 
## Implementation List
- 회원가입
  - 입력된 정보의 고유성 검사 
  - 올바르게 입력 되었을시 데이터베이스에 정보 저장
- 로그인
  - 항목이 올바르게 입력되었는 지 확인
  - 로그인 시 해당 계정의 로그인 정보를 저장 
- 게시글
  - 로그인된 사용자만 POST 가능
  - 작성자만 PATCH, DELETE 가능
  - READ시 한 ID당 한 번만 조회수 증가  
- 댓글
  - 작성자만 PATCH, DELETE 가능
  - 대댓글 작성 및 PATCH, DELETE 가능
  - 대댓글 Pagination (1 depth)
 
 
 
## TIL
* 이태성: 
* 임유선: https://yusunlim.wordpress.com/2021/11/03/21-11-03-today-i-learned/

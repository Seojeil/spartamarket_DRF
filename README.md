# Spartamarket_DRF

## Document
- Wireframe
- ERD
- API specification
## Apps
### accounts
- 회원가입
    - 새로운 유저의 정보를 등록합니다. username, password, first_name, last_name, nickname, email, birth_day, gender, introduce를 입력받을 수 있으며 gender는 비공개가 가능하고 introduce는 생략가능합니다.
    - ![회원가입](postman/signup.JPG)
- 로그인
    - DB에 등록된 회원일 경우 토큰을 발행합니다. 등록되지 않을 회원이거나 비밀번호를 잘못 입력한 경우 지정한 메시지를 출력합니다.
    - ![로그인 성공](postman/login_success.JPG)
    - ![로그인 실패](postman/login_failure.JPG)
- 프로필 조회
    - 현재 로그인한 유저의 정보를 조회할 수 있습니다. 로그인한 경우에만 사용할 수 있습니다.
    - ![프로필](postman/profile.JPG)
- 로그아웃
    - 현재 로그인한 유저의 refresh token 을 blacklist에 추가하여 작동하지 않도록 합니다.
    - ![로그아웃](postman/logout.JPG)
- 회원탈퇴
    - 현재 로그인중인 유저의 정보를 DB에서 삭제합니다.
    - ![회원탈퇴](postman/account_delete.JPG)
### products
- 상품등록
    - 로그인한 사용자는 게시글을 작성할 수 있습니다.
    - ![글작성](postman/create.JPG)
- 상품목록 조회
    - 작성글 목록을 조회할 수 있습니다.
    - ![글목록](postman/index.JPG)
- 상품수정
    - 작성자는 자신이 작성한 작성한 게시물을 수정할 수 있습니다.
    - ![글목록](postman/update.JPG)
- 상품 삭제
    - 작성자는 자신이 작성한 작성한 게시물을 삭제할 수 있습니다.
    - ![글목록](postman/delete.JPG)
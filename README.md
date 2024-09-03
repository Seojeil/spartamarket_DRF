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
### products
- 상품등록
    - 기능설명
- 상품목록 조회
    - 기능설명
- 상품수정
    - 기능설명
- 상품 삭제
    - 기능설명
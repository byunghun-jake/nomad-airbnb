# Nomad coder - Airbnb Clone



#### 시작:

210321(일) in cafe DAMDA



#### 진행 상황

- [ ] User App
- [ ] Room App
- [ ] etc...



## 환경 설정



### 0) 원격 레포지토리 설정

github에서 원격 레포지토리 생성 후

```bash
$ git init
# README.md가 추가된 상태
$ git add .
$ git commit -m "init"
# 원격 레포지토리 연결
$ git remote add origin "https://github.com/byunghun-jake/nomad-airbnb.git"

# 원격 레포 연결 확인
$ git remote
origin

# push
$ git push -u origin
```

> push 시 -u 키워드의 의미: 기본 원격 레포지토리를 origin이라는 이름의 레포지토리로 설정한다는 뜻



### 1) 가상 환경 설정

```bash
# 가상 환경 설정하기
$ python -m venv venv

# 가상 환경 활성화
$ source venv/Scripts/activate
```

- 가상 환경 설정 시, `-m`을 쓰는 이유는 뭘까? [공식 문서](https://docs.python.org/ko/3/using/cmdline.html#cmdoption-m)

  > 제공한 모듈 이름을 sys.path에서 검색하고, 그 내용을 \__main__모듈로써 실행합니다.
  >
  > `python -m module-name`
  >
  > 즉, 파이썬 모듈을 실행하기 위해 입력하는 것!

- 노마드 코더는 pipenv라는 별도의 패키지를 사용하는데, venv를 쓰는 이유는?
  - [pipenv를 추천하지 않는 이유](https://velog.io/@doondoony/pipenv-101)
  - ssafy에서 배운 내용을 그대로 활용하고 싶어서
  - 파이썬을 맞춰서 새로 설치할 필요는 없을 것 같고, 컴퓨터에 설치된 파이썬을 그대로 사용하며 패키지만 관리해주려고



- 가상환경 설정 후 .gitignore 필요

  ![image-20210321163135814](README.assets/image-20210321163135814.png)

  > 장고 패키지까지만 설치하였는데, 수많은 파일이 생성되어 있음

  ![image-20210321163223762](README.assets/image-20210321163223762.png)

  > gitignore로 정리 완료 후
  >
  > 참고 사이트는 항상 애용하는 [gitignore](https://www.toptal.com/developers/gitignore)

  

### 2) django 패키지 설치

```bash
$ pip install django

# 패키지 설치 목록 저장
$ pip freeze > requirements.txt
```

> 패키지 목록을 따로 만드는 이유
>
> 우리는 venv를 원격 레포지토리에 올리지 않기 때문에, 어떤 패키지들이 이 프로젝트를 위해 설치되어 있는지 확인하기가 힘들다.
> pip freeze 명령어를 통해 특정한 파일에 지금까지 설치된 패키지를 저장함으로써 이 프로젝트를 보는 다른 사람들에게 패키지 정보를 전달할 수 있는 것이다.

![image-20210321170106499](README.assets/image-20210321170106499.png)

> requirements.txt 예시



---



## 프로젝트 시작



### 1) 장고 프로젝트 생성하기

#### 프로젝트 생성

```bash
$ django-admin startproject config .
```

```
- config
- manage.py
- README.md
```

> config 폴더와 manage.py 파일이 생성됩니다.

> 명령어에서 마지막에 `.`을 붙인 이유: 현재 폴더에 config라는 이름의 장고 프로젝트를 생성하고 싶기 때문
>
> `.`을 붙이지 않는다면, 다음과 같은 폴더 구조가 생성됩니다.
>
> ```
> - config
> 	- config
> 	- manage.py
> - README.md
> ```



- Linter & Formatter

  - Linter는 실시간 **문법 검사기**라고 생각하면 될 것 같다.

    이 프로젝트에서는 `flake8`을 사용한다.

    설정 방법은 `ctrl + shift + p`를 눌러 vs 콘솔창을 켠 후, select linter를 선택하여 flake8을 선택하면 된다.

    그러고나면, flake8이 설치되어있지 않았다라는 메세지가 뜰 텐데 flake8 패키지를 설치해주면 된다.

    `$ pip install flake8` 

    한가지 추가로 설정해 줄 것이 있는데, E501 규칙에 대한 내용이다. (라인 당 글자 길이 제한)

    ```json
    // .vscode/settings.json
    
    {
        // ...
        "python.linting.flake8Args": ["--max-line-length=100"]
    }
    ```

    

  - Formatter는 **문법 교정기**라고 생각하면 될 것 같다.

    이 프로젝트에서는 `black`을 사용한다.

    vscode의 Format On Save 옵션을 활성화해주면, 파이썬 파일을 변경하고 저장할 때 마다 `black`이 확인하고 `formatting`을 수행한다.

  

  - config 폴더에 있는 `__init__.py`의 의미

    파이썬 파일이 담겨있는 하나의 폴더를 패키지처럼 (import 할 수 있는) 사용하기 위한 일종의 표시라고 생각하면 될 것 같다.

    "이 폴더는 패키지처럼 사용할꺼야"

  

#### 시간대, 언어 설정하기

```python
# settings.py

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"
```



#### 기본 세팅 migrate

```bash
$ python manage.py migrate
```

> 장고 프로젝트를 생성하면, 기본적으로 DB를 위한 마이그레이션 파일이 생성됩니다.
>
> 마이그레이션 파일을 가지고 DB에 적용하는 작업을 migrate라고 하며, 이를 위와 같은 명령어로 수행할 수 있습니다.



#### admin 페이지 탐색하기

1. 관리자 계정 생성

   admin 페이지에 로그인할 관리자 계정을 생성해야 합니다.

   ```bash
   $ python manage.py createsuperuser
   ```

2. 서버 실행 후 admin 페이지 주소를 통해 접근하기

   ```bash
   $ python manage.py runserver
   ```

   

### 2) 앱 생성하기

> 장고 프로젝트는 앱(함수)의 집합입니다.
>
> 여러 앱으로 구성될 수 있으며, 기능에 따라 하나가 될 수도 있고 수십개가 될 수도 있습니다.
>
> **프로젝트를 본격적으로 시작하기 전에 만들고자 하는 서비스를 분석하며, 어떤 앱이 설치되어야 하는가에 대해 생각해봅시다.**



#### 앱 구조를 짜보자

- Rooms (숙소)

  - 숙소 생성(C)
  - 숙소 확인(R)
  - 숙소 수정(U)
  - 숙소 삭제(D)

  > 어라? CRUD??

- Reservations (예약)
- User (이용자)
  - CRUD
  - 로그인, 로그아웃
- Messages (메세지)
- Lists (이용자가 저장한 숙소 목록)

- Review (리뷰)



#### 앱 생성하기

1. 앱 생성하기

   ```bash
   $ python manage.py startapp rooms
   $ python manage.py startapp users
   $ python manage.py startapp reviews
   $ python manage.py startapp conversations
   $ python manage.py startapp lists
   $ python manage.py startapp reservations
   ```

   > 생성하는 앱 이름은 복수형이어야 합니다. (국룰)

   

2. 앱 등록하기

   > 생성한 앱은 프로젝트에 "이런 앱을 생성했습니다"라고 알려주어야 합니다.






























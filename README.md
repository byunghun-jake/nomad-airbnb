# Nomad coder - Airbnb Clone



## 환경 설정



### 0) 원격 레포지토리 설정

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

  

### 2) django 패키지 설치

```bash
$ pip install django
```


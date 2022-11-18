---
layout: post
title:  "지킬 블로그 리셋하기"
date:   2022-11-06 21:52:20 +0900
categories: jekyll
cover: /assets/dinosaur.gif
---

> 블로그를 손에 놓은지 꽤 시간이 지나고 그 사이 블로그 작성에 사용하였던 노트북이나 컴퓨터가 바뀌었습니다. 그리고 다시 블로그를 시작하려고 하니 SEO에 검색이 안된다거나 페이지가 망가진채 작성이 안된다거나 이런 경우가 생기게 되어 결국 지킬 블로그 사용 방법이나 깃허브 사용법 등도 다시 익힐 겸 블로그 리셋을 결정하게 되었습니다.


# 0. 지킬 블로그 리셋을 어떻게?
일단 블로그 리셋은 다음과 같은 방향으로 이루어집니다. 먼저 새로운 블로그를 생성하고 기본적인 설정을 해줍니다. 그리고 이후에 기존 블로그에 이를 overwrite 합니다. 그리고 마지막으로 구글 관련된 설정을 할 예정입니다.

요목화하면 다음과 같습니다.

1. 새로운 지킬 블로그 생성
2. 테마 설정

# 1.  M1 맥에서 새로운 지킬 블로그(jekyll blog) 생성

M1 맥에서 jekyll 블로그의 생성은 다음과 같은 순서로 진행합니다.

1. 터미널 intel로 설정하기
2. Homebrew의 설치
3. 루비 설치
4. 지킬 블로그 설치 및 실행하기

## 0. 터미널(또는 i-term) intel로 설정하기
현재 M1 맥의 ventura OS에서 루비의 설치는 오류가 난다. 이는 M1에서의 호환성 문제로 보이며, 이는 터미널을 intel 모드로 실행함으로써 해결할 수 있습니다. 물론 완전한 해결 방법은 아닌 것으로 보이며, 구글 검색을 해보면 이와 관련된 많은 내용을 찾아볼 수 있습니다. 일단 터미널을 intel 모드로 실행하는 벙법은 다음과 같습니다.

(1) 로제타2 설치하기
```
softwareupdate --install-rosetta --agree-to-license
```

(2) 터미널 설정 변경하기(i-term도 동일)
- Finder - 응용프로그램 
- 터미널 앱을 우클릭한 후 `정보 가져오기`를 선택한다.
- `Rosetta를 사용하여 열기`를 체크한다.
- `활성 상태 보기`를 통해 intel로 터미널 앱을 사용하고 있는지 확인하기


## 1. Homebrew의 설치
먼저 터미널을 실행합니다. 그리고 다음 커맨드로 HomeBrew가 설치되어 있는지 확인합니다.

```
$ which brew  # Homebrew의 설치 위치 확인

$ brew --version # Homebrew의 버젼 확인
```
만약 Homebrew가 오래된 버젼이거나 설치가 되어 있는 경우 다음 커맨드를 입력하여 최신 버젼의 Homebrew를 설치합니다.
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
만약 원본을 확인하고 싶으면 [Homebrew의 홈페이지](https://brew.sh/)로 들어가 가장 상단에 있는 커맨드를 복사해 오면 됩니다.

## 2. asdf를 활용하여 루비 설치하기
루비의 설치 방법은 여러 방식이 있습니다. [루비 홈페이지](https://www.ruby-lang.org/ko/documentation/installation/#homebrew)를 참고하면 다양한 루비 설치 방법을 확인 할 수 있습니다. 이 중에서 관리자 항목의 `asdf-vm`를 활용할 것이다. asdf에 대해 홈페이지에서는 다음과 같이 설명하고 있다.

>asdf는 도구 버전 관리자입니다. 모든 도구 버전 정의는 프로젝트의 Git 리포지토리에 체크인하여 팀과 공유할 수 있는 하나의 파일(.tool-versions)에 포함되어 있어 모든 사람이 정확히 동일한 버전의 도구를 사용하고 있습니다.

**설치방법**

(1) asdf 설치하기 
```
brew install asdf
```

(2) ruby 플러그인 설치하기
```
brew install gpg gawk
```

(3)  최신 루비 설치하기
```
asdf install ruby latest
```

(4) 버젼 설정하기

```
$ asdf global ruby latest
$ asdf local ruby latest
```

(5) 버전 확인하기
```
asdf current
```

## 3. 지킬 설치하기
지킬을 설치하는 방법은 간단하다. 자세한 내용은 [지킬 홈페이지](https://jekyllrb.com/docs/step-by-step/01-setup/)를 참고하기 바랍니다.

(1) 지킬 설치하기
```
gem install jekyll bundler
```

(2) 지킬 블로그 생성하기
```
jekyll new 설치폴더이름
```

(3) 지킬 실행
```
$ cd 설치경로  # 설치 경로로 이동
$ bundle exec jekyll serve # 첫 실행
$ jekyll serve # 다음 실행시
```

**주의!**

만약 `bundler: failed to load command: jekyll`가 뜬다면
```
Bundle install --redownload
```
를 통해 다시 설치 해보세요.

(4) localhost 들어가 블로그 확인하기

http://localhost:4000 로 들어가면 새롭게 생성된 빈 블로그를 확인할 수 있습니다.


# 2. 테마 설정
다음으로 할일은 새로운 테마를 설정하는 일이었다. 기존의 minima 테마도 나쁘지 않았지만 이왕 새롭게 블로그를 개설하는 김에 새로운 테마로 바꾸기로 결정하였다. 그리고 눈에 띈 것이 jekyll-theme.org 첫 화면에 있던 `jekyll-Gitbook` 이었다. 깔끔하고 체계적인 UI를 보고 이를 선택하였다. 

홈페이지에서는 다음과 같이 Gitbook theme에 대해 설명하고 있다.

>GitBook은 웹에서 콘텐츠(예: 책 챕터 및 블로그)를 표시하고 구성하는 놀라운 프론트엔드 스타일입니다. Github Pages에서 GitBook을 배포하는 일반적인 방법은 로컬에서 HTML 파일을 빌드한 다음 Github 저장소(일반적으로 gh-pages 분기)로 푸시하는 것입니다. 이러한 작업을 반복하고 스테이징할 생성된 HTML 파일이 있을 때 git을 통해 버전 제어를 하기 어렵게 만드는 것은 상당히 성가신 일입니다.

이 테마는 생성된 GitBook 사이트에서 스타일 정의를 가져오고 마크다운 문서를 HTML로 렌더링하는 Jekyll용 템플릿을 제공하므로 원본 repo에 변경 사항이 있을 때마다 HTML 번들을 생성 및 업로드하지 않고도 전체 사이트를 Github 페이지에 배포할 수 있습니다.

## 2-1. 테마의 설치
`jekyll-Gitbook` 테마의 설치는 간단하다. 
  1. 블로그 설치 폴더에서 `config.yml` 파일을 연다.
  2. `theme: jekyll-theme-minimal`를 `remote_theme: sighingnow/jekyll-gitbook`로 수정한다.




---
layout: post
title:  "jekyll을 이용하여 블로그 만들기(7): GitHub 연동하기"
date:   2019-04-07 12:08:12 +0900
categories: IT
comments: true
---

> 지금까지 jekyll을 이용하여 블로그를 만드는 방법에 대해서 알아보았다면 이제는 실제로 블로그를 GitHub에 연동하여 누구나 웹을 통해 접속이 가능하도록 하는 방법에 대해서 알아보고자 한다.


## GitHub repository 만들기

우선적으로 GitHub를 가입하여야 한다. [GitHub 홈페이지](https://github.com/)에 들어가 가입을 하고 로그인을 하면 좌측상단에 이런 화면을 확인할 수가 있을 것이다.
![Repository 만들기1](https://github.com/newjin87/storage/blob/master/_img/jekyll/github.png?raw=true)

여기에서 `NEW` 아이콘을 선택하게 되면 우리는 우리만의 새로운 Repository를 만들 수가 있게 된다. 누르면 다음과 같은 화면을 확인할 수가 있을 것이다.
![Repository 만들기2](https://github.com/newjin87/storage/blob/master/_img/jekyll/github1.png?raw=true)

먼저 Repository 이름을 정해야 하는데, 이 이름이 도메인 주소  `http://github.com/레포지토리이름`과 같이 결정되므로 주의해서 지어야 한다. 일반적인 경우에는 다음과 같이 원하는 이름을 정하면 된다.
![Repository 이름정하기](https://github.com/newjin87/storage/blob/master/_img/jekyll/github2.png?raw=true)

다만 만약 도메인 주소를 `https://아이디.github.io`의 형태로 하기를 원한다면 다음과 같이 Repository의 이름을 `아이디.github.io`로 정하면 된다.
![Repository 이름정하기](https://github.com/newjin87/storage/blob/master/_img/jekyll/github3.png?raw=true)

Repository를 만들기 전에 마지막으로 주의할 점은 `Initialize this repository with a README`를 체크를 하지 말아야 한다는 점이다. 이 부분만 주의해서 만든다면 손쉽게 Repository를 생성할 수가 있다.
![주의사항](https://github.com/newjin87/storage/blob/master/_img/jekyll/github4.png?raw=true)


## GitHub에 블로그 연동하기

![완성된 Repository](https://github.com/newjin87/storage/blob/master/_img/jekyll/github5.png?raw=true)
Repository를 만들고 나면 다음과 같은 창을 확인할 수가 있다. 그리고 가운데 있는 화면이 사용자의 블로그 도메인이 되므로 옆에 아이콘을 눌러 복사를 해놓도록 하자. 그 다음으로 할 일은 `_config.yml` 파일을 수정하는 일이다.
두 가지 경우가 있는데, 만약 도메인 주소가 `http://github.com/레포지토리이름` 형태라면 `baseurl`에 다음과 같이 `"/레포지토리이름"`을 입력하면 된다.
![config수정](https://github.com/newjin87/storage/blob/master/_img/jekyll/github6.png?raw=true)

하지만 만약 `https://아이디.github.io`의 형태로 도메인을 설정했다면 baseurl은 빈칸으로 두고, 다음과 같이 `url`에 `"`https://아이디.github.io`"`를 입력하면 된다.
![config수정1](https://github.com/newjin87/storage/blob/master/_img/jekyll/github7.png?raw=true)

다음으로 할 일은 사용자의 사이트 폴더에 GIT을 설치하고 이를 연동시키는 일이다. 하지만 이 내용은 조금 복잡하기 떄문에 다음 포스팅을 통해서 글을 쓰도록 하겠다.

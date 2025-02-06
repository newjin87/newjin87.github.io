---
layout: post
title: 
date: 2025-02-07
Categories:
comments: true
---
Homebrew를 설치했지만 `brew` 명령어를 찾을 수 없다는 오류(`zsh: command not found: brew`)가 발생한 경우 해결방법은 다음과 같습니다.

### 해결 방법 
1. **설치 경로 확인** 
Homebrew가 정상적으로 설치되었는지 확인하려면 다음 명령어를 실행하세요.


```bash
ls /opt/homebrew/bin/brew
```

또는


```bash
ls /usr/local/bin/brew
```
출력이 없다면 Homebrew가 제대로 설치되지 않은 것일 수 있습니다.
설치가 되어 있다면, 다음 단계를 진행하세요.2. **환경 변수 설정** Homebrew가 설치된 경로를 `PATH` 환경 변수에 추가해야 합니다.
M1/M2/M3/M4 맥북의 경우:

```bash
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
```

인텔 맥의 경우:


```bash
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
```
3. **환경 변수 적용** 
위의 설정을 적용하려면 다음 명령어를 실행하세요.


```bash
source ~/.zshrc
```
4. **Brew 동작 확인** 
Homebrew가 정상적으로 동작하는지 확인하려면 다음을 실행하세요.


```bash
brew --version
```

버전 정보가 출력되면 정상적으로 설정된 것입니다.
5. **터미널 재시작** 위 설정을 적용한 후에도 `brew`가 작동하지 않으면 터미널을 닫고 다시 실행해 보세요.
### 추가 해결 방법 

설치 경로를 확인하는 명령어:


```bash
which brew
```

만약 아무것도 출력되지 않는다면, 설치가 제대로 되지 않은 것일 수 있으므로 다시 설치하는 것이 좋습니다.


```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

위 단계를 차례로 따라 하면 Homebrew가 정상적으로 실행될 것입니다. 😊

You: 

여전히 계속

ChatGPT: 

여전히 `brew`를 찾을 수 없다면, 아래 추가 방법을 하나씩 시도해보세요.

---


## 🔍 1. Homebrew가 어디에 설치되었는지 확인 

아래 명령어를 실행하여 Homebrew가 설치된 경로를 찾으세요.


```bash
find /opt/homebrew -name brew 2>/dev/null
find /usr/local -name brew 2>/dev/null
```

- 만약 출력 결과가 없다면, Homebrew가 정상적으로 설치되지 않은 것입니다. 다시 설치해 보세요.
 
- 출력 결과가 `/opt/homebrew/bin/brew` 또는 `/usr/local/bin/brew`와 같이 나온다면 다음 단계로 진행합니다.


---


## 🛠 2. 환경 변수에 경로 추가 

### ✅ M1/M2/M3/M4 맥북 (Apple Silicon) 


```bash
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
```

### ✅ 인텔 맥 (Intel) 


```bash
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
```

환경 변수를 적용하려면:


```bash
source ~/.zshrc
```
그런 다음 다시 `brew --version`을 실행해 보세요.

---

🔄 3. `brew`를 수동으로 실행해 보기만약 `brew --version`이 여전히 안 된다면, `brew` 명령어가 어디 있는지 직접 실행해 보세요.

```bash
/opt/homebrew/bin/brew --version
/usr/local/bin/brew --version
```
 
- 위 명령어 중 하나가 정상적으로 실행된다면, `brew`가 존재하지만 `PATH` 설정이 적용되지 않은 것입니다.
 
- 위 명령어가 정상 작동하는 경우, `alias`로 간단히 설정할 수도 있습니다.


```bash
echo 'alias brew="/opt/homebrew/bin/brew"' >> ~/.zshrc
source ~/.zshrc
```

또는 인텔 맥의 경우:


```bash
echo 'alias brew="/usr/local/bin/brew"' >> ~/.zshrc
source ~/.zshrc
```


---


## 🔁 4. Homebrew를 완전히 삭제 후 재설치 

그래도 해결되지 않는다면 Homebrew를 완전히 삭제하고 다시 설치하세요.

### 🗑 Homebrew 삭제 (M1/M2/M3/M4 및 Intel 공통) 


```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"
```

### 🆕 Homebrew 재설치 


```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
설치 후 다시 `brew --version`을 실행해 보세요.

---


### 🚀 최종 확인 

설치가 완료되었으면 다음을 실행하여 정상 작동하는지 확인합니다.


```bash
brew doctor
brew update
brew --version
```

위 방법으로도 해결되지 않는다면, 오류 메시지를 알려주시면 추가 해결 방법을 찾아드릴게요! 😊

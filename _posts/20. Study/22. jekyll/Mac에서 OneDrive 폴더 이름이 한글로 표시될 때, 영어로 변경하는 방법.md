---
layout: post
title: 
date: 2025-02-07
Categories: onedrive
comments: true
---

Mac에서 OneDrive의 기본 폴더 경로는 macOS Monterey 이후부터  
📂 **`/Users/사용자이름/Library/CloudStorage/OneDrive-개인`**  
형식으로 저장됩니다.

하지만 **이 폴더 이름은 수동으로 변경할 수 없으며**, Microsoft에서 자동 생성하는 경로이므로 직접 변경하면 OneDrive 동기화 오류가 발생할 수 있습니다.
##  해결 방법: 대체 경로 만들기**

폴더 이름을 `OneDrive-personal`로 바꾸고 싶다면, **심볼릭 링크(Symbolic Link)**를 사용하여 해결할 수 있습니다.

### **심볼릭 링크 생성**

1. **터미널 실행 (`Command + Space` → "터미널" 입력 후 실행)**
2. 다음 명령어 입력:
    
    bash
    
    복사편집
    ```
    ln -s "/Users/sungjinyoo/Library/CloudStorage/OneDrive-개인" "/Users/sungjinyoo/OneDrive-personal"
    '''
3. Finder에서 `~/OneDrive-personal` 폴더를 확인하면 원래 OneDrive 폴더와 동일한 내용이 보입니다.

💡 **이 방식은 원본 폴더를 변경하지 않으면서, 원하는 이름으로 접근할 수 있게 해줍니다.**
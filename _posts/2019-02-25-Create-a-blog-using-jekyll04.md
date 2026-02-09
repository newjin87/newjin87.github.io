---
layout: post
title: 'Create a blog using jekyll (4): Setting up Front Matter'
date: 2019-02-26 16:20:00 +0900
comments: true
categories: [Dev-Log]
tags: [GitHub-Pages, Jekyll, Blog-Setup]
---
> While creating a blog with jekyll, the most important thing is the front matter rather than the content of the article. Users who are familiar with other blog sites such as Naver may find the jekyll system very difficult. However, if you get used to it, you will be able to use it more comfortably than any other site. And what influences it is "Front Matter".

## Let's add "title".

 As we saw in the previous article, if you do not add "title" to FrontMatter, jekyll automatically sets the title of the post to the title set in the file name (the part after the date). However, in this case, the file name is too complicated and long. To solve this shortcoming, you can add **"title"** as the title of the post you want in Front Matter as shown below.

<img src="https://github.com/newjin87/storage/blob/master/_img/jekyll/posting.png?raw=true">

 If you add the **"title"** item, you can see that the title of the main screen and the title of the post have changed as follows. However, even if the "title" is changed in FrontMatter, the address of the post does not change.

<img src="https://github.com/newjin87/storage/blob/master/_img/jekyll/title1.png?raw=true" width="50%"><img src="https://github .com/newjin87/storage/blob/master/_img/jekyll/title2.png?raw=true" width="50%">

## What about "date"? Issue time!

 In the example provided by jekyll, you can see that there is a "date" item in FrontMatter. As with "title" as before, if "date" is not set, post is automatically set to the date of the file name. However, in this case, there is a disadvantage that the date does not change as it was when it was first written when editing or editing the article. Due to the nature of blogs, where the most recent posts are displayed at the top, this can be a major drawback.

 > Default format for "date": yyyy-mm-dd tt:mm:ss +0900

 Therefore, if "date" is set as in the above format, this problem can be prevented. At this time, the meaning of +0900 means the time zone of Korea. And for the rest, just put the time as it is now. The important point is that this time *does not have to be the current time*. Just think about the publication time of the post the user wants and insert it. However, it should be noted that if the time is later than the current time, it will be issued only after that time has passed.

 > On the homepage of jekyll, it is written that after time is optional. However, as a result of checking, it was confirmed that the date was entered only when the minimum time was entered. Please refer to this and enter 'date'. (Example: 2019-02-23 09:00)


#### Example of changing "date"
 In the figure below, the file name is set to 2019-02-03 under the title of 'date_test'. At this time, you can see that the post appeared on **'Feb 3, 2019'** in the same way on the web. And on the main screen, you can see that the 'date_test' post is located under the post 'My first blog post!' written on the same **'Feb 3, 2019'**.

<img src="https://github.com/newjin87/storage/blob/master/_img/jekyll/date1.png?raw=true" width="70%"><img src="https://github .com/newjin87/storage/blob/master/_img/jekyll/date2.png?raw=true" width="30%">

 What if we add "date" item to FrontMatter of 'date_test'? If you put '2019-02-04 15:08:12 +0900', which is the time after the file name, in the 'date' field as shown below, you can confirm that the post appears as **'Feb 4, 2019'** on the web. and **'My first blog post!' written on 'Feb 3, 2019'** It can also be confirmed that it is positioned higher than that!

<img src="https://github.com/newjin87/storage/blob/master/_img/jekyll/date3.png?raw=true" width="70%"><img src="https://github .com/newjin87/storage/blob/master/_img/jekyll/date4.png?raw=true" width="30%">
---
layout: post
title: 'Create a blog using jekyll (2): What you need to know before posting'
date: 2019-02-25 15:08:12 +0900
comments: true
categories: [Dev-Log]
tags: [GitHub-Pages, Jekyll, Blog-Setup]
---
> In the last post, we learned how to install jekyll and how to create a site using it. In this article, I would like to take a look at the things you need to know before posting in earnest on the site you created last time.


## Explore the installation folder

First, you need to look into the **myblog** folder where jekyll is installed.

<img src="https://github.com/newjin87/storage/blob/master/_img/jekyll/dir.png?raw=true">

* First, in the *_site* folder, there are files for sites that are ultimately displayed on the web.
* Second, in the *_posts* folder, postings are stored here.
* Among the files, one of the most important files is the *_config.yml* file, which records the properties of the website and can also be converted.

## Posts are in the "_ posts" folder!

Blog posts created through jekyll are stored in the **_posts** folder in the **myblog** folder. And in this, there is an example file *"2019-02-25-welcome-to-jekyll.markdown"* that explains the basic posting method. When you open it, you will see the following:

<img src="https://github.com/newjin87/storage/blob/master/_img/jekyll/front.png?raw=true">

As you can see from this figure, the post can be divided into two parts. The first is ***Front Matter*** written in YML and the bottom part is ***Contents***.
To put it simply, *Front Matter* is the part that specifies the format of the post, and *Contents* is the part where the content to be posted is entered.
In other words, what actually appears on the website is the content of *Contents*, and *Front Matter* appears only indirectly, such as in the title.
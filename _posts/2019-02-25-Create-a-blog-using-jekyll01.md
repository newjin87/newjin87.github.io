---
layout: post
title: "Create a blog using jekyll (1): Installing jekyll"
date: 2019-02-25 12:08:12 +0900
Categories: jekyll
comments: true
---

 >In this article, we will learn how to create a blog using jekyll. Jekyll is a software that can create simple blogs or static sites, and is based on a programming language called "ruby". Jekyll was created in 2008 by Tom Preston-Werner, who is also the co-founder of GitHub. Jekyll is the engine for GitHub Pages and one of the most popular static site generators.

## Advantages of jekyll

 One of the biggest advantages of jekyll is that it is easy to integrate with GitHub Pages. Github Pages is a web hosting service provided by GitHub based on jekyll. Users can get domains for free through Github Pages. And users can use GitHub Pages more easily through jekyll.

* Through jekyll, users can use Markdown instead of HTML.

* Users can decorate their site by using the theme provided by jekyll without using CSS.

![jekyllthemeChooser](https://help.github.com/assets/images/help/pages/select-theme.png)

## Then, is there any problem?

 Unfortunately, this is the biggest problem. It's just that it's difficult. Not only is it not a GUI format like Naver Blog or Tistory, but there are a lot of things you need to know, such as jekyll and GitHub. Therefore, I will focus on creating a blog through jekyll and GitHub through several articles. If you follow the blog posts well, there will be no big difficulties in creating and operating a blog.

## Let's install jekyll first.

**! The installation of jekyll** is done *from the terminal*. After opening the terminal, enter the following command: The order is in the order of installing **Ruby** - installing **jekyll**.

1. xcode-select --install // *Install command line tools.*

2. To install the latest **Ruby gem**, it is recommended to install it through Homebrew as follows.
```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"#*Install Homebrew*
$ brew install ruby ​​#*Install latest Ruby*
$ ruby ​​-v # *Check the version of Ruby*
```

**! If you have installed the Ruby gem**, you can now install **jekyll**.

1. sudo install bundler jekyll // Install *jekyll. At this time, SuperUser permission is required.*

2. *If the installation of jekyll is complete, you need to install the jekyll site. At this time, you need to create a main folder for managing your blog. (Let's think about the folder name, here * **"myblog"** *)*
```
$ jekyll new myblog #*Create a myblog folder and install jekyll there*
$ cd myblog # *Go to the myblog folder*
$ bundle exec jekyll serve # *Open a site on the local server and make it available for use.*
```
1. If you connect to *http://localhost:4000/, you can see that the blog has been created as follows.*
<img src="https://github.com/newjin87/storage/blob/master/_img/jekyll/firstpage.png?raw=true" width="80%">
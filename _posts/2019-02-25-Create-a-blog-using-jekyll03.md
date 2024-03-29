---
layout: post
title: "Create a blog using jekyll (3): Let's do a post"
Categories: jekyll
date: 2019-02-25 18:08:12 +0900
comments: true
---
>Before explaining this content, please note that I used the Atom editor in the Mac environment and explained based on using the Markdown language. In the case of an editor, you should use the editor you are comfortable with. If you use markdown, please use an editor that supports markdown.

## Let's check the example file

 Before posting in earnest, you need to check the example file *"2019-02-25-welcome-to-jekyll.markdown"*. First, you need to pay attention to the file name. The file name is composed of the following.

    > Date - Subject . extension

 In jekyll, blog posts must maintain this format. The reason is that the file name becomes the address of the posting.

<img src="https://github.com/newjin87/storage/blob/master/_img/jekyll/date.png?raw=true">

 As you can see in the above capture, you can see that *file name = posting address*. Therefore, if the file name is incorrect, the blog post itself will not be created, so you must specify the file name in the format specified in jekyll.
 It doesn't matter if you use Korean characters when designating a file name. Also, spaces are not recognized, so **"_"** must be used to express them. When using markdown, "md" or "markdown" can be used for the extension.
 Also, if *title* is not specified in *FrontMatter*, the title of the file appears on the blog main screen. However, if *title* is separately designated in *FrontMatter*, there is no need to make the file title in Korean or long, so you can create a file by referring to this.

## Let's do a post.

 Basically, in order to post, you must first create a file in the *"_posts"* folder as described above.

<img src="https://github.com/newjin87/storage/blob/master/_img/jekyll/title.png?raw=true">

 If you have created a file, you must first set Front Matter. Use **'_'** to set Front Matter as shown in the picture below, and enter appropriate information below it. And just save. At this time, be careful that **"layout"** must be set to post because the post is written in the form of a blog post.

<img src="https://github.com/newjin87/storage/blob/master/_img/jekyll/cate.png?raw=true">

 And if you connect to **localhost:4000**, you can see that there is a post title on the main screen. And if you click to enter, you can see that the post has been created with the address of the file name you created.

<img src="https://github.com/newjin87/storage/blob/master/_img/jekyll/post.png?raw=true" width="50%"><img src="https://github .com/newjin87/storage/blob/master/_img/jekyll/post1.png?raw=true" width="50%">
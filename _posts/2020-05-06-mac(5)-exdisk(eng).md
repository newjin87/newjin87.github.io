---
layout: post
title: "Get to know your Macbook (5): Decorate your external hard drive for Mac"
date: 2020-05-06 08:00:00 +0900
Categories: Mac
comments: true
tags: usb-c, external hard drive, seagate
---

![img](https://github.com/newjin87/storage/blob/master/_img/mac/mac5-1.jpg?raw=true)

 In the previous article (<a href = "">Getting to know the MacBook Pro (4): Resolving usb-c compatibility</a>), Seagate's USB-C type external hard drive for Mac was recommended for use with the MacBook. have. However, even this product has several limitations. In this article, we will look at how to use this external hard drive and how to make it more helpful for Mac expandability. I couldn't use it for other external hard drives due to cost, but it will be possible to use it.



## Install the driver and configure the file system

### 1. Understanding purpose and environment

The first thing to do before using an external hard drive is to set what purpose the external hard drive will be used for. General users who only use Windows computers do not need to worry about this. However, Mac users need to think about this issue. The reason is that the file system used by Mac and Windows is different. In the case of Mac, the file system called apfs and macOS extension is used, but in Windows, NTFS is generally used. And the biggest problem is the incompatibility between these two systems. In the case of a file system called ExFAT, which can be used in both OSs, it can be a good alternative, but it has a disadvantage in terms of stability. Therefore, Mac users need to think about how to use the external hard drive.

Reference site: [Wikipedia_Filesystem](https://en.wikipedia.org/wiki/%ED%8C%8C%EC%9D%BC_%EC%8B%9C%EC%8A%A4%ED%85 %9C)


### 2. Installing the Paragon driver

The way to solve this problem is to install the Paragon Driver from Seagate's homepage. This driver helps you to use a Mac OS Extended format disk on a Windows computer or an NTFS format disk on a Mac. However, since it is not installed on an external hard drive, there is the hassle of having to install this driver for each computer that uses the external hard drive. Also, it is said that it only applies to Seagate products, so you should refer to this when purchasing an external hard drive.
If you use this Paragon driver, you can solve the problems pointed out above to some extent. However, you have to make a choice according to your usage environment and purpose. In general, there are a small number of Mac users in Korea, and most computers are based on Windows. In this case, it is recommended to install in NTFS format so that it can be used on Windows. However, setting up the file system requires careful consideration before using an external hard drive because **format** of the disk must precede it.

Paragon driver: https://www.seagate.com/kr/en/support/software/paragon/


### 3. Setting the external hard drive file system through disk format

Setting up the file system through disk formatting is a task that does not matter whether it is performed before step 2 or at the same time. Disk formatting can be done in **Disk Utility**. After running Disk Utility through Spotlight search or Launchpad, select Erase at the top and set the format you want to proceed. If you follow the recommendation, you can proceed by selecting Microsoft NTFS.

![img](https://github.com/newjin87/storage/blob/master/_img/mac/mac5-2.png?raw=true)![img](https://github.com/newjin87/ storage/blob/master/_img/mac/mac5-3.png?raw=true)![img](https://github.com/newjin87/storage/blob/master/_img/mac/mac5-4.png ?raw=true)



### 4. Partition the external hard drive

However, despite these solutions, users still feel dissatisfied. That's the Mac's backup problem. Unfortunately, you can't back up your Mac to an NTFS-formatted external hard drive, even if you install Paragon drivers. If Time Machine tries to back up to an NTFS format external hard drive, you will see the following message. *And if you proceed with this, you will experience a catastrophe in which the file system is changed and all data is deleted at the same time.*

![img](https://github.com/newjin87/storage/blob/master/_img/mac/mac5-5.png?raw=true)


 Therefore, for users who want to back up their Mac to an external hard drive, it would be the best way to purchase another external hard drive and set it to the Mac OS extended format. However, for users who do not have the capacity to do so, it is recommended to partition the external hard drive. In the case of external hard partitions, you can proceed by selecting the partition in **Disk Utility**, similar to disk formatting. This problem can be solved by dividing the partition and setting the NTFS file system on one partition and the Mac OS Extended file system on the other partition.

![img](https://github.com/newjin87/storage/blob/master/_img/mac/mac5-6.png?raw=true)

## Issues still present

When using a Mac, several solutions were presented to overcome the limitations of external hard drives. If you follow the recommendations, I think it will be a solution to some extent. However, the process of partitioning is more complicated than expected, and there is a high probability that the data you have so far will be deleted.

For details on how to partition and how to partition without deleting data, check out the following article.

[Getting to know your Macbook (6): Setting up an external hard drive for backup]()
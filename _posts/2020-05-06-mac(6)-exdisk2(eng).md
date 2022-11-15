---
layout: post
title: "Getting to know your Macbook (6): Setting up an external hard drive for backup"
date: 2020-05-06 09:00:00 +0900
Categories: Mac
comments: true
tags: usb-c, external hard drive, seagate
---
Previous post: [Getting to know your Macbook (5): Decorating an external hard drive for Mac]()

## 1. Partition the external hard drive on the MacBook

 The most important way to solve this is to divide the external hard drive into partitions. Usually, only the hard disk is partitioned. However, even in the case of an external hard drive, partitions are possible, and using this, one external hard drive is divided into an NTFS format volume for file sharing and a macOS extension volume for Macbook backup. If you do this, you can use both methods. If you are not a user of Seagate products, it seems that you can divide it into two partitions, one in the EX-FAT format and the other in the MacOS extended format. would.

 **1) Run Disk Utility**

 First, after connecting the external hard drive, run Disk Utility. You can run Disk Utility through Spotlight or through Launchpad. After running Disk Utility, select the external hard drive you want to partition. Then select the partition in the top center part.

![img](https://github.com/newjin87/storage/blob/master/_img/mac/mac6-1.png?raw=true)

**2) Setting up partitions**
<img src= "https://github.com/newjin87/storage/blob/master/_img/mac/mac6-2.png?raw=true" width = 50%><img src= "https://github .com/newjin87/storage/blob/master/_img/mac/mac6-3.png?raw=true" width = 50%>

  After entering the partition, a window like the one on the left will appear. In this state, press the + button below the circle to create a partition. And set the name, format, and size as shown in the picture on the right. At this time, the existing work system must be checked. If the external hard drive is in the NTFS format, if you create a new macOS extended format volume, the partition operation will be performed after the disk is formatted. Methods for preventing such formatting will be described again below.

 If the explanation continues, the format setting can be set to macOS Extended (Journaled) if the existing external hard drive is NTFS, and NTFS if the existing file system is macOS Extended. And the size of the volume can be set appropriately based on the capacity of the Mac. (My MacBook is 256 gigabytes.) When all settings are complete, click the Apply button to execute.

![img](https://github.com/newjin87/storage/blob/master/_img/mac/mac6-4.png?raw=true)

 When finished, you can see that two volumes have been created as follows. You can also confirm that the files in the existing external hard drive are also intact.



## 2. What if the external hard drive is in NTFS format?

 If the file system of the external hard drive is NTFS and there are many precious files, is there any way to partition without damaging the files? Of course there is. However, even in this case, it is impossible if the file has a larger capacity than the size of the partition to be divided. The way to partition without deleting files is to proceed with partitioning in Windows. After partitioning in Windows, connect to Mac again and convert the volume for Mac backup to Mac OS extension method. It can be a bit complicated, so let's check it out through the video.

<iframe width="886" height="498" src="https://www.youtube.com/embed/KOtYlujDsDI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in -picture" allowfullscreen></iframe>
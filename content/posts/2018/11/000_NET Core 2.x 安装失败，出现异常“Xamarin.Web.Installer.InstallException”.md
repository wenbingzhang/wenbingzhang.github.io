---
url: /blog/macos/Hka7rLR0Q
title: "NET Core 2.x 安装失败，出现异常“Xamarin.Web.Installer.InstallException”"
date: 2018-11-30T06:25:07+08:00
description:
categories:
  - MacOS
tags:
  - MacOS
menu: main
---

> visual studio for mac 下载的安装包损坏的解决方法

## 错误代码

```
Visual Studio installation failed with exception 'Xamarin.Web.Installer.InstallException' (Attempt #3)
Message: Failed to attach DMG image '/Users/qatesting/Library/Caches/XamarinInstaller/Universal/downloads/visualstudioformac-7.6.10.27.dmg'. Error code 1.
Exception type: Xamarin.Web.Installer.InstallException
at Xamarin.Web.Installer.MacInstallationArchiveHandler.MountDmg (System.String path) [0x00059] in /Users/vsts/agent/2.139.1/work/1/installer/Xamarin.Web.Installer/MacInstallationArchiveHandler.Mac.cs:71
at Xamarin.Web.Installer.MacInstallationArchiveHandler.InstallDmg (System.String path, System.Boolean needsPrivileges) [0x0002f] in /Users/vsts/agent/2.139.1/work/1/installer/Xamarin.Web.Installer/MacInstallationArchiveHandler.Mac.cs:100
at Xamarin.Web.Installer.Installer.InstallationArchiveHandler.Install (System.String path, System.Boolean needsPrivileges) [0x00056] in /Users/vsts/agent/2.139.1/work/1/installer/Xamarin.Web.Installer/Installer/InstallationArchiveHandler.cs:33
at (wrapper dynamic-method) System.Object.CallSite.Target(System.Runtime.CompilerServices.Closure,System.Runtime.CompilerServices.CallSite,Xamarin.Web.Installer.Installer.InstallationArchiveHandler,string,object)
at Xamarin.Web.Installer.Installer.BaseSoftwareItem.InstallDownloadedItem (System.String url, Xamarin.Web.Installer.Installer.InstallationArchiveHandler handler, Xamarin.Web.Installer.DownloadServiceWorkItem download) [0x0025e] in /Users/vsts/agent/2.139.1/work/1/installer/Xamarin.Web.Installer/Installer/BaseSoftwareItem.cs:278
at Xamarin.Web.Installer.Installer.BaseSoftwareItem.Install (System.UInt32 tryNumber) [0x000ed] in /Users/vsts/agent/2.139.1/work/1/installer/Xamarin.Web.Installer/Installer/BaseSoftwareItem.cs:303
at Xamarin.Web.Installer.Installer.XamarinIDEBase.Install (System.UInt32 tryNumber) [0x00000] in /Users/vsts/agent/2.139.1/work/1/installer/Xamarin.Web.Installer/Installer/XamarinIDEBase.Mac.cs:74
at MacInstaller.WizardPageInstallationController.InstallationWorker () [0x001f1] in /Users/vsts/agent/2.139.1/work/1/installer/MacInstaller.Universal/WizardPageInstallationController.cs:551

```

## 解决方法

```
rm -rf ~/Library/Caches/XamarinInstaller/Universal

```

执行上面的命令后，然后重新打开安装程序，会重新下载并安装

## 原因解析

.net core安装程序下载的时候损坏了，导致安装失败，安装失败后没有重新下载，所以我们只能先删掉安装包，然后重新安装。
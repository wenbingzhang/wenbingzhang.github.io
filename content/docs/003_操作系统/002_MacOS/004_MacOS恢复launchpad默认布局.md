---
slug: "HJvNDli-4"
title: "📝 MacOS恢复launchpad默认布局"
date: 2019-01-03T02:49:14+08:00
bookComments: false
bookHidden: false
weight: 4
---


> 在Mac OS 中重置Launchpad布局

Launchpad可以作为从熟悉的类似iOS的图标网格界面在Mac上打开应用程序的快捷方式。如果您已经自定义了这些应用程序图标并在Launchpad中进行了排列，那么您可能会决定从头开始并将其顺序重置为首次购买Mac时的显示方式。如果要重新排列Launchpad图标的显示方式，这也很有用，但使用Launchpad解决某些显示错误也很有帮助，尤其是在图标未显示或显示不正确的情况下。

在OS X的早期版本中，用户可以通过转储一些数据库文件来刷新Launchpad内容，但在Mac OS和OS X

10.10.x以后，您需要使用默认命令字符串来重置Launchpad内容和布局代替。

如何在MacOS中重置Launchpad布局

打开终端应用程序并输入以下默认值写入命令字符串：

```bash
defaults write com.apple.dock ResetLaunchPad -bool true; killall Dock
```

点击返回并等待Dock重新启动并重启Launchpad

再次打开Launchpad时，布局将恢复为默认状态，将所有捆绑的应用程序放在Launchpad的第一个屏幕上，将第三方应用程序放到辅助（以及第三个，如果适用）屏幕上。

您现在可以根据需要重新排列Launchpad的图标和布局，或者只在第一个屏幕上保留Apple应用程序的默认布局，在后面的屏幕上添加第三方应用程序和添加内容。

这个默认的命令字符串是在stackexchange上找到的，虽然提到它的用户仍然列出旧的数据库转储技巧作为必要的步骤 - 在测试中，后面的

Launchpad数据库删除命令不需要简单地重置OS X中的Launchpad布局Yosemite 10.10 .x +。
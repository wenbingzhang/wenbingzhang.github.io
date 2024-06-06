---
slug: Sf4FF6x8cuYhVzoUgJ9dwg
title: 📝 MacOS签名
date: 2024-06-06 13:20:42+08:00
bookComments: false
bookHidden: false
bookCollapseSection: false
weight: 1
---

## 下载根证书
[https://www.apple.com/certificateauthority/DeveloperIDG2CA.cer](https://www.apple.com/certificateauthority/DeveloperIDG2CA.cer)

## 导入根证书

```bash
sudo security import ~/Downloads/DeveloperIDG2CA.cer \
-k /Library/Keychains/System.keychain \
-T /usr/bin/codesign \
-T /usr/bin/security \
-T /usr/bin/productbuild

```

## 查看和清理特殊属性

```
xattr -lr xxx.app
xattr -cr xxx.app

```

## 签发APP

```bash
codesign --deep --force --verbose --sign "xxxx" xxx.app
```

## 验证签名

```bash
 spctl --assess --type execute --verbose=4 xxx.app
```

## 参考文档

[https://testerhome.com/topics/33338](https://testerhome.com/topics/33338)

[https://www.apple.com/certificateauthority/](https://www.apple.com/certificateauthority/)

[https://www.jianshu.com/p/f420649fba42](https://www.jianshu.com/p/f420649fba42)
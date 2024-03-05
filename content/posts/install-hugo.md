+++
title = "hugo网站搭建过程"
description = ""
tags = [
    "hugo",
]
date = "2014-04-02"
categories = [
    "hugo"
]
menu = "main"
+++

## 安装Hugo
下载地址：{{<link href="https://github.com/gohugoio/hugo/releases" text="https://github.com/gohugoio/hugo/releases" target="_blank">}}

## 创建网站
```bash
hugo new site book
cd book
git init
git submodule add https://github.com/alex-shpak/hugo-book themes/hugo-book
```

## 本地调试
```bash
hugo server --disableFastRender --minify --ignoreCache
```

## github actions
```bash
mkdir -p .github/workflows
touch .github/workflows/build.yml
```
```yaml
name: Build
on:
  push:
    branches:
      - main  # Set a branch to deploy
  pull_request:

jobs:
  deploy:
    runs-on: ubuntu-20.04
    concurrency:
      group: ${{ github.workflow }}-${{ github.ref }}
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true  # Fetch Hugo themes (true OR recursive)
          fetch-depth: 0    # Fetch all history for .GitInfo and .Lastmod

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: '0.123.7'
          # 是否启用 hugo extend
          extended: true

      - name: Build
        run: hugo --minify

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        if: ${{ github.ref == 'refs/heads/main' }}
        with:
          github_token: ${{ secrets.GH_PAGE_ACTION_TOKEN }}
          publish_dir: ./public
```

## github pages
  可以在项目的Settings中开启Pages服务，然后选择Branch为`gh-pages`即可。
  如果想要定制域名，可以参考官方文档 {{<link href="https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages" text="About custom domains and GitHub Pages" target="_blank">}}
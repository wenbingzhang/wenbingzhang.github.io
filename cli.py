#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from datetime import datetime
import time
from typing import Optional
from typing import List
import uuid as _uuid
import math
import binascii
import os
import pathlib
import fnmatch
import argparse

YAML_DELIM_LF = "---"


class ShortUUID(object):
    def __init__(self, alphabet: Optional[str] = None) -> None:
        if alphabet is None:
            alphabet = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ" "abcdefghijkmnopqrstuvwxyz"

        self.set_alphabet(alphabet)

    def int_to_string(
        self, number: int, alphabet: List[str], padding: Optional[int] = None
    ) -> str:
        """
        Convert a number to a string, using the given alphabet.

        The output has the most significant digit first.
        """
        output = ""
        alpha_len = len(alphabet)
        while number:
            number, digit = divmod(number, alpha_len)
            output += alphabet[digit]
        if padding:
            remainder = max(padding - len(output), 0)
            output = output + alphabet[0] * remainder
        return output[::-1]

    def string_to_int(self, string: str, alphabet: List[str]) -> int:
        """
        Convert a string to a number, using the given alphabet.

        The input is assumed to have the most significant digit first.
        """
        number = 0
        alpha_len = len(alphabet)
        for char in string:
            number = number * alpha_len + alphabet.index(char)
        return number

    @property
    def _length(self) -> int:
        """Return the necessary length to fit the entire UUID given the current alphabet."""
        return int(math.ceil(math.log(2**128, self._alpha_len)))

    def encode(self, uuid: _uuid.UUID, pad_length: Optional[int] = None) -> str:
        """
        Encode a UUID into a string (LSB first) according to the alphabet.

        If leftmost (MSB) bits are 0, the string might be shorter.
        """
        if not isinstance(uuid, _uuid.UUID):
            raise ValueError("Input `uuid` must be a UUID object.")
        if pad_length is None:
            pad_length = self._length
        return self.int_to_string(uuid.int, self._alphabet, padding=pad_length)

    def decode(self, string: str, legacy: bool = False) -> _uuid.UUID:
        """
        Decode a string according to the current alphabet into a UUID.

        Raises ValueError when encountering illegal characters or a too-long string.

        If string too short, fills leftmost (MSB) bits with 0.

        Pass `legacy=True` if your UUID was encoded with a ShortUUID version prior to
        1.0.0.
        """
        if not isinstance(string, str):
            raise ValueError("Input `string` must be a str.")
        if legacy:
            string = string[::-1]
        return _uuid.UUID(int=self.string_to_int(string, self._alphabet))

    def uuid(self, name: Optional[str] = None, pad_length: Optional[int] = None) -> str:
        """
        Generate and return a UUID.

        If the name parameter is provided, set the namespace to the provided
        name and generate a UUID.
        """
        if pad_length is None:
            pad_length = self._length

        # If no name is given, generate a random UUID.
        if name is None:
            u = _uuid.uuid4()
        elif name.lower().startswith(("http://", "https://")):
            u = _uuid.uuid5(_uuid.NAMESPACE_URL, name)
        else:
            u = _uuid.uuid5(_uuid.NAMESPACE_DNS, name)
        return self.encode(u, pad_length)

    def random(self, length: Optional[int] = None) -> str:
        """Generate and return a cryptographically secure short random string of `length`."""
        if length is None:
            length = self._length

        random_num = int(binascii.b2a_hex(os.urandom(length)), 16)
        return self.int_to_string(random_num, self._alphabet, padding=length)[:length]

    def get_alphabet(self) -> str:
        """Return the current alphabet used for new UUIDs."""
        return "".join(self._alphabet)

    def set_alphabet(self, alphabet: str) -> None:
        """Set the alphabet to be used for new UUIDs."""
        # Turn the alphabet into a set and sort it to prevent duplicates
        # and ensure reproducibility.
        new_alphabet = list(sorted(set(alphabet)))
        if len(new_alphabet) > 1:
            self._alphabet = new_alphabet
            self._alpha_len = len(self._alphabet)
        else:
            raise ValueError(
                "Alphabet with more than " "one unique symbols required.")

    def encoded_length(self, num_bytes: int = 16) -> int:
        """Return the string length of the shortened UUID."""
        factor = math.log(256) / math.log(self._alpha_len)
        return int(math.ceil(factor * num_bytes))


def get_weight(filename):
    s = pathlib.Path(filename).name
    if s == '_index.md':
        s = pathlib.Path(filename).parent.name
    s_arr = s.split("_", maxsplit=1)
    weight = int(s_arr[0]) if len(s_arr) > 1 else None
    return weight


def mkdir_p(filename):
    s = pathlib.Path(filename).name
    if s == '_index.md':
        # 获取filename的父目录并创建目录
        parent_dir = pathlib.Path(filename).parent
        if not parent_dir.exists():
            parent_dir.mkdir(parents=True)


def find_md_files(directory):
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file, "*.md"):
                md_files.append(os.path.join(root, file))
    return md_files


def generate_date():
    # 获取当前时间
    current_time = datetime.now()
    tzinfo = datetime.fromtimestamp(time.time()).astimezone().tzinfo
    return datetime(current_time.year, current_time.month, current_time.day,
                    current_time.hour, current_time.minute, current_time.second, tzinfo=tzinfo)


def generate_uuid():
    shortuuid = ShortUUID()
    return shortuuid.uuid()


def update_weight(filename):
    # 读取Markdown文件内容
    with open(filename, "r", encoding="utf-8") as file:
        markdown_content = file.read()

    # 以换行符分割内容为行
    lines = markdown_content.split("\n")

    # 查找元数据
    is_metadata = False
    metadata = {}
    body_index = 0
    for index, line in enumerate(lines):
        if line.strip() == YAML_DELIM_LF:
            is_metadata = not is_metadata

        if index == 0 and not is_metadata:
            break

        if line.strip() == YAML_DELIM_LF and index > 0:
            body_index = index + 1
            break

        if is_metadata:
            # 解析元数据键值对
            parts = line.split(":", maxsplit=1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                metadata[key] = value

    # s = pathlib.Path(filename).name
    # if s == '_index.md':
    #     s = pathlib.Path(filename).parent.name
    # s_arr = s.split("_", maxsplit=1)
    # weight = int(s_arr[0]) if len(s_arr) > 1 else None

    # 获取权重
    weight = get_weight(filename)
    # 更新权重
    if metadata.get("weight", None) == str(weight):
        return
    if weight is not None:
        metadata["weight"] = str(weight)

    # # 打印内容
    # print(YAML_DELIM_LF)
    # for key, value in metadata.items():
    #     print(f"{key}: {value}")
    # print(YAML_DELIM_LF)
    # print("\n".join(lines[body_index:]))

    # 写入文件
    with open(filename, "w", encoding="utf-8") as output_file:
        output_file.write(YAML_DELIM_LF + "\n")
        for key, value in metadata.items():
            output_file.write(f"{key}: {value}\n")
        output_file.write(YAML_DELIM_LF + "\n")
        output_file.write("\n".join(lines[body_index:]))

    print("更新成功：", filename)


def create_doc(filename):
    # 创建目录
    mkdir_p(filename)

    # 获取权重
    weight = get_weight(filename)
    if weight is None:
        weight = 999

    matedata = '''
---
slug: %s
title: "📝 默认标题"
date: %s
bookComments: false
bookHidden: false
weight: %d
---
    ''' % (generate_uuid(), generate_date(), weight)

    with open(filename, "w", encoding="utf-8") as output_file:
        output_file.write(matedata.strip() + "\n")


def create_post(filename):
    # 创建目录
    mkdir_p(filename)

    matedata = '''
---
slug: %s
title: 默认标题
description:
tags:
  - 默认标签
date: %s
categories:
  - 默认分类
menu: main
---
    ''' % (generate_uuid(), generate_date())

    with open(filename, "w", encoding="utf-8") as output_file:
        output_file.write(matedata.strip() + "\n")


def parse_args():
    parser = argparse.ArgumentParser(description="hugo-book 帮助工具")
    command_subparsers = parser.add_subparsers(dest='command', help='可用的子命令')
    # 自动更新权重
    supdate_weight_parser = command_subparsers.add_parser(
        'auto_weight', help='自动更新权重')
    supdate_weight_parser.add_argument('website_root', type=str, help='站点根目录')

    # 创建新文档
    supdate_weight_parser = command_subparsers.add_parser(
        'create_doc', help='创建新文档')
    supdate_weight_parser.add_argument('doc_filename', type=str, help='文档名称')

    # 创建新文章
    supdate_weight_parser = command_subparsers.add_parser(
        'create_post', help='创建新文章')
    supdate_weight_parser.add_argument('post_filename', type=str, help='文章名称')

    # uuid
    command_subparsers.add_parser('uuid', help='生成uuid')

    # datetime
    command_subparsers.add_parser('datetime', help='生成当前日期时间')

    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == 'auto_weight':
        docs_dir = os.path.join(args.website_root, "content/docs")
        files = find_md_files(docs_dir)
        for file in files:
            update_weight(file)
    elif args.command == 'create_doc':
        create_doc(args.doc_filename)
    elif args.command == 'create_post':
        create_post(args.post_filename)
    elif args.command == 'uuid':
        shortuuid = ShortUUID()
        print(shortuuid.uuid())
    elif args.command == 'datetime':
        print(generate_date())


if __name__ == "__main__":
    main()

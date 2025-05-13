---
slug: 7aUahQG8NNxm5ydhxzqRNr
title: 📝 调用Python代码
date: 2025-02-10 17:42:52+08:00
bookComments: false
bookHidden: false
bookCollapseSection: false
weight: 1
---


```cpp
#include <cstdio>
#include <iostream>
#include <Python.h>  // 包含 Python 头文件

int main() {
    // 初始化 Python 解释器
    Py_Initialize();

    // 创建一个 Python 字典来传递参数
    PyObject* pName = PyUnicode_FromString("__main__");
    PyObject* pModule = PyImport_Import(pName);
    Py_XDECREF(pName);

    if (pModule != nullptr) {
        // 创建一个全局字典来存储参数
        PyObject* pGlobals = PyModule_GetDict(pModule);

        // 将参数作为 Python 对象添加到全局字典中
        PyDict_SetItemString(pGlobals, "param1", PyLong_FromLong(42));  // 示例参数1
        PyDict_SetItemString(pGlobals, "param2", PyUnicode_FromString("Hello from C++"));  // 示例参数2

        // 定义并执行 Python 代码
        const char* script = R"(
import platform
import sys
import os

system_info = {
    'param1': param1,
    'param2': param2,
    'OS': platform.system(),
    'OS Version': platform.version(),
    'Release': platform.release(),
    'Machine': platform.machine(),
    'Processor': platform.processor(),
    'Python Version': sys.version,
}

print(system_info)
)";

        // 执行 Python 代码
        const auto result = PyRun_SimpleString(script);
        std::cout << "Result from Python: " << result << std::endl;

        Py_XDECREF(pModule);
    } else {
        PyErr_Print();
        std::cerr << "Failed to load the Python script" << std::endl;
    }

    // 关闭 Python 解释器
    Py_Finalize();
    return 0;
}
```
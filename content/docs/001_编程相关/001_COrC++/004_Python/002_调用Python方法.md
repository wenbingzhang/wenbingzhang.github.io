---
slug: gqCi9RiUgfetRibe6j6Fou
title: 📝 调用Python方法
date: 2025-02-10 17:44:56+08:00
bookComments: false
bookHidden: false
bookCollapseSection: false
weight: 2
---

```cpp
#include <Python.h>
#include <iostream>

int main() {
    // 初始化 Python 解释器
    Py_Initialize();

    // 创建 Python 字典并将参数传递给 Python
    PyObject* pName = PyUnicode_FromString("__main__");
    PyObject* pModule = PyImport_Import(pName);
    Py_XDECREF(pName);

    if (pModule != nullptr) {
        // 创建一个全局字典来存储参数
        PyObject* pGlobals = PyModule_GetDict(pModule);

        // 创建 Python 函数
        const char* func_code = R"(
def my_function(param1, param2):
    return f"Received param1: {param1}, param2: {param2}"
)";

        // 执行定义函数的代码
        PyRun_SimpleString(func_code);

        // 获取 Python 函数对象
        PyObject* pFunc = PyDict_GetItemString(pGlobals, "my_function");

        if (PyCallable_Check(pFunc)) {
            // 准备参数
            PyObject* pArgs = PyTuple_Pack(2, PyLong_FromLong(42), PyUnicode_FromString("Hello from C++"));

            // 调用函数
            PyObject* pValue = PyObject_CallObject(pFunc, pArgs);
            if (pValue != nullptr) {
                // 打印函数返回值
                std::cout << "Function returned: " << PyUnicode_AsUTF8(pValue) << std::endl;
                Py_XDECREF(pValue);
            } else {
                PyErr_Print();
            }
            Py_XDECREF(pArgs);
        } else {
            PyErr_Print();
        }
    } else {
        PyErr_Print();
        std::cerr << "Failed to load the Python module" << std::endl;
    }

    // 关闭 Python 解释器
    Py_Finalize();
    return 0;
}
```
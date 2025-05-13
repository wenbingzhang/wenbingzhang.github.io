---
slug: PkdRvN9md3GGFMbXaHx4EF
title: 📝 注册Python模块
date: 2025-02-10 17:49:08+08:00
bookComments: false
bookHidden: false
bookCollapseSection: false
weight: 3
---

```cpp
#include <Python.h>
#include <iostream>

// 示例结构体（C++对象）
struct MyStruct {
    int value;
};

// C++ 从 Python 获取 `void*` 并使用
static PyObject* use_object(PyObject* self, PyObject* args) {
    PyObject* capsule;
    if (!PyArg_ParseTuple(args, "O", &capsule)) {
        return nullptr;
    }

    // 取回 `void*` 并转换回 C++ 指针
    auto* obj = static_cast<MyStruct*>(PyCapsule_GetPointer(capsule, "this"));
    if (!obj) {
        PyErr_SetString(PyExc_RuntimeError, "Invalid capsule!");
        return nullptr;
    }

    std::cout << "Received C++ object with value: " << obj->value << std::endl;
    return PyLong_FromLong(obj->value);
}

// Python 方法表
static PyMethodDef CppMethods[] = {
    {"use_object", use_object, METH_VARARGS, "Use a C++ object from PyCapsule"},
    {nullptr, nullptr, 0, nullptr}
};

// Python 模块定义
static struct PyModuleDef cppModule = {
    PyModuleDef_HEAD_INIT, "cppModule", nullptr, -1, CppMethods
};

// 初始化 Python 模块
PyMODINIT_FUNC PyInit_cppModule(void) {
    return PyModule_Create(&cppModule);
}

int main() {
    // 初始化 Python 解释器
    Py_Initialize();
    PyObject* pModule = PyImport_AddModule("__main__");
    PyObject* pGlobals = PyModule_GetDict(pModule);

    // 注册 C++ 方法到 Python
    PyObject* pCppModule = PyModule_Create(&cppModule);
    PyDict_SetItemString(pGlobals, "cppModule", pCppModule);

    // 执行 Python 代码
    const auto python_code = R"(
def my_function(capsule):
    result = cppModule.use_object(capsule)  # 传回 C++ 处理
    print(f"Python received: {result}")
    return result
)";
    PyRun_SimpleString(python_code);

    // 获取 Python 函数对象
    if (PyObject* pFunc = PyDict_GetItemString(pGlobals, "my_function"); PyCallable_Check(pFunc)) {
        auto* obj = new MyStruct{42};  // 创建 C++ 对象
        const auto capsule = PyCapsule_New(obj, "this", nullptr); // 返回封装的指针
        // 准备参数
        PyObject* pArgs = PyTuple_Pack(1, capsule);

        // 调用函数
        if (PyObject* pValue = PyObject_CallObject(pFunc, pArgs); pValue != nullptr) {
            // 打印函数返回值
            std::cout << "Function returned: " << PyLong_AsLong(pValue) << std::endl;
            Py_XDECREF(pValue);
        } else {
            PyErr_Print();
        }
        Py_XDECREF(pArgs);
    } else {
        PyErr_Print();
    }

    // 关闭 Python 解释器
    Py_Finalize();
    return 0;
}
```
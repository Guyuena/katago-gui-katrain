对于一个python项目，里面的每一个文件夹都可以认为是一个package，而每一个.py文件被认为是一个module。如果你用的IDE是PyCharm，
那么当你新建一个Python Package的时候，PyCharm都会自动为你新建一个__init__.py文件。
这个__init__.py文件可以看作这个package的初始化文件

2. __init__.py文件在做什么？
要了解__init__.py有什么用，首先要理解他在坐什么？我们举一个简单的例子：

文件目录如下

"""
.
├── demo.py
├── package
|   ├── __init__.py
|   ├── module.py
"""
demo.py文件如下

# demo.py

import package
__init__.py文件如下

# __init__.py

print("__init.py file is called!")
那么当我执行demo.py文件时，输出结果如下

$ python demo.py 
__init.py file is called!
这说明__init__.py中的代码被执行了。如果把demo.py中的 import package 换成import package.module也是一样的结果。
这说明，当我们从一个package里面调用东西的时候，该__init__.py文件内的代码会被首先执行。

3. __init__.py文件有什么用？
3.1 简化import语法
假设在module.py文件中有一个函数a_function()如下

# module.py

def a_function():
    print("Test function is called!")
如果我现在想从demo.py中调用它，没有__init__.py文件的话，只能这么写（方法一）

# demo.py

from package.module import a_function

a_function()
但是我可以在__init__.py中进行如下定义

# __init__.py

from package.module import a_function
这样定义完了以后在demo.py就可以如下调用了（方法二）

# demo.py

from package import a_function

a_function()
好像也没简洁到哪儿去？试想，如果你在package里面有几十个module，那么当你想调用这几十个module里面的几十上百个函数的时候，
你就需要在demo.py文件中写几十行import语句，这样无疑是不简洁的。而采用方法二的办法，你就可以把这些import语句统统放进__init__.py文件。
但这不是__init__.py最重要的用途，最重要的是下面两点。

3.2 批量导入和规范化导入以及__all__
如果你在module.py中定义了很多函数，你想在demo.py中调用，怎么办呢？如module.py中有两个函数

# module.py

def a_function_1():
    print("Test function 1 is called!")

def a_function_2():
    print("Test function 2 is called!")
先在__init__.py批量导入

# __init__.py

from package.module import *
再在demo.py中批量导入

# demo.py

from package import *

a_function_1()
这样就可以实现package中诸多函数的批量导入了。注意批量导入遵从覆盖原则，即如果有多个类和方法名字相同，那么后导入的会覆盖先导入的。

但是如果你只允许a_function_1被外界调用呢，就可以把__init__.py改成

# __init__.py

from package.module import a_function_1
这样在demo.py文件中，调用a_function_2就会报错。

# demo.py

from package import *

a_function_2()    # 这里就会报错
更优雅一点可以调用__all__属性，在__init__.py中定义可以被外界调用的类和方法，如

# __init__.py

__all__ = ['a_function_1']     # 这样，在demo.py只能调用a_function_1方法

from package.module import *
这里举的例子都是函数/方法，对于类来说，是一样的。
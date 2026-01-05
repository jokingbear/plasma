from .context import CONTEXT
from . import package_11, sub_modules
from .class1 import Class1
from .class2 import Class2
from .class4 import Class4
from .class5 import Class5
from ..package2 import CONTEXT as p2_context


CONTEXT\
    .register(
        class1=Class1,
        class2=Class2,
        class4=Class4,
        class5=Class5
    )\
    .link_name(p2_context)

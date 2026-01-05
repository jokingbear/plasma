from . import context, package_11
from .class1 import Class1
from .class2 import Class2
from .class4 import Class4
from .class5 import Class5
from plasma.meta.object_graph.auto import register


register(
    class1=Class1,
    class2=Class2,
    class4=Class4,
    class5=Class5
)

import os
import sys

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        # 在被 Nuitka 编译后的环境中，根据你的打包设置来调整
        base_path = os.path.dirname(sys.executable)
    else:
        # 在开发环境中，可能需要不同的路径处理
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
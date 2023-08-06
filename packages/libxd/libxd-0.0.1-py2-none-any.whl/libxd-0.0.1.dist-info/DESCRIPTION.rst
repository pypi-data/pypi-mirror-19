# libxd

## 函数列表

### 1. 给出文件路径获得去掉了扩展名的文件名

```python
from libxd.io import FileUtils

path = '/path/to/index.html'
FileUtils.file_name(path)  # result is index
```


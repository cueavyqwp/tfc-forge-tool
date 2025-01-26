<div align="center">

# 锻造工具

为[TerraFirmaCraft](https://github.com/TerraFirmaCraft/TerraFirmaCraft)模组写的锻造工具

---

## 资源包
[1.7.10](./assets/Forge-Tool-1.7.zip)|[1.12.2](./assets/Forge-Tool-1.12.zip)|[1.18.2](./assets/Forge-Tool-1.18.zip)|[1.20.1](./assets/Forge-Tool-1.20.zip)

---

</div>

## 使用说明

使用前先从[上方](#资源包)安装对应版本资源包

### 运行

点击此处[main.zip](https://github.com/cueavyqwp/tfc-forge-tool/archive/refs/heads/main.zip)下载源码

解压后找到`tfc_anvil.py`文件

使用使用python3.10及以上版本来运行

`python tfc_anvil.py`

### 操作界面

- **起始位置** : 即绿色箭头位置
- **结束位置** : 既红色箭头位置
- **末尾** : 分为三个下拉框,从上到下分别为`末尾` `倒数第二` `倒数第三` 要是有空的选择`任意`操作
- **输出** : 点击后会将锻造步骤输出到下方文本框内

### 保存与加载

输入好数据之后点击保存按钮即可保存为JSON文件

点击加载按钮选择保存好的JSON文件即可加载(不会改变起始位置)

### 快捷键

- `Ctrl+l` : 加载
- `Ctrl+s` : 保存
- `Enter` : 输出
- `Delete` : 清空

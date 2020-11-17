# CO 自动评测机

支持三种仿真工具的自动化调用，支持对输出序列的判别比较并对每组测试数据输出评测结果。

操作系统： Windows

所需运行环境：python3/Anaconda3，仿真软件支持 ISE/ModelSim/iVerilog 。

## 说明

每一次评测采用一个 .json 文件来描述，分为标准模式和对拍模式。目前仅支持手动编写评测配置的 .json 文件。

标准评测示例：
```json
{
    "name": "Demo Standard Task",
    "mode": "standard", 
    "src": "your_path\\mips.zip",
    "tool": "ise",
    "testcases": [
        "WeakTest1",
        "jump",
        "loadstore"
    ]
}
```
对拍示例：
```json
{
    "name": "Demo Pat Task",
    "mode": "pat", 
    "src1": "your_path\\others.zip",
    "src2": "your_path\\yours.zip",
    "tool": "iverilog",
    "testcases": [
        "jump",
        "loadstore"
    ]
}
```
**注意：json文件的格式必须参照例子，不得缺少任何一个必须的key!!**
选项说明：
- `name` : 评测任务的名称
- `mode` : 评测模式，只有两种值( `"standard"` : 标准模式， `"pat"` : 对拍模式)
- `src`  : 源代码路径，要求与向 cscore 提交的一致，为一个含有顶层模块 `mips.v` 的压缩包。
  - 注意：压缩包内不要含有自己的 testbench ，也不要采用 `tb.v` 命名 CPU 部件，以免发生意外的错误。
  - 如果是对拍模式则不需要 `src` 但是需要 `src1` 和 `src2` 。
- `tool` : 选用的仿真工具，只有三种值(`ise`, `iverilog`, `modelsim`)
- `testcases` : 本次评测所选取的测试数据集，为一个列表，每一项是一个测试数据的名称(稍后说明)

## 主要功能以及使用方法

### 本地评测 CPU

1. 建立好一个空的文件夹并新建一个 `.json` 文件，参考上述示例填好空。
2. 采用命令行调用 `python3 -u main.py -run [你建立的.json]`

### 导入测试数据

本功能仅支持自动导入 `.asm` 格式的汇编程序。本功能需要采用命令行的 `-load` 选项，本套评测机将利用 Mars 生成机器码并运行出输出序列结果，将其存储进默认的测试数据路径并添加到测试集中。

1. 准备好要导入的汇编程序。
2. 命令行调用 `python3 -u main.py -load [你准备的.asm]`

### 删除测试数据(手动)

目前仅能手动删除测试数据，进入全局配置文件 `configs/global.json` 中找到 `testcases` 字段，手动删去想要删除的测试数据即可。


## 一些全局的配置
在 `configs/global.json` 中含有一些全局的配置，在 `configs/simulator` 中有对于每种仿真工具的配置。

### 全局配置 `global.json`

这个文件中的字段有：
- `identifier` : 评测机的名字，可以自己取。
- `defaultTestcasePath` : 默认用来导入测试数据的路径(绝对路径或者相对于评测机主程序 `main.py` 的相对路径)。
- `testcases` : 支持的测试数据，每个测试数据包含的信息有测试数据名称和用来描述这组数据的 `.json` 文件的路径。
- `simulatorSupported` : 支持的仿真工具。这项不要随意修改。
- `marsPath` : 指定生成测试数据所选用的 Mars （一般为魔改 Mars ）

注意：在本配置文件中所有的路径都是绝对路径或者相对于评测机主程序的相对路径。

### 仿真软件的配置文件

在 `configs/simulator` 中，每个 `.json` 文件中最主要的字段为仿真软件的安装路径，使用时根据本机的配置修改即可。**注意：仿真软件的安装路径建议用绝对路径并且只能使用 Windows 的反斜杠！**


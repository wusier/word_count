# 多模式中文文本字频统计工具

这是一个高效的中文文本字频统计工具，旨在提供一个兼具命令行便捷性和图形化界面直观性的解决方案。项目采用 MapReduce 的思想对核心算法进行拆分，使其具备处理大规模文本的潜力。

## 项目亮点

- **双模式启动 (Dual-Mode)**: 同一份代码支持 **命令行 (CLI)** 和 **图形用户界面 (GUI)** 两种启动模式，满足不同用户场景的需求。
- **算法思想**: 核心逻辑借鉴了 **MapReduce** 的分布式计算思想，将任务分解为 `clean`, `map`, `reduce` 等阶段，代码结构清晰，易于理解和扩展。
- **工程实践**: 使用 `argparse` 库处理命令行参数，使用 `Tkinter` 构建GUI，展示了将算法落地为实用工具的工程能力。
- **高可读性**: 代码注释清晰，函数功能单一，遵循良好的编程规范。

## 功能列表

- [x] **文本清洗**: 自动移除所有非中文字符和标点符号。
- [x] **字频统计**: 精确统计输入文本中每个汉字出现的频率。
- [x] **命令行模式**: 支持通过命令行参数直接指定输入/输出文件路径，便于自动化和脚本集成。
    - `python word_count_gui.py --input_file <path> --output_file <path>`
- [x] **GUI模式**: 提供一个简单的图形界面，用户可以通过点击按钮选择文件并查看统计结果。
- [x] **结果展示**: 统计结果按字频降序排列，并可保存到指定文件。

## 技术栈

- **语言**: Python
- **GUI**: Tkinter (Python标准库)
- **命令行解析**: argparse (Python标准库)
- **核心数据结构**: `collections.Counter`

## 如何运行

1.  **克隆仓库**
    ```bash
    git clone [https://github.com/wusier/word_count]
    cd [word_count]
    ```

2.  **准备环境**
    本项目仅使用Python标准库，无需安装额外依赖。推荐使用 Python 3.6+。

3.  **运行模式**

    *   **GUI 模式 (直接运行):**
        ```bash
        python word_count_gui.py
        ```
        程序将弹出一个图形界面，按照提示操作即可。

    *   **命令行模式 (指定输入输出):**
        ```bash
        # 准备一个名为 input.txt 的输入文件
        python word_count_gui.py --input_file input.txt --output_file result.txt
        ```
        程序将在后台完成统计，并将结果保存到 `result.txt` 文件中。


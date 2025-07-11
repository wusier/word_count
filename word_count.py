# word_count_gui.py

import re
from collections import Counter
import argparse
import sys
import os
file_path="lunyu.txt"
# --- 核心功能函数 (与之前完全相同) ---
def clean_text(text):
    """移除文本中的标点符号和非中文字符"""
    text = re.sub(r"[^\u4e00-\u9fa5]", "", text)
    return text

def map_phase(text):
    """Map阶段：将文本中的每个字映射为 (字, 1) 的形式"""
    words = list(text)
    return [(word, 1) for word in words]

def reduce_phase(mapped_values):
    """Reduce阶段：聚合所有键值对，计算每个字的总数"""
    word_counts = Counter()
    for word, count in mapped_values:
        word_counts[word] += count
    return word_counts

def get_top_n_words(word_counts, n):
    """获取频率最高的 N 个字"""
    return word_counts.most_common(n)

def process_file(file_path, top_n):
    """处理文件的完整流程，并返回格式化后的结果字符串"""
    try:
        # 尝试用 gbk 解码，如果不行再尝试 utf-8
        try:
            with open(file_path, 'r', encoding='gbk', errors='ignore') as f:
                text = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()

        cleaned_text = clean_text(text)
        mapped_values = map_phase(cleaned_text)
        word_counts = reduce_phase(mapped_values)
        top_words = get_top_n_words(word_counts, top_n)

        # 构建结果字符串
        result_lines = [f"文件 '{os.path.basename(file_path)}' 的词频统计结果 (Top {top_n}):\n"]
        for word, count in top_words:
            result_lines.append(f"字: '{word}'  出现次数: {count}")
        return "\n".join(result_lines)

    except FileNotFoundError:
        return f"错误：找不到文件 '{file_path}'"
    except Exception as e:
        return f"处理文件时发生未知错误: {e}"

# --- 图形用户界面 (GUI) 部分 ---
def run_gui():
    """运行图形用户界面"""
    import tkinter as tk
    from tkinter import filedialog, messagebox, scrolledtext

    def select_file():
        """打开文件选择对话框"""
        filepath = filedialog.askopenfilename(
            title="请选择一个 TXT 文本文件",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filepath:
            entry_path.delete(0, tk.END)
            entry_path.insert(0, filepath)

    def start_analysis():
        """开始分析按钮的回调函数"""
        filepath = entry_path.get()
        top_n_str = entry_top_n.get()

        if not filepath:
            messagebox.showerror("错误", "请先选择一个文件！")
            return
        
        try:
            top_n = int(top_n_str)
            if top_n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("错误", "Top N 必须是一个正整数！")
            return
            
        # 显示"处理中"并禁用按钮
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "正在处理中，请稍候...\n")
        window.update_idletasks() # 刷新界面以显示消息
        btn_start.config(state=tk.DISABLED)

        # 调用核心处理函数
        result = process_file(filepath, top_n)
        
        # 显示结果并重新启用按钮
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result)
        btn_start.config(state=tk.NORMAL)


    # 创建主窗口
    window = tk.Tk()
    window.title("词频统计工具")
    window.geometry("500x400") # 设置窗口大小

    # 创建并放置控件
    frame_top = tk.Frame(window)
    frame_top.pack(pady=10, padx=10, fill=tk.X)

    tk.Label(frame_top, text="文件路径:").pack(side=tk.LEFT)
    entry_path = tk.Entry(frame_top)
    entry_path.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    btn_select = tk.Button(frame_top, text="浏览...", command=select_file)
    btn_select.pack(side=tk.LEFT)

    frame_middle = tk.Frame(window)
    frame_middle.pack(pady=5, padx=10, fill=tk.X)
    
    tk.Label(frame_middle, text="Top N 值:").pack(side=tk.LEFT)
    entry_top_n = tk.Entry(frame_middle, width=10)
    entry_top_n.insert(0, "10") # 默认值
    entry_top_n.pack(side=tk.LEFT, padx=5)
    
    btn_start = tk.Button(frame_middle, text="开始统计", command=start_analysis)
    btn_start.pack(side=tk.LEFT, padx=20)
    
    # 创建结果显示区域
    result_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, height=15)
    result_text.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

    # 运行窗口主循环
    window.mainloop()


# --- 程序主入口 ---
if __name__ == "__main__":
    # 检查命令行参数中是否有 '--path'
    # sys.argv 是一个包含所有命令行参数的列表
    if '--path' in sys.argv:
        # 如果有 --path，则使用命令行模式
        parser = argparse.ArgumentParser(description='命令行词频统计工具。')
        parser.add_argument('--path', type=str, required=True, help='输入文本文件的路径')
        parser.add_argument('--top_n', type=int, default=10, help='显示频率最高的N个词')
        args = parser.parse_args()
        
        result = process_file(args.path, args.top_n)
        print(result)
    else:
        # 如果没有 --path 参数（比如双击运行时），则启动 GUI 模式
        run_gui()
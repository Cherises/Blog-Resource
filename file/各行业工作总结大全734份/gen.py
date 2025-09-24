import os
import subprocess
from tqdm import tqdm  # 需要先安装： pip install tqdm

def call_ollama(model: str, prompt: str) -> str:
    """
    调用本地 ollama 模型，返回生成的结果
    """
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,              # 注意：必须是 str
            capture_output=True,
            text=True,                 # 让 stdout/stderr 以 str 返回
            encoding="utf-8",          # 强制 utf-8 解码
            errors="ignore",           # 忽略坏字符
            check=True
        )
        return result.stdout.strip() if result.stdout else ""
    except subprocess.CalledProcessError as e:
        print(f"❌ 调用 ollama 出错: {e.stderr}")
        return ""

def main():
    model = "qwen2.5:7b"
    output_file = "output.md"

    # 获取当前目录下的所有文件（排除自身和 output.md）
    all_files = [f for f in os.listdir(".") if os.path.isfile(f)]
    script_name = os.path.basename(__file__)
    all_files = [f for f in all_files if f not in [script_name, output_file]]

    results = []

    # tqdm 显示进度条
    for idx, filename in enumerate(tqdm(all_files, desc="处理中", unit="file"), 1):
        prompt = f"""你现在的任务是根据文件名生成严格指定格式的Markdown。
文件名是：{filename}

严格输出以下格式（不要添加任何额外文字）：
##{filename}
[{filename}](https://raw.githubusercontent.com/Cherises/Blog-Resource/main/file/各行业工作总结大全734份/{filename})
"""

        print(f"\n===== 正在处理第 {idx}/{len(all_files)} 个文件: {filename} =====")
        result = call_ollama(model, prompt)

        if result:
            print(result)  # 打印到终端
            results.append(result)

    # 写入到 output.md
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(results))

    print(f"\n✅ 已完成，结果保存到 {output_file}")

if __name__ == "__main__":
    main()

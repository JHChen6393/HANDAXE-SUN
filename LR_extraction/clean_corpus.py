import os
import re

def clean_text_in_parentheses(text):
    """
    使用正则表达式删除文本中所有括号及其内部的内容。
    此版本使用 re.DOTALL 标志来处理跨越多行的括号内容。
    """
    # 正则表达式模式保持不变
    pattern = r'\(.*?\)'
    
    # **关键修改**：在 re.sub() 函数中添加 flags=re.DOTALL
    # 这让 '.' 可以匹配包括换行符在内的任何字符
    cleaned_text = re.sub(pattern, '', text, flags=re.DOTALL)
    
    # 清理可能由删除括号产生的连续多余空格和换行符
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    return cleaned_text

def process_directory(input_dir, output_dir):
    """
    处理一个目录下的所有.txt文件，进行清洗并保存到输出目录。
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建输出目录: {output_dir}")

    if not os.path.exists(input_dir):
        print(f"输入目录不存在: {input_dir}")
        print("仔细检查路径是否完全正确。")
        return

    print(f"\n--- 开始处理目录: {input_dir} ---")
    
    processed_count = 0
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_filepath = os.path.join(input_dir, filename)
            output_filepath = os.path.join(output_dir, filename)
            
            try:
                with open(input_filepath, 'r', encoding='utf-8') as f:
                    original_text = f.read()
                
                cleaned_text = clean_text_in_parentheses(original_text)
                
                with open(output_filepath, 'w', encoding='utf-8') as f:
                    f.write(cleaned_text)
                
                # print(f"  [成功] 清洗文件: {filename}") # 可以取消这行注释来查看每个文件的处理情况
                processed_count += 1

            except Exception as e:
                print(f"  [失败] 处理文件 {filename} 时出错: {e}")
    
    print(f"  共成功处理 {processed_count} 个文件。")
    print(f"--- 目录处理完成: {input_dir} ---")


# --- 主程序 ---
if __name__ == "__main__":
    base_path = 
    input_folder_base = os.path.join(base_path, '清洗前')
    output_folder_base = os.path.join(base_path, '清洗后')
    
    subfolders_to_process = ['22', '25']

    for folder_name in subfolders_to_process:
        input_directory = os.path.join(input_folder_base, folder_name)
        output_directory = os.path.join(output_folder_base, folder_name)
        
        process_directory(input_directory, output_directory)

    print("\n所有任务已完成！")
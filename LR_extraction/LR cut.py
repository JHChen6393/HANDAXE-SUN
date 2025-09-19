import os
import re


start_keywords = [
    'Literature Review',
    'Review of literature',
    'Review of the literature',
    'THEORETICAL BACKGROUND',
    'Theoretical framework',
    'Research Background and Objectives',
    'Background Literature',
    'Background',
    'Related Work',
    'Previous studies',
    'State of the Art',
    'Conceptual Framework',
    'LR',
    'LITERATURE BACKGROUND',               
    'REVIEW OF RELEVANT RESEARCH',      
    'THEORETICAL FOUNDATIONS OF THIS STUDY', 
    'BACKGROUND AND MOTIVATION'           

#开始关键词库 

temporary_keywords = [
    'RESEARCH ON LEARNER FACTORS IN CORPUS-BASED L2 VOCABULARY LEARNING', 
    'L2 LISTENING RESEARCH'                                        
]

# 结束关键词库
end_keywords = [
    'Methodology', 'Method', 'Methods',
    'The present study', 'The study', 'This study',
    'Research questions', 'Research Question',
    'Proposed model',
    'Hypotheses Development', 'Hypotheses',
    'Data and Sample', 'Data', 'Sample',
    'Experiment'
]

def main():
    """主执行函数"""
    print("--- 文献综述提取 ---")

    all_start_keywords = start_keywords + temporary_keywords
    if temporary_keywords:
        print("\n注意：正在使用以下临时关键词: ", temporary_keywords)

    print(f"\n读取源文件于: {source_folder}")
    print(f"保存结果至:   {output_folder}\n")

    # 检查和创建文件夹
    if not os.path.exists(source_folder):
        print(f"错误：源文件夹不存在: {source_folder}")
        return
    if not os.path.exists(output_folder):
        print(f"输出文件夹不存在，正在创建: {output_folder}")
        os.makedirs(output_folder)

    processed_start_keywords = [re.escape(k).replace(r'\ ', r'\s+') for k in all_start_keywords]
    # (?i) 不区分大小写
    # ((\d|I|V|X)+\.?\s*)? 匹配可选的章节号，如 "2. " or "II. "
    start_pattern_str = r'(?i)((\d|I|V|X)+\.?\s*)?(' + '|'.join(processed_start_keywords) + r')'
    start_pattern = re.compile(start_pattern_str)

    end_pattern_str = r'(?im)^\s*((\d|I|V|X)+\.?\s*)?(' + '|'.join(end_keywords) + r')'
    end_pattern = re.compile(end_pattern_str)

    # --- 循环处理文件 ---
    count_success = 0
    count_fail = 0
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(".txt"):
            print(f"处理文件: {filename}")
            try:
                source_path = os.path.join(source_folder, filename)
                with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                extracted_text = ""
                # 从文档开头开始搜索开始标志
                start_match = start_pattern.search(content)

                if start_match:
                    start_index = start_match.start()
                    # 从开始标志之后的位置开始搜索结束标志
                    end_match = end_pattern.search(content, pos=start_index + len(start_match.group(0)))

                    if end_match:
                        end_index = end_match.start()
                        extracted_text = content[start_index:end_index]
                        print("  -> 成功提取 (找到开始和结束)。")
                    else:
                        extracted_text = content[start_index:]
                        print("  -> 只找到开始标志，已提取至文末。")
                    
                    output_path = os.path.join(output_folder, filename)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(extracted_text.strip()) # 使用strip()移除首尾多余空白
                    count_success += 1
                else:
                    print("  -> 未找到开始标志，已跳过。")
                    count_fail += 1
            except Exception as e:
                print(f"  -> 处理时发生严重错误: {e}")
                count_fail += 1
            print("-" * 30)

    # --- 输出最终报告 ---
    print("\n--- 所有文件处理完毕 ---\n")
    print(f"成功处理: {count_success} 个文件")
    print(f"跳过/失败: {count_fail} 个文件")
    print(f"\n提取结果已保存在 '{output_folder}' 文件夹中。")

# --- 程序入口 ---
if __name__ == "__main__":
    main()
    input("\n按回车键退出程序。")
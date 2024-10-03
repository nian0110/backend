import os
import pandas as pd
import argparse
from dotenv import load_dotenv

# 加載 .env 文件
load_dotenv()

def str_to_bool(v):
    if v.lower() in ('true', 't', '1'):
        return True
    elif v.lower() in ('false', 'f', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def get_all_files(directory):
    """ 獲取指定資料夾中所有檔案的完整路徑 """
    all_files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

    # 將檔案名稱寫入 CSV
    df = pd.DataFrame(all_files, columns=['filename'])
    df['full_path'] =  df['filename'].apply(lambda x:os.path.join(directory, x))
    df['full_path'] = df['full_path'].apply(lambda x: x.replace('\\', '/'))

    return df

def merge_notion_df(df, notion_data_path):
    notion_df = pd.read_excel(notion_data_path)
    notion_df = notion_df[['filename', 'username', 'root_path', 'children_path', 'month_path', 'lingorm']]

    df['filename'] = df['filename'].apply(lambda x: os.path.splitext(x)[0])
    df = df.rename(columns={'filename':'base_filename'})
    notion_df['base_filename'] = notion_df['filename'].apply(lambda x: os.path.splitext(x)[0])

    # 合并数据框
    merged_df = pd.merge(df, notion_df, on='base_filename', how='inner')

    # 删除临时列
    merged_df = merged_df.drop(columns=['base_filename'])
    merged_df = merged_df[['filename', 'full_path', 'username', 'root_path', 'children_path', 'month_path', 'lingorm']]
    merged_df['filename'] = merged_df['filename'].apply(lambda x:x.replace('.jpg', '.webp'))
    merged_df = merged_df.rename(columns={'children_path':'activity', 'month_path':'month'})
    
    return merged_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='指定是否合併其他欄位')
    parser.add_argument('merge', type=str_to_bool, help='True/False')
    args = parser.parse_args()
    merge = args.merge
    print(f'merge: {merge}')

    dest_folder = os.getenv('DEST_FOLDER')
    output_file = os.getenv('OUTPUT_FILE')
    notion_data_path = os.getenv('NOTION_DATA_PATH')
    
    # 獲取目的資料夾中的所有檔案
    tmp_df = get_all_files(dest_folder)
    if merge:
        df = merge_notion_df(tmp_df, notion_data_path)
    else:
        df = tmp_df

    df.to_csv(output_file, index=False)
    
    print(f"已將 {tmp_df.shape[0]} 個檔案匯出到 {output_file}")
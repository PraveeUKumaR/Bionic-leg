import glob
import os
import pandas as pd


def res_into_df(folder_path):
    df = pd.DataFrame(columns=['epochs', 'learning_rate', 'gat_dim', 'gat_heads', 'gat_layers',
                               'lambda', 'folder', 'AP'])

    files_names = glob.glob(folder_path + '*.txt')
    for file in files_names:
        epochs = file.split("_")[1][1:]
        learning_rate = file.split("_")[2][2:]
        gat_dim = file.split("_")[3][1:]
        gat_heads = file.split("_")[4][1:]
        gat_layers = file.split("_")[5][1:]
        lambda_ = file.split("_")[6][3:]
        folder = file.split("_")[7][4:].split('.')[0]

        with open(file) as stdio:
            lines = [line.rstrip() for line in stdio]

        df = df.append({'epochs': float(epochs), 'learning_rate': float(learning_rate), 'gat_dim': float(gat_dim),
                        'gat_heads': float(gat_heads), 'gat_layers': float(gat_layers),
                        'lambda': float(lambda_), 'folder': float(folder),
                        'AP': float(lines[0])}, ignore_index=True)

    file_name_csv = folder_path + "joint_results.csv"
    print("file save into ", file_name_csv)
    df.to_csv(file_name_csv)
    return df


def res_into_df_for_headers(folder_path):
    df = pd.DataFrame(columns=['epochs', 'learning_rate', 'gat_dim', 'gat_heads', 'gat_layers',
                               'lambda', 'folder', 'head_type', 'AP'])

    sub_folder_paths = os.listdir(folder_path)
    for sub_folder in sub_folder_paths:
        files_names = glob.glob(folder_path + '/' + sub_folder + '/*.txt')

        for file in files_names:
            epochs = file.split("_")[1][1:]
            learning_rate = file.split("_")[2][2:]
            gat_dim = file.split("_")[3][1:]
            gat_heads = file.split("_")[4][1:]
            gat_layers = file.split("_")[5][1:]
            lambda_ = file.split("_")[6][3:]
            folder = file.split("_")[7][4:].split('.')[0]
            head_type = sub_folder

            with open(file) as stdio:
                lines = [line.rstrip() for line in stdio]

            df = df.append({'epochs': float(epochs), 'learning_rate': float(learning_rate), 'gat_dim': float(gat_dim),
                            'gat_heads': float(gat_heads), 'gat_layers': float(gat_layers),
                            'lambda': float(lambda_), 'folder': float(folder), 'head_type': head_type,
                            'AP': float(lines[0])}, ignore_index=True)

    file_name_csv = folder_path + "joint_results.csv"
    df.to_csv(file_name_csv)
    return df


def group_by_df(df, path):
    if 'head_type' in df.columns:
        df = df.groupby(['head_type']).mean()
        df.rename(columns={'AP': 'mAP'}, inplace=True)
        file_name_csv = path + "joint_group_results.csv"
        print("file save into ", file_name_csv)
        df.to_csv(file_name_csv)
        return df
    else:
        df = df.groupby(['learning_rate']).mean()
        df.rename(columns={'AP': 'mAP'}, inplace=True)
        file_name_csv = path + "joint_group_results.csv"
        print("file save into ", file_name_csv)
        df.to_csv(file_name_csv)
        return df


def show_best_param(df):
    print(df.query('mAP == mAP.max()'))


if __name__ == "__main__":
    df = res_into_df("/home/oleh/bionic/outputs/4/4/")
    df = group_by_df(df, "/home/oleh/bionic/resHead/outputs/4/4/")
    show_best_param(df)

import os
import subprocess
import sys
import pandas as pd
import matplotlib.pyplot as plt

def train_yolov5s(
    data_yaml='path/to/data.yaml',
    weights='yolov5s.pt',
    epochs=100,
    batch_size=16,
    imgsz=640,
    project='runs/train',
    name='yolov5s_experiment',
    device='0'
):
    """
    使用YOLOv5s训练模型的函数，并在训练后生成损失和预测的折线图。

    参数:
    - data_yaml: 数据集配置文件路径
    - weights: 预训练权重文件路径
    - epochs: 训练的轮数
    - batch_size: 批次大小
    - imgsz: 输入图像大小
    - project: 保存训练结果的项目目录
    - name: 训练实验名称
    - device: 设备ID（'0'表示第一个GPU，'cpu'表示使用CPU）
    """
    # 获取YOLOv5的路径
    yolov5_dir = os.path.abspath('yolov5')  # 确保脚本在yolov5目录外运行，或根据实际路径调整

    # 构建训练命令
    cmd = [
        sys.executable,  # 使用当前Python解释器
        os.path.join(yolov5_dir, 'train.py'),
        '--img', str(imgsz),
        '--batch', str(batch_size),
        '--epochs', str(epochs),
        '--data', data_yaml,
        '--weights', weights,
        '--project', project,
        '--name', name,
        '--device', device
    ]

    # 打印命令以供调试
    print('Running command:', ' '.join(cmd))

    # 执行命令
    subprocess.run(cmd, check=True)

    # 训练完成后，生成损失和预测的折线图
    results_csv = os.path.join(project, name, 'results.csv')
    if os.path.exists(results_csv):
        plot_training_results(results_csv, project, name)
    else:
        print(f"未找到 {results_csv}，无法生成图表。")

def plot_training_results(results_csv, project, name):
    """
    解析results.csv并生成损失和预测的折线图。

    参数:
    - results_csv: results.csv文件路径
    - project: 项目目录
    - name: 实验名称
    """
    # 读取results.csv
    df = pd.read_csv(results_csv)

    # 检查所需的列是否存在
    required_columns = ['epoch', 'train/loss', 'val/precision', 'val/recall', 'val/mAP_0.5', 'val/mAP_0.5:0.95']
    for col in required_columns:
        if col not in df.columns:
            print(f"列 '{col}' 未在 {results_csv} 中找到。")
            return

    # 确保保存图表的目录存在
    save_dir = os.path.join(project, name)
    os.makedirs(save_dir, exist_ok=True)

    # 绘制训练损失
    plt.figure(figsize=(10, 6))
    plt.plot(df['epoch'], df['train/loss'], label='训练损失')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('训练损失曲线')
    plt.legend()
    plt.grid(True)
    loss_plot_path = os.path.join(save_dir, 'training_loss.png')
    plt.savefig(loss_plot_path)
    plt.close()
    print(f"训练损失曲线已保存到 {loss_plot_path}")

    # 绘制验证精度和mAP
    plt.figure(figsize=(10, 6))
    plt.plot(df['epoch'], df['val/precision'], label='验证精度 (Precision)')
    plt.plot(df['epoch'], df['val/recall'], label='验证召回率 (Recall)')
    plt.plot(df['epoch'], df['val/mAP_0.5'], label='验证mAP@0.5')
    plt.plot(df['epoch'], df['val/mAP_0.5:0.95'], label='验证mAP@0.5:0.95')
    plt.xlabel('Epoch')
    plt.ylabel('值')
    plt.title('验证指标曲线')
    plt.legend()
    plt.grid(True)
    metrics_plot_path = os.path.join(save_dir, 'validation_metrics.png')
    plt.savefig(metrics_plot_path)
    plt.close()
    print(f"验证指标曲线已保存到 {metrics_plot_path}")

if __name__ == '__main__':
    # 配置参数
    data_yaml = r"C:\yolov5\yaml.yaml"  # 替换为你的data.yaml路径
    weights = 'yolov5s.pt'  # 如果未下载，将自动下载预训练权重
    epochs = 100
    batch_size = 16
    imgsz = 640
    project = r"C:\yolov5\output"
    name = 'yolov5s_experiment'
    device = '0'  # 使用GPU 0，或设置为 'cpu' 使用CPU

    # 检查YOLOv5目录是否存在
    yolov5_dir = os.path.abspath('yolov5')
    if not os.path.isdir(yolov5_dir):
        print(f"未找到YOLOv5目录：{yolov5_dir}")
        print("请确保你已经克隆了YOLOv5仓库并位于正确的目录。")
        sys.exit(1)

    # 开始训练并生成图表
    train_yolov5s(
        data_yaml=data_yaml,
        weights=weights,
        epochs=epochs,
        batch_size=batch_size,
        imgsz=imgsz,
        project=project,
        name=name,
        device=device
    )

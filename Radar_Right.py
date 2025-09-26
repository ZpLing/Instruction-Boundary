import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.transforms import Affine2D
import matplotlib.cm as cm

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def radar_factory(num_vars, frame='circle'):
    """
    创建一个雷达图工厂函数
    """
    # 计算角度
    theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

    # 旋转角度，使第一个轴在顶部
    theta += np.pi / 2

    def unit_poly_verts(theta):
        """返回单位多边形的顶点"""
        x0, y0, r = [0.5] * 3
        verts = [(r * np.cos(t) + x0, r * np.sin(t) + y0) for t in theta]
        return verts

    def unit_circle_verts(theta):
        """返回单位圆的顶点"""
        x0, y0, r = [0.5] * 3
        verts = [(r * np.cos(t) + x0, r * np.sin(t) + y0) for t in theta]
        return verts

    if frame == 'circle':
        verts = unit_circle_verts(theta)
    else:
        verts = unit_poly_verts(theta)

    # 创建路径
    path = Path(verts)

    # 创建变换
    transform = Affine2D().scale(1.0, 1.0).translate(0.0, 0.0)

    return theta, path, transform


# def normalize_data_within_radar(data_list):
#     """
#     对雷达图内的数据进行归一化，保留原始数据信息
#     对于不同指标，使用不同的归一化策略
#     """
#     # 将所有数据合并，找到每个维度的最大值和最小值
#     all_data = np.array(data_list)
#     
#     # 只使用前6个维度的数据进行归一化（GR3被注释掉）
#     data_for_norm = all_data[:, :6]
#     
#     # 计算每个维度的范围
#     min_vals = np.min(data_for_norm, axis=0)
#     max_vals = np.max(data_for_norm, axis=0)
#     
#     # 避免除零错误
#     ranges = max_vals - min_vals
#     ranges[ranges == 0] = 1  # 如果范围为0，设为1
#     
#     # 归一化数据
#     normalized_data = []
#     for data in data_list:
#         # 只归一化前6个维度
#         data_6d = np.array(data[:6])
#         normalized_6d = (data_6d - min_vals) / ranges
#         # 保留第7个维度的原始数据（GR3）
#         if len(data) > 6:
#             normalized_6d = np.append(normalized_6d, data[6])
#         normalized_data.append(normalized_6d)
#     
#     return normalized_data, min_vals, max_vals

def get_data_ranges(data_list):
    """
    获取数据的范围信息，用于显示刻度标签
    使用统一的0-100刻度
    """
    # 使用统一的0-100刻度
    num_dimensions = 6  # 只使用前6个维度
    min_vals = np.zeros(num_dimensions)  # 所有维度最小值都是0
    max_vals = np.full(num_dimensions, 100)  # 所有维度最大值都是100
    
    return min_vals, max_vals

def radar_plot(ax, data_list, labels, title, colors, alpha=0.3):
    """
    在给定的轴上绘制雷达图，支持多个数据集对比，直接使用原始数据
    """
    # 创建雷达图
    theta, path, transform = radar_factory(len(labels), frame='circle')

    # 获取数据范围信息（不使用归一化）
    min_vals, max_vals = get_data_ranges(data_list)

    # 绘制雷达图背景（调整范围以适应放大后的数据）
    scale_factor = 1.2  # 刻度放大系数，可以调整这个值来放大数据
    ax.set_xlim(-1.1*scale_factor, 1.1*scale_factor)
    ax.set_ylim(-1.1*scale_factor, 1.1*scale_factor)
    ax.set_aspect('equal')

    # 绘制同心圆和刻度标签（使用放大系数）
    for i, r in enumerate([0.2, 0.4, 0.6, 0.8, 1.0]):
        # 应用放大系数
        scaled_r = r * scale_factor
        circle = Circle((0, 0), scaled_r, fill=False, color='gray', alpha=0.3, linewidth=0.5)
        ax.add_patch(circle)
        
        # 不显示刻度标签，只保留径向线延伸

    # 绘制径向线（延伸到最外层圆圈）
    for i, (t, label) in enumerate(zip(theta, labels)):
        x = np.cos(t) * scale_factor  # 延伸到最外层圆圈
        y = np.sin(t) * scale_factor  # 延伸到最外层圆圈
        ax.plot([0, x], [0, y], 'gray', alpha=0.3, linewidth=0.5)

        # 添加标签 - 更紧靠雷达图（调整位置以适应放大）
        label_x = 0.9 * x * scale_factor
        label_y = 0.9 * y * scale_factor
        ax.text(label_x, label_y, label, ha='center', va='center', fontsize=8)

    # 绘制多个数据集（直接使用原始数据）
    for data, color in zip(data_list, colors):
        if np.any(data):  # 只有当数据不为全零时才绘制
            # 只使用前6个维度的数据进行绘制，应用放大系数
            data_for_plot = np.array(data[:6]) / 100.0 * scale_factor  # 将百分比转换为0-1范围，然后应用放大系数
            x_coords = data_for_plot * np.cos(theta)
            y_coords = data_for_plot * np.sin(theta)

            # 闭合多边形
            x_coords = np.append(x_coords, x_coords[0])
            y_coords = np.append(y_coords, y_coords[0])

            # 填充区域
            ax.fill(x_coords, y_coords, alpha=alpha, color=color)

            # 绘制边界线
            ax.plot(x_coords, y_coords, color=color, linewidth=1)

            # 绘制数据点
            ax.scatter(x_coords[:-1], y_coords[:-1], color=color, s=1, zorder=5)

    # 设置标题
    ax.set_title(title, fontsize=10, pad=10)

    # 移除坐标轴
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)


def save_original_data(radar_data, filename='radar_original_data.json'):
    """
    保存原始雷达图数据到JSON文件
    """
    import json
    
    # 创建保存数据的结构
    save_data = {
        'model_names': model_names,
        'labels': labels,
        'settings': settings,
        'radar_data': radar_data,
        'description': '原始雷达图数据，包含所有实验的完整数据'
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, indent=2, ensure_ascii=False)
    
    print(f"原始数据已保存到: {filename}")

# 定义莫兰迪色系的五种颜色（五个模型）
model_colors = ['#8B9DC3', '#A8C8A8', '#D4A5A5', '#C4A484', '#B8A9C9']  # 莫兰迪色系
model_names = ['GPT-3.5-turbo', 'GPT-4o', 'Llama-3.1-8b-Instruct', 'Claude-3.7-sonnet', 'Gemini-2.0-Flash']

# 创建数据（六个雷达图使用不同的数据）
labels = ['Acc$_b^1$', 'Acc$_b^2$', 'GR$^1$', 'GR$^2$', 'SR$^1$', 'SR$^2$']  # GR$^3$ 注释掉，保留数据但不显示

# 为每个雷达图定义不同的数据
# 第一张图：GPT-3.5-turbo和GPT-4o的数据对比
# 其他图：保持空白
radar_data = [
    {
        'data_list': [
            [34.76, 25.56, 8.48, 12.67, 61.04, 64.0, 0],  # GPT-3.5-turbo: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [40.39, 40.89, 47.69, 32.67, 38.09, 90.0, 0],  # GPT-4o: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [47.91, 22.44, 86.67, 5.33, 8.67, 59.33, 2.67],  # Llama-3.1-8b: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [53.19, 9.78, 80.07, 11.33, 26.32, 14.67, 3.33],  # Claude-3.7: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [45.79, 36.0, 60.28, 21.21, 31.3, 87.88, 0]  # Gemini-2.0: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
        ],
        'colors': [model_colors[0], model_colors[1], model_colors[2], model_colors[3], model_colors[4]]  # 使用所有五个模型颜色
    },
    {
        'data_list': [
            [50, 29.11, 0.625, 22.0, 99.375, 65.33, 0],  # GPT-3.5-turbo: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [56.12, 44.0, 31.495, 34.0, 80.73, 98.0, 0],  # GPT-4o: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [46.28, 38.0, 15.15, 63.33, 77.4, 50.67, 0.67],  # Llama-3.1-8b: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [54.095, 25.11, 54.105, 21.33, 54.085, 52.67, 1.33],  # Claude-3.7: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [54.505, 42.67, 18.305, 40.67, 88.225, 87.33, 0]  # Gemini-2.0: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
        ],
        'colors': [model_colors[0], model_colors[1], model_colors[2], model_colors[3], model_colors[4]]
        # 第二张图：Few-shot "Mislearning"
    },
    {
        'data_list': [
            [38.32, 24.7, 50.375, 0.7, 23.165, 73.3, 0],  # GPT-3.5-turbo: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [41.005, 32.7, 69.75, 4.7, 12.275, 93.3, 0],  # GPT-4o: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [29.21, 25.6, 58.11, 0.7, 0.315, 75.3, 0.7],  # Llama-3.1-8b: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [51.2, 30.2, 57.065, 2.0, 45.34, 88.7, 0],  # Claude-3.7: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [40.725, 31.6, 61.96, 4.0, 19.49, 90.7, 0]  # Gemini-2.0: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
        ],
        'colors': [model_colors[0], model_colors[1], model_colors[2], model_colors[3], model_colors[4]]
        # 第三张图：Vagueness
    },
    {
        'data_list': [
            [34.295, 21.33, 59.44, 5.33, 9.155, 58.67, 0],  # GPT-3.5-turbo: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [48.855, 37.11, 37.21, 19.33, 60.5, 89.33, 2.67],  # GPT-4o: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [42.58, 7.78, 34.875, 5.33, 50.28, 13.33, 4.67],  # Llama-3.1-8b: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [57.21, 2.67, 27.655, 5.33, 84.06, 1.33, 1.33],  # Claude-3.7: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [35.4, 10.44, 70.305, 7.33, 0.5, 18.67, 5.33]  # Gemini-2.0: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
        ],
        'colors': [model_colors[0], model_colors[1], model_colors[2], model_colors[3], model_colors[4]]
        # 第四张图：Prompt-polishing
    },
    {
        'data_list': [
            [36.14, 33.56, 40.775, 60.0, 31.51, 40.67, 0],  # GPT-3.5-turbo: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [40.07, 18.89, 50.615, 40.0, 29.525, 16.67, 0],  # GPT-4o: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [38.81, 15.33, 19.93, 8.67, 57.695, 36.0, 1.33],  # Llama-3.1-8b: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [45.73, 14.0, 35.98, 24.67, 55.48, 16.67, 0.67],  # Claude-3.7: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [40.835, 36.0, 41.865, 45.33, 39.81, 60.67, 2.0]  # Gemini-2.0: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
        ],
        'colors': [model_colors[0], model_colors[1], model_colors[2], model_colors[3], model_colors[4]]
        # 第五张图：Multi-turn
    },
    {
        'data_list': [
            [50, 37.11, 100, 100.0, 0, 11.33, 0],  # GPT-3.5-turbo: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [56.915, 44.0, 93.24, 48.67, 20.595, 83.33, 0],  # GPT-4o: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [50, 38.0, 100, 60.0, 0, 50.67, 3.33],  # Llama-3.1-8b: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [55.095, 3.78, 91.49, 7.33, 18.695, 1.33, 2.67],  # Claude-3.7: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
            [51.195, 50.0, 97.695, 84.67, 4.68, 65.33, 0]  # Gemini-2.0: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3
        ],
        'colors': [model_colors[0], model_colors[1], model_colors[2], model_colors[3], model_colors[4]]
        # 第六张图：Conformity
    },
    {
        'data_list': [
            [48.745, 24.67, 76.025, 12.0, 21.465, 62.0, 0.0],  # GPT-3.5-turbo: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3 (Vanilla)
            [45.405, 39.33, 27.32, 28.67, 63.49, 89.33, 0.0],  # GPT-4o: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3 (Vanilla)
            [51.865, 20.67, 85.815, 4.67, 17.915, 55.33, 2.0],  # Llama-3.1-8b: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3 (Vanilla)
            [46.225, 7.78, 52.325, 7.33, 40.125, 12.67, 3.33],  # Claude-3.7: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3 (Vanilla)
            [51.805, 35.0, 66.62, 18.18, 36.99, 84.85, 2.94]  # Gemini-2.0: Acc1, Acc2, GR1, GR2, SR1, SR2, GR3 (Vanilla)
        ],
        'colors': [model_colors[0], model_colors[1], model_colors[2], model_colors[3], model_colors[4]]
        # 第七张图：Vanilla (所有五个模型，包含sufficient setting数据)
    }
]

# 创建图形，设置ICLR单栏论文宽度，增加高度让子图更大
fig, axes = plt.subplots(3, 3, figsize=(8, 10))

# 手动调整边距
plt.subplots_adjust(left=0.01, right=0.99, wspace=0.2, hspace=0.25)

# 雷达图背景颜色（保持原有的六种颜色，添加第七种）
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

# 定义七个设置的小标题
settings = ['Missing Choices', 'Few-shot "Mislearning"', 'Vagueness', 'Prompt-polishing', 'Multi-turn', 'Conformity', 'Vanilla']

# 绘制七个雷达图
for i in range(3):
    for j in range(3):
        idx = i * 3 + j
        if idx >= 7:  # 只绘制7张图，隐藏第8和第9个位置
            axes[i, j].set_visible(False)
            continue
        color = colors[idx % len(colors)]

        # 设置每个雷达图的标题
        title = settings[idx]

        # 使用对应雷达图的数据
        radar_info = radar_data[idx]

        radar_plot(axes[i, j], radar_info['data_list'], labels, title, radar_info['colors'], alpha=0.3)

        # 在每个雷达图下方添加序号标签
        axes[i, j].text(0.5, -0.08, f'({idx + 1})',
                        ha='center', va='center',
                        transform=axes[i, j].transAxes,
                        fontsize=10, fontweight='bold')

# 添加图例
# 创建图例元素
legend_elements = []
for i, (model, color) in enumerate(zip(model_names, model_colors)):
    legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color,
                                      markersize=8, label=model, linewidth=0))


# 使用gridspec_kw已经设置了间距，不需要tight_layout
# plt.tight_layout(pad=0.01, h_pad=0.001, w_pad=0.01)
# 1) 组装图例元素（与原版一致）
legend_elements = []
for model, color in zip(model_names, model_colors):
    legend_elements.append(
        plt.Line2D([0], [0], marker='o', color='w',
                   markerfacecolor=color, markersize=8,
                   label=model, linewidth=0)
    )

# 2) 调整画布底部边距，给图例留空间（数值可微调）
plt.subplots_adjust(bottom=0.16)         # 如果你已经有 subplots_adjust，就把 bottom ≥ 0.16

# 3) 放置图例在底部居中；bbox_to_anchor 的 y 值略为负可贴近边缘但不被裁
fig.legend(handles=legend_elements,
           loc='lower center',
           ncol=5,
           bbox_to_anchor=(0.5, 0.08),   # 调整y值从0.02到0.08，让legend离雷达图更近
           fontsize=10,
           frameon=True)

# 保存原始数据
save_original_data(radar_data, 'radar_original_data.json')

# 4) 保存（保留 tight），如发现仍被裁，可把 bbox_to_anchor 的 y 调大一点
plt.savefig('six_radar_charts.pdf', dpi=300, bbox_inches='tight')

plt.show()
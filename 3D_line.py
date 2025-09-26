import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.cm as cm


# 创建x轴数据点（现在只有3个数据点）
x_points = np.array([1, 2, 3])


# 直接使用指定的数据值
def create_model_data(values):
    return np.array(values)


# 为5个模型创建数据，使用指定的数值（重新排序：Unknown, True, False）
group_bases = {
    'gpt-3.5-turbo': [47.81, 48.90, 3.3],  # Unknown, True, False
    'gpt-4o': [22.19, 77.18, 0.06],
    'llama-3.1-8b-instruct': [69.22, 30.78, 0],
    'claude-3.7-sonnet': [18.75, 72.03, 9.22],
    'gemini-2.0-flash': [52.34, 36.41, 11.25]
}

# 创建数据框
data = {'Count': x_points}

# 为每个模型生成数据
for model, values in group_bases.items():
    data[model] = create_model_data(values)

data = pd.DataFrame(data)
drawing_order = ['gpt-3.5-turbo', 'gpt-4o', 'llama-3.1-8b-instruct', 'claude-3.7-sonnet', 'gemini-2.0-flash']

# 使用viridis色彩方案，避免黄色
viridis_colors = cm.viridis(np.linspace(0, 1, len(drawing_order)))
colors = {drawing_order[i]: tuple(viridis_colors[i]) for i in range(len(drawing_order))}

# 为gemini-2.0-flash指定一个非黄色的颜色（深红色）
colors['gemini-2.0-flash'] = (0.8, 0.2, 0.2)

x_values = data['Count'].values

# 创建包含四个子图的图形
fig = plt.figure(figsize=(10, 5))

# 使用gridspec来精确控制布局
from matplotlib.gridspec import GridSpec
gs = GridSpec(1, 4, figure=fig, width_ratios=[1, 1, 1, 1], hspace=0.0, wspace=0.0)

# 左边的3D图 - 冗余实验准确率
ax1 = fig.add_subplot(gs[0, 0], projection='3d')

# 冗余实验数据 - 所有模型
redundancy_data = {
    'gpt-4o': [0.9867, 0.97, 0.9633, 0.97, 0.97, 0.9733, 0.96, 0.96, 0.9667],
    'gpt-3.5-turbo': [0.84, 0.8433, 0.7733, 0.7567, 0.7433, 0.7633, 0.7367, 0.73, 0.7133],
    'llama-3.1-8b-instruct': [0.9667, 0.9533, 0.9633, 0.95, 0.9567, 0.9533, 0.95, 0.94, 0.9533],
    'claude-3.7-sonnet': [1.0, 0.9967, 0.9967, 1.0, 0.9833, 0.99, 0.9933, 0.9867, 0.9833],
    'gemini-2.0-flash': [1.0, 0.9867, 0.9867, 0.9833, 0.9933, 0.9833, 0.9833, 0.9867, 0.9733]
}

# 绘制冗余实验的3D瀑布图
x_redundancy = np.array(list(range(1, 10)))  # 1-9个错误选项
redundancy_models = ['gpt-3.5-turbo', 'gpt-4o', 'llama-3.1-8b-instruct', 'claude-3.7-sonnet', 'gemini-2.0-flash']

for i, model in enumerate(redundancy_models):
    color = colors.get(model, 'blue')
    accuracies = np.array(redundancy_data[model])
    y_points = np.full_like(x_redundancy, i)
    
    # 转换为百分比
    z_values = accuracies * 100
    
    ax1.plot(x_redundancy, y_points, z_values, color=color, alpha=1, linewidth=1.5)
    ax1.scatter(x_redundancy, y_points, z_values, color=color, marker='o', s=10)
    
    # 只标注每个模型最左边和最右边的数值
    for x, y, z in zip(x_redundancy, y_points, z_values):
        if x == 1 or x == 9:  # 只标注最左边(x=1)和最右边(x=9)的数据点
            label = f'{z:.1f}'
            ax1.text(x, y, z + 2, label, ha='center', va='bottom', fontsize=8)
    
    # 去掉3D填充区域阴影
    # verts = [list(zip(x_redundancy, y_points, z_values)),
    #          list(zip(x_redundancy, y_points, np.full_like(z_values, 0)))]  # 从0开始覆盖满整个区域
    # poly = Poly3DCollection([verts[0] + verts[1][::-1]], alpha=0.15)
    # poly.set_color(color)
    # ax1.add_collection3d(poly)
    ax1.scatter([], [], [], color=color, marker='o', label=model)

z_ticks = [0, 20, 40, 60, 80, 100]
ax1.set_zticks(z_ticks)
ax1.set_zlim(0, 100)
ax1.set_zticklabels([f'{tick}%' for tick in z_ticks])
ax1.tick_params(axis='z', labelsize=8)  # 设置z轴刻度字体大小
ax1.set_box_aspect([1.5, 1.5, 1])  # 与右边保持一致
ax1.set_xlabel('')
ax1.set_xticks(x_redundancy)
ax1.set_yticks([0, 1, 2, 3, 4])
ax1.set_yticklabels([])  # 隐藏y轴标签
ax1.set_zlim(0, 100)
ax1.tick_params(axis='x', pad=0)  # 减少x轴标签与图的距离
# 去掉图例
ax1.view_init(elev=30, azim=-55)

# 中间的3D图 - 准确率数据（Acc₁和Acc₂）
ax2 = fig.add_subplot(gs[0, 1], projection='3d')
ax2.set_box_aspect([1.5, 1.5, 1])

# 准确率数据 - 从雷达图数据中提取，计算Acc₁和Acc₂的平均值
accuracy_data = {
    'gpt-3.5-turbo': [(34.76+25.56)/2, (50.0+29.11)/2, (38.32+24.7)/2, (34.295+21.33)/2, (36.14+33.56)/2, (50.0+37.11)/2],
    'gpt-4o': [(40.39+40.89)/2, (56.12+44.0)/2, (41.005+32.7)/2, (48.855+37.11)/2, (40.07+18.89)/2, (56.915+44.0)/2],
    'llama-3.1-8b-instruct': [(47.91+22.44)/2, (46.28+38.0)/2, (29.21+25.6)/2, (42.58+7.78)/2, (38.81+15.33)/2, (50.0+38.0)/2],
    'claude-3.7-sonnet': [(53.19+9.78)/2, (54.095+25.11)/2, (51.2+30.2)/2, (57.21+2.67)/2, (45.73+14.0)/2, (55.095+3.78)/2],
    'gemini-2.0-flash': [(45.79+36.0)/2, (54.505+42.67)/2, (40.725+31.6)/2, (35.4+10.44)/2, (40.835+36.0)/2, (51.195+50.0)/2]
}

# 设置x轴标签（6个settings）- 使用具体名称
settings_labels = ['Missing Choices', 'Few-shot\n"Mislearning"', 'Vagueness', 'Prompt-\npolishing', 'Reflection', 'Conformity']
x_acc = np.array([1, 2, 3, 4, 5, 6])

# 绘制准确率数据的3D瀑布图（每个模型一条线）
for i, model in enumerate(drawing_order):
    color = colors.get(model, 'blue')
    avg_values = np.array(accuracy_data[model])  # 使用平均值数据
    y_points = np.full_like(x_acc, i)
    
    # 绘制平均准确率折线图
    ax2.plot(x_acc, y_points, avg_values, color=color, alpha=1, linewidth=2, linestyle='-')
    ax2.scatter(x_acc, y_points, avg_values, color=color, marker='o', s=15)
    
    # 去掉3D填充区域阴影
    # verts = [list(zip(x_acc, y_points, avg_values)),
    #          list(zip(x_acc, y_points, np.full_like(avg_values, 0)))]
    # poly = Poly3DCollection([verts[0] + verts[1][::-1]], alpha=0.1)
    # poly.set_color(color)
    # ax2.add_collection3d(poly)

# 设置中间图的标签和刻度
ax2.set_xticks(x_acc)
ax2.set_xticklabels(settings_labels, fontsize=7, rotation=45, ha='right')
ax2.set_yticks([0, 1, 2, 3, 4])
ax2.set_yticklabels([])  # 隐藏y轴标签
ax2.set_zlabel('Avg Accuracy (%)')
ax2.set_xlabel('')
ax2.set_zlim(0, 100)
ax2.set_ylim(-0.5, 4.5)
# 设置与其他图统一的z轴刻度
z_ticks = [0, 20, 40, 60, 80, 100]
ax2.set_zticks(z_ticks)
ax2.set_zticklabels([f'{tick}%' for tick in z_ticks])
ax2.tick_params(axis='z', labelsize=8)  # 设置z轴刻度字体大小
ax2.tick_params(axis='x', pad=0)
ax2.view_init(elev=30, azim=-55)

# 右边的3D图
ax3 = fig.add_subplot(gs[0, 2], projection='3d')
ax3.set_box_aspect([1.5, 1.5, 1])
# 设置x轴刻度标签
ax3.set_xticks([1, 2, 3])
ax3.set_xticklabels(['Unknown', 'True', 'False'], rotation=45, ha='right')

for i, y_label in enumerate(reversed(drawing_order)):
    color = colors[y_label]
    z_values = data[y_label].values
    x_valid = x_values
    z_valid = z_values
    y_val = drawing_order.index(y_label)
    y_points = np.full_like(x_valid, y_val)

    ax3.plot(x_valid, y_points, z_valid, color=color, alpha=1, linewidth=1.5)
    ax3.scatter(x_valid, y_points, z_valid, color=color, marker='o', s=20)

    # 隐藏所有数字标注
    # for x, y, z in zip(x_valid, y_points, z_valid):
    #     if x == 2 or x == 3:  # 只标注True列（x=2）和False列（x=3），隐藏Unknown列（x=1）
    #         label = f'{z:.1f}' if isinstance(z, float) else str(z)
    #         ax3.text(x, y, z + 1, label, ha='center', va='bottom', fontsize=10)

    # 去掉3D填充区域阴影
    # verts = [list(zip(x_valid, y_points, z_valid)),
    #          list(zip(x_valid, y_points, np.zeros_like(z_valid)))]
    # poly = Poly3DCollection([verts[0] + verts[1][::-1]], alpha=0.15)
    # poly.set_color(color)
    # ax3.add_collection3d(poly)
    ax3.scatter([], [], [], color=color, marker='o', label=y_label)

ax3.view_init(elev=30, azim=-55)
ax3.set_xlabel('')
ax3.set_zlabel('Accuracy (%)')
y_ticks = np.arange(len(drawing_order))
ax3.set_yticks(y_ticks)
ax3.set_yticklabels([])  # 隐藏y轴标签，只保留图例

# 设置z轴刻度为5个梯度等级
z_ticks = [0, 20, 40, 60, 80, 100]
ax3.set_zticks(z_ticks)
ax3.set_zticklabels([f'{tick}%' for tick in z_ticks])
ax3.tick_params(axis='z', labelsize=8)  # 设置z轴刻度字体大小

ax3.set_xlim(0.5, 3.5)
ax3.set_zlim(0, 100)
ax3.tick_params(axis='x', pad=0)  # 减少x轴标签与图的距离

# 第四张3D图 - Sufficient Setting输出比例
ax4 = fig.add_subplot(gs[0, 3], projection='3d')
ax4.set_box_aspect([1.5, 1.5, 1])

# Sufficient setting输出比例数据（修正版：no_answer和unclear归类为All Wrong）
sufficient_output_data = {
    'gpt-3.5-turbo': [49.1, 19.6, 31.3],      # 单选, 多选, All wrong (no_answer+unclear)
    'gpt-4o': [66.0, 19.8, 14.2],
    'llama-3.1-8b-instruct': [52.0, 39.6, 8.4],
    'claude-3.7-sonnet': [24.7, 41.8, 33.6],
    'gemini-2.0-flash': [61.0, 28.0, 11.0]
}

# 设置x轴标签
output_labels = ['Single\nChoice', 'Multiple\nChoices', 'All Wrong']
x_output = np.array([1, 2, 3])

# 绘制sufficient setting输出比例的3D瀑布图
for i, model in enumerate(drawing_order):
    color = colors.get(model, 'blue')
    output_values = np.array(sufficient_output_data[model])
    y_points = np.full_like(x_output, i)
    
    # 绘制输出比例折线图
    ax4.plot(x_output, y_points, output_values, color=color, alpha=1, linewidth=2, linestyle='-')
    ax4.scatter(x_output, y_points, output_values, color=color, marker='o', s=15)
    
    # 去掉3D填充区域阴影
    # verts = [list(zip(x_output, y_points, output_values)),
    #          list(zip(x_output, y_points, np.full_like(output_values, 0)))]
    # poly = Poly3DCollection([verts[0] + verts[1][::-1]], alpha=0.1)
    # poly.set_color(color)
    # ax4.add_collection3d(poly)

# 设置第四张图的标签和刻度
ax4.set_xticks(x_output)
ax4.set_xticklabels(output_labels, rotation=45, ha='right')
ax4.set_yticks([0, 1, 2, 3, 4])
ax4.set_yticklabels([])  # 隐藏y轴标签
ax4.set_zlabel('Output Ratio (%)')
ax4.set_xlabel('')
ax4.set_zlim(0, 100)
ax4.set_ylim(-0.5, 4.5)
# 设置与其他图统一的z轴刻度
z_ticks = [0, 20, 40, 60, 80, 100]
ax4.set_zticks(z_ticks)
ax4.set_zticklabels([f'{tick}%' for tick in z_ticks])
ax4.tick_params(axis='z', labelsize=8)  # 设置z轴刻度字体大小
ax4.tick_params(axis='x', pad=0)
ax4.view_init(elev=30, azim=-55)

# 在中间图的顶部添加图例
legend_elements = []
for model in drawing_order:
    color = colors.get(model, 'blue')
    legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=8, label=model))

# 使用fig来放置图例，避免被3D图覆盖
legend = fig.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 0.7), ncol=5, fontsize=10, frameon=True, fancybox=True, shadow=True, columnspacing=1.0, handletextpad=0.3)
legend.set_zorder(1000)  # 设置图例置于顶层

# 确保图例不被任何元素覆盖
legend.set_in_layout(False)  # 不参与自动布局
legend.set_visible(True)     # 确保图例可见
legend.set_alpha(1.0)        # 设置完全不透明

# 调整图形边距，为图例留出空间
plt.subplots_adjust(top=0.85)

plt.savefig("rainbow_plot.pdf", dpi=300, bbox_inches='tight', pad_inches=.01)
plt.show()
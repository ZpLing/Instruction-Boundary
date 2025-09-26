#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - 主运行器
统一的实验运行入口
"""

import asyncio
import argparse
import sys
import os
from typing import List, Dict, Any

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.model_config import get_model_config, get_experiment_config, SUPPORTED_MODELS
from config.experiment_config import get_output_folder, get_execution_order, create_output_directories
from core.data_loader import ChoiceDataLoader
from experiments.exp_1_1_2_1 import Experiment1_1_2_1
from experiments.exp_1_2 import Experiment1_2
from experiments.exp_2_3 import Experiment2_3
from experiments.exp_2_5 import Experiment2_5
from experiments.exp_2_6 import Experiment2_6
from experiments.exp_2_8 import Experiment2_8

class ChoiceToolkit:
    """Choice实验工具包主类"""
    
    def __init__(self, model_name: str = None):
        self.model_config = get_model_config(model_name)
        self.data_loader = ChoiceDataLoader(self.model_config)
        self.experiments = {}
        self._initialize_experiments()
    
    def _initialize_experiments(self):
        """初始化实验模块"""
        # 注册所有实验
        self.experiments = {
            "1.1_2.1": Experiment1_1_2_1(self.model_config),
            "1.2": Experiment1_2(self.model_config),
            "2.3": Experiment2_3(self.model_config),
            "2.5": Experiment2_5(self.model_config),
            "2.6": Experiment2_6(self.model_config),
            "2.8": Experiment2_8(self.model_config),
        }
    
    async def run_single_experiment(self, experiment_id: str, dataset: List[Dict], 
                                 dataset_name: str) -> Dict[str, Any]:
        """运行单个实验"""
        if experiment_id not in self.experiments:
            raise ValueError(f"不支持的实验ID: {experiment_id}")
        
        experiment = self.experiments[experiment_id]
        output_folder = f"results/{get_output_folder(experiment_id)}"
        
        print(f"\n{'='*50}")
        print(f"开始处理数据集: {dataset_name}")
        print(f"实验类型: {get_experiment_config(experiment_id)['name']}")
        print(f"{'='*50}")
        
        # 运行实验
        result = await experiment.run_experiment(
            dataset, self.model_config['test_model'], dataset_name, output_folder
        )
        
        print(f"\n🎉 {dataset_name} {experiment_id}实验完成!")
        return result
    
    async def run_experiments(self, experiment_ids: List[str]) -> Dict[str, Any]:
        """运行多个实验"""
        print("🚀 开始运行Choice实验工具包")
        print("=" * 80)
        
        # 创建输出目录
        create_output_directories("results")
        
        # 获取数据集
        dataset_files = self.data_loader.get_all_dataset_files()
        if not dataset_files:
            print("❌ 未找到数据集文件")
            return {}
        
        all_results = {}
        
        # 为每个数据集运行实验
        for dataset_file in dataset_files:
            print(f"\n{'='*70}")
            print(f"📁 处理数据集: {dataset_file}")
            print(f"{'='*70}")
            
            try:
                # 加载数据集
                dataset, question_types, dataset_name = self.data_loader.load_and_prepare_dataset(
                    dataset_file, self.data_loader.load_dataset_config()
                )
                
                if not dataset:
                    continue
                
                # 使用全部样本进行实验
                print(f"   使用全部{len(dataset)}个样本进行实验")
                
                dataset_results = {}
                
                # 运行指定的实验
                for experiment_id in experiment_ids:
                    if experiment_id in self.experiments:
                        try:
                            result = await self.run_single_experiment(
                                experiment_id, dataset, dataset_name
                            )
                            dataset_results[experiment_id] = result
                        except Exception as e:
                            print(f"❌ 运行实验 {experiment_id} 时出错: {e}")
                            continue
                    else:
                        print(f"⚠️  实验 {experiment_id} 暂未实现")
                
                all_results[dataset_file] = dataset_results
                
            except Exception as e:
                print(f"❌ 处理数据集 {dataset_file} 时出错: {e}")
                continue
        
        # 生成综合报告
        print(f"\n{'='*80}")
        print("📊 综合实验结果报告")
        print(f"{'='*80}")
        
        for dataset_file, dataset_results in all_results.items():
            print(f"\n📁 数据集: {dataset_file}")
            for experiment_id, result in dataset_results.items():
                print(f"   ✅ 实验 {experiment_id} 完成")
        
        print(f"\n🎊 所有Choice实验完成!")
        return all_results

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="Choice实验工具包")
    
    parser.add_argument(
        "--model", 
        type=str, 
        choices=SUPPORTED_MODELS,
        default="gpt-4o",
        help="指定测试模型"
    )
    
    parser.add_argument(
        "--experiment",
        type=str,
        help="指定要运行的实验ID，用逗号分隔多个实验"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="运行所有实验"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出所有可用的实验"
    )
    
    return parser.parse_args()

def list_experiments():
    """列出所有可用的实验"""
    print("可用的实验:")
    print("-" * 50)
    
    experiments = {
        "1.1_2.1": "充分vs不充分提示对比",
        "1.2": "少样本学习",
        "2.3": "模糊提示",
        "2.5": "LLM优化提示",
        "2.6": "多轮对话反思",
        "2.8": "从众效应"
    }
    
    for exp_id, description in experiments.items():
        status = "✅ 已实现"
        print(f"  {exp_id:>8}: {description:<20} {status}")

async def main():
    """主函数"""
    args = parse_arguments()
    
    if args.list:
        list_experiments()
        return
    
    # 确定要运行的实验
    if args.all:
        experiment_ids = get_execution_order()
    elif args.experiment:
        experiment_ids = [exp.strip() for exp in args.experiment.split(',')]
    else:
        print("请指定要运行的实验 (--experiment) 或运行所有实验 (--all)")
        return
    
    # 创建工具包实例
    toolkit = ChoiceToolkit(args.model)
    
    # 运行实验
    try:
        results = await toolkit.run_experiments(experiment_ids)
        print(f"\n✅ 实验完成! 结果保存在 results/ 目录中")
    except Exception as e:
        print(f"❌ 运行实验时出错: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

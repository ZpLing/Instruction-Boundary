#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - 快速启动脚本
提供简化的启动方式
"""

import asyncio
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def print_banner():
    """打印欢迎横幅"""
    print("=" * 80)
    print("🎯 Choice实验End-to-End Toolkit")
    print("   统一的Choice实验工具包")
    print("   支持6种实验类型，清晰的文件保存路径")
    print("=" * 80)

def print_menu():
    """打印菜单"""
    print("\n请选择操作:")
    print("1. 运行所有实验")
    print("2. 运行单个实验")
    print("3. 运行多个实验")
    print("4. 列出所有实验")
    print("5. 测试工具包")
    print("6. 查看使用示例")
    print("0. 退出")

def get_experiment_choice():
    """获取实验选择"""
    experiments = {
        "1": "1.1_2.1",
        "2": "1.2", 
        "3": "2.3",
        "4": "2.5",
        "5": "2.6",
        "6": "2.8"
    }
    
    print("\n可用实验:")
    for key, exp_id in experiments.items():
        descriptions = {
            "1.1_2.1": "充分vs不充分提示对比",
            "1.2": "少样本学习",
            "2.3": "模糊提示", 
            "2.5": "LLM优化提示",
            "2.6": "多轮对话反思",
            "2.8": "从众效应"
        }
        print(f"  {key}. {exp_id}: {descriptions[exp_id]}")
    
    return experiments

async def run_all_experiments():
    """运行所有实验"""
    print("\n🚀 运行所有实验...")
    from main import ChoiceToolkit
    
    toolkit = ChoiceToolkit("gpt-4o")
    results = await toolkit.run_experiments(["1.1_2.1", "1.2", "2.3", "2.5", "2.6", "2.8"])
    print("✅ 所有实验完成!")

async def run_single_experiment(exp_id):
    """运行单个实验"""
    print(f"\n🚀 运行实验 {exp_id}...")
    from main import ChoiceToolkit
    
    toolkit = ChoiceToolkit("gpt-4o")
    results = await toolkit.run_experiments([exp_id])
    print(f"✅ 实验 {exp_id} 完成!")

async def run_multiple_experiments(exp_ids):
    """运行多个实验"""
    print(f"\n🚀 运行实验 {', '.join(exp_ids)}...")
    from main import ChoiceToolkit
    
    toolkit = ChoiceToolkit("gpt-4o")
    results = await toolkit.run_experiments(exp_ids)
    print(f"✅ 实验 {', '.join(exp_ids)} 完成!")

def list_experiments():
    """列出所有实验"""
    from main import list_experiments
    list_experiments()

async def test_toolkit():
    """测试工具包"""
    print("\n🧪 测试工具包...")
    from test_toolkit import main as test_main
    await test_main()

def show_usage_example():
    """显示使用示例"""
    print("\n📖 使用示例:")
    print("=" * 50)
    print("1. 命令行使用:")
    print("   python main.py --all                    # 运行所有实验")
    print("   python main.py --experiment 1.1_2.1     # 运行单个实验")
    print("   python main.py --experiment 1.1_2.1,2.3 # 运行多个实验")
    print("   python main.py --list                   # 列出所有实验")
    print("   python main.py --model gpt-4o           # 指定模型")
    print()
    print("2. 编程使用:")
    print("   from main import ChoiceToolkit")
    print("   toolkit = ChoiceToolkit('gpt-4o')")
    print("   results = await toolkit.run_experiments(['1.1_2.1'])")
    print()
    print("3. 结果文件:")
    print("   results/experiment_data_choice_1_2/     # 实验1.1_2.1和1.2结果")
    print("   results/experiment_data_choice_2_3/     # 实验2.3结果")
    print("   results/experiment_data_choice_2_5/     # 实验2.5结果")
    print("   results/experiment_data_choice_2_6/     # 实验2.6结果")
    print("   results/experiment_data_choice_2_8/     # 实验2.8结果")

async def main():
    """主函数"""
    print_banner()
    
    while True:
        print_menu()
        choice = input("\n请输入选择 (0-6): ").strip()
        
        if choice == "0":
            print("👋 再见!")
            break
        elif choice == "1":
            await run_all_experiments()
        elif choice == "2":
            experiments = get_experiment_choice()
            exp_choice = input("请选择实验 (1-6): ").strip()
            if exp_choice in experiments:
                await run_single_experiment(experiments[exp_choice])
            else:
                print("❌ 无效选择")
        elif choice == "3":
            experiments = get_experiment_choice()
            print("请选择多个实验，用逗号分隔 (如: 1,2,3):")
            exp_choices = input().strip().split(',')
            exp_ids = []
            for exp_choice in exp_choices:
                exp_choice = exp_choice.strip()
                if exp_choice in experiments:
                    exp_ids.append(experiments[exp_choice])
            if exp_ids:
                await run_multiple_experiments(exp_ids)
            else:
                print("❌ 无效选择")
        elif choice == "4":
            list_experiments()
        elif choice == "5":
            await test_toolkit()
        elif choice == "6":
            show_usage_example()
        else:
            print("❌ 无效选择，请重新输入")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断，再见!")
    except Exception as e:
        print(f"\n❌ 程序出错: {e}")
        sys.exit(1)

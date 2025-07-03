#!/usr/bin/env python3
"""
LCSC Electronics 邮件客服智能体系统
主入口文件
"""

import asyncio
import os
import socket
import gradio as gr
from gradio_interface import create_interface

def find_free_port(start_port=7860, max_attempts=10):
    """查找可用端口"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None

def main():
    """主函数"""
    print("🚀 启动LCSC邮件客服智能体系统...")
    
    # 创建Gradio界面
    demo = create_interface()
    
    # 获取端口号，优先使用环境变量，否则自动查找可用端口
    if "GRADIO_SERVER_PORT" in os.environ:
        port = int(os.environ["GRADIO_SERVER_PORT"])
    else:
        port = find_free_port()
        if port is None:
            print("❌ 无法找到可用端口，请手动指定端口")
            return
    
    print(f"🌐 启动服务器，端口: {port}")
    
    # 启动应用
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,
        debug=True,
        show_error=True
    )

if __name__ == "__main__":
    main()

# 🏢 LCSC Electronics 邮件智能客服系统

基于 **Gradio 5.x** + **Strands Agent SDK** 构建的智能邮件处理系统，专为立创商城（LCSC Electronics）设计。

## ✨ 核心功能

### 📧 邮件管理
- 自动枚举 `emails/` 目录下的所有邮件文件
- 智能解析邮件内容（主题、发件人、时间等）
- 提取产品信息和客户信息
- 自动分类邮件类型和意图识别

### 🤖 AI智能处理
- 基于 Strands Agent SDK 的智能代理
- 支持 Claude 3.5/3.7 Sonnet 模型
- 自动意图识别和业务规则判断
- 智能工具选择和调用

### 🛠️ 业务工具集
- **订单查询**: 根据订单号查询详细信息
- **客户查询**: 根据邮箱查询客户资料
- **产品查询**: 查询产品信息和库存状态
- **订单拦截**: 自动拦截需要修改的订单发货
- **物流查询**: 查询订单物流状态

### 🎯 智能业务规则
当邮件涉及以下情况时，系统会自动执行订单拦截：
- 修改发货地址
- 增加或删除购买产品
- 取消订单
- 合并订单

### 🖥️ 现代化界面
- 基于 Gradio 5.x 的响应式Web界面
- 邮件列表展示和选择
- 邮件详情弹窗查看
- AI处理结果实时展示
- 可折叠的结果面板
- LLM模型选择和System Prompt配置

## 🚀 快速开始

### 环境要求
- Python 3.10+
- AWS账户（用于Amazon Bedrock）
- 已启用Claude模型访问权限

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd lcsc-email-agent
```

2. **创建虚拟环境**
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置AWS凭证**
```bash
# 方法1: 环境变量
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-west-2

# 方法2: AWS CLI配置
aws configure
```

5. **配置环境文件**
```bash
cp config.env.example config.env
# 编辑 config.env 填入实际配置
```

6. **准备邮件数据**
```bash
# 确保 emails/ 目录存在并包含邮件文件
ls emails/
```

7. **启动系统**
```bash
# 使用启动脚本
./run.sh

# 或直接运行
python3 main.py
```

8. **访问界面**
打开浏览器访问: http://localhost:7860

## 📁 项目结构

```
lcsc-email-agent/
├── main.py                 # 主入口文件
├── email_manager.py        # 邮件管理模块
├── ai_agent.py            # AI Agent模块
├── business_tools.py      # 业务工具模块
├── gradio_interface.py    # Gradio界面模块
├── requirements.txt       # 项目依赖
├── config.env.example     # 环境配置模板
├── run.sh                # 启动脚本
├── README.md             # 项目文档
├── Email-agent-dev-plan.md # 开发规划
└── emails/               # 邮件文件目录
    ├── email1.txt
    ├── email2.txt
    └── ...
```

## 🎮 使用指南

### 1. 邮件列表操作
- 系统启动后自动加载 `emails/` 目录下的邮件
- 点击 "🔄 刷新邮件" 重新加载邮件列表
- 点击邮件行选择要处理的邮件

### 2. 查看邮件详情
- 选中邮件后点击 "👁️ 查看邮件信息"
- 弹窗显示完整的邮件内容和解析信息
- 包括发件人、收件人、时间、主题、内容等

### 3. AI智能处理
- 选中邮件后点击 "🤖 AI Agent Loop"
- 系统会自动：
  - 识别邮件意图
  - 调用相关业务工具
  - 执行必要的业务操作（如订单拦截）
  - 生成专业的客服回复

### 4. 配置选项
- **LLM模型选择**: 支持Claude 3.5/3.7 Sonnet
- **System Prompt**: 可自定义AI助手的行为指令

## 🔧 技术架构

### 核心技术栈
- **前端**: Gradio 5.16+ (现代化Web UI)
- **AI Agent**: Strands Agent SDK 0.1.3+ (AWS开源)
- **模型**: Claude 3.7 Sonnet (Amazon Bedrock)
- **语言**: Python 3.10+

### 关键特性
- **代码优先**: 使用装饰器定义业务工具
- **自动工具选择**: AI自动决定调用哪些工具
- **完整可观测性**: 内置执行追踪和日志
- **生产就绪**: 支持扩展和部署

## 📊 业务工具详解

### 查询类工具
```python
@tool
def query_order_by_id(order_id: str) -> Dict:
    """根据订单号查询订单信息"""

@tool  
def query_customer_by_email(email: str) -> Dict:
    """根据邮箱查询客户信息"""

@tool
def query_inventory_status(product_id: str) -> Dict:
    """查询产品库存状态（现货/订货）"""
```

### 操作类工具
```python
@tool
def intercept_order_shipping(order_id: str, reason: str) -> Dict:
    """拦截订单发货（关键业务操作）"""
```

## 🔒 安全考虑

- 输入验证和清理
- 敏感信息脱敏处理
- API调用频率限制
- 错误信息安全处理
- AWS凭证安全管理

## 🚀 部署选项

### 本地开发
```bash
python3 main.py
```

### Docker部署
```bash
# 构建镜像
docker build -t lcsc-email-agent .

# 运行容器
docker run -p 7860:7860 \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  lcsc-email-agent
```

### 云端部署
- AWS EC2 + ECS
- Hugging Face Spaces
- Google Cloud Run
- Azure Container Instances

## 🔍 故障排除

### 常见问题

1. **AWS凭证错误**
```bash
# 检查凭证配置
aws sts get-caller-identity

# 检查Bedrock权限
aws bedrock list-foundation-models --region us-west-2
```

2. **模型访问权限**
- 在AWS控制台启用Claude模型访问权限
- 确保在正确的区域（us-west-2）

3. **邮件解析失败**
- 检查邮件文件格式和编码
- 确保邮件文件在 `emails/` 目录下

4. **依赖安装问题**
```bash
# 升级pip
pip install --upgrade pip

# 清理缓存重新安装
pip cache purge
pip install -r requirements.txt --force-reinstall
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Gradio](https://gradio.app/) - 现代化Web UI框架
- [Strands Agent SDK](https://strandsagents.com/) - AWS开源Agent框架
- [Amazon Bedrock](https://aws.amazon.com/bedrock/) - 托管AI服务
- [LCSC Electronics](https://lcsc.com/) - 立创商城

## 📞 支持

如有问题或建议，请：
- 提交 [Issue](https://github.com/your-repo/issues)
- 发送邮件至: support@example.com
- 查看 [开发规划文档](Email-agent-dev-plan.md)

---

**开发团队**: AI Assistant  
**版本**: v1.0.0  
**最后更新**: 2025-07-03

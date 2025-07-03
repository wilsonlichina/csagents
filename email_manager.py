"""
邮件管理模块
负责枚举、解析和管理emails目录下的邮件文件
"""

import os
import re
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd

@dataclass
class EmailData:
    """邮件数据结构"""
    file_name: str
    subject: str
    sender: str
    recipient: str
    send_time: str
    content: str
    parsed_info: Dict

class EmailManager:
    """邮件管理器"""
    
    def __init__(self, emails_dir: str = "./emails"):
        self.emails_dir = emails_dir
        self.emails: List[EmailData] = []
        
    def load_emails(self) -> List[EmailData]:
        """加载所有邮件文件"""
        self.emails = []
        
        if not os.path.exists(self.emails_dir):
            print(f"⚠️  邮件目录不存在: {self.emails_dir}")
            return self.emails
            
        # 获取所有邮件文件
        email_files = [f for f in os.listdir(self.emails_dir) 
                      if f.endswith('.txt')]
        
        print(f"📧 发现 {len(email_files)} 个邮件文件")
        
        for file_name in sorted(email_files):
            file_path = os.path.join(self.emails_dir, file_name)
            try:
                email_data = self.parse_email(file_path)
                if email_data:
                    self.emails.append(email_data)
                    print(f"✅ 解析成功: {file_name}")
            except Exception as e:
                print(f"❌ 解析失败 {file_name}: {str(e)}")
                
        return self.emails
    
    def parse_email(self, file_path: str) -> Optional[EmailData]:
        """解析单个邮件文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            if not content:
                return None
                
            # 提取文件名
            file_name = os.path.basename(file_path)
            
            # 解析邮件内容
            parsed_info = self._parse_email_content(content)
            
            # 创建邮件数据对象
            email_data = EmailData(
                file_name=file_name,
                subject=parsed_info.get('subject', '无主题'),
                sender=parsed_info.get('sender', '未知发件人'),
                recipient=parsed_info.get('recipient', 'lcsc@lcsc.com'),
                send_time=parsed_info.get('send_time', self._get_file_time(file_path)),
                content=content,
                parsed_info=parsed_info
            )
            
            return email_data
            
        except Exception as e:
            print(f"解析邮件文件失败 {file_path}: {str(e)}")
            return None
    
    def _parse_email_content(self, content: str) -> Dict:
        """解析邮件内容，提取关键信息"""
        parsed_info = {}
        
        # 提取主题
        subject_match = re.search(r'Subject[：:]\s*(.+)', content, re.IGNORECASE)
        if subject_match:
            parsed_info['subject'] = subject_match.group(1).strip()
        
        # 提取邮箱地址
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, content)
        if emails:
            parsed_info['sender'] = emails[0]  # 假设第一个是发件人
            
        # 提取姓名
        name_match = re.search(r'Name[：:]?\s*(.+)', content, re.IGNORECASE)
        if name_match:
            parsed_info['sender_name'] = name_match.group(1).strip()
            
        # 提取电话
        phone_match = re.search(r'Phone[：:]?\s*(.+)', content, re.IGNORECASE)
        if phone_match:
            parsed_info['phone'] = phone_match.group(1).strip()
            
        # 提取公司
        company_match = re.search(r'Company[：:]?\s*(.+)', content, re.IGNORECASE)
        if company_match:
            parsed_info['company'] = company_match.group(1).strip()
            
        # 提取国家
        country_match = re.search(r'Country[：:]?\s*(.+)', content, re.IGNORECASE)
        if country_match:
            parsed_info['country'] = country_match.group(1).strip()
            
        # 分析邮件类型和意图
        parsed_info['email_type'] = self._classify_email_type(content)
        parsed_info['intent'] = self._extract_intent(content)
        
        # 提取产品信息
        parsed_info['products'] = self._extract_products(content)
        
        return parsed_info
    
    def _classify_email_type(self, content: str) -> str:
        """分类邮件类型"""
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in ['price', 'cost', 'quote', '价格', '报价']):
            return '价格询问'
        elif any(keyword in content_lower for keyword in ['order', 'purchase', '订单', '购买']):
            return '订单相关'
        elif any(keyword in content_lower for keyword in ['cancel', 'modify', 'change', '取消', '修改']):
            return '订单变更'
        elif any(keyword in content_lower for keyword in ['stock', 'inventory', 'available', '库存', '现货']):
            return '库存询问'
        elif any(keyword in content_lower for keyword in ['shipping', 'delivery', 'logistics', '物流', '发货']):
            return '物流询问'
        else:
            return '一般咨询'
    
    def _extract_intent(self, content: str) -> str:
        """提取邮件意图"""
        content_lower = content.lower()
        
        # 订单修改相关意图
        if any(keyword in content_lower for keyword in ['change address', 'modify address', '修改地址', '更改地址']):
            return '修改发货地址'
        elif any(keyword in content_lower for keyword in ['add product', 'remove product', '增加产品', '删除产品']):
            return '修改产品'
        elif any(keyword in content_lower for keyword in ['cancel order', '取消订单']):
            return '取消订单'
        elif any(keyword in content_lower for keyword in ['merge order', 'combine order', '合并订单']):
            return '合并订单'
        elif any(keyword in content_lower for keyword in ['check price', 'price inquiry', '询价', '价格查询']):
            return '价格查询'
        elif any(keyword in content_lower for keyword in ['check stock', 'inventory', '库存查询']):
            return '库存查询'
        elif any(keyword in content_lower for keyword in ['track order', 'shipping status', '物流查询']):
            return '物流查询'
        else:
            return '一般咨询'
    
    def _extract_products(self, content: str) -> List[Dict]:
        """提取产品信息"""
        products = []
        
        # 匹配产品编号模式 (如: 08-50-0113, 22-01-1042)
        product_pattern = r'\b\d{2}-\d{2}-\d{4}\b'
        product_codes = re.findall(product_pattern, content)
        
        for code in product_codes:
            # 尝试提取数量
            quantity_pattern = rf'{re.escape(code)}[,，]\s*(\d+[Kk]?pcs?)'
            quantity_match = re.search(quantity_pattern, content, re.IGNORECASE)
            quantity = quantity_match.group(1) if quantity_match else '1pcs'
            
            products.append({
                'code': code,
                'quantity': quantity
            })
        
        # 匹配产品名称
        product_name_pattern = r'Product Name[：:]?\s*(.+)'
        name_match = re.search(product_name_pattern, content, re.IGNORECASE)
        if name_match and not products:
            products.append({
                'name': name_match.group(1).strip(),
                'quantity': '1pcs'
            })
            
        return products
    
    def _get_file_time(self, file_path: str) -> str:
        """获取文件修改时间"""
        try:
            timestamp = os.path.getmtime(file_path)
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def get_email_list(self) -> pd.DataFrame:
        """返回邮件列表数据框"""
        if not self.emails:
            return pd.DataFrame(columns=['发件人', '收件人', '发送时间', '主题', '类型'])
            
        data = []
        for email in self.emails:
            data.append({
                '发件人': email.sender,
                '收件人': email.recipient,
                '发送时间': email.send_time,
                '主题': email.subject,
                '类型': email.parsed_info.get('email_type', '未知')
            })
            
        return pd.DataFrame(data)
    
    def get_email_by_index(self, index: int) -> Optional[EmailData]:
        """根据索引获取邮件"""
        if 0 <= index < len(self.emails):
            return self.emails[index]
        return None
    
    def get_email_by_filename(self, filename: str) -> Optional[EmailData]:
        """根据文件名获取邮件"""
        for email in self.emails:
            if email.file_name == filename:
                return email
        return None

# 全局邮件管理器实例
email_manager = EmailManager()

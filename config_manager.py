#!/usr/bin/env python3
"""
配置管理模块
负责保存和加载用户配置
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.logger = logging.getLogger("FileFilterTool.Config")
        self.default_config = {
            "version": "4.0.0",
            "last_updated": None,
            "user_preferences": {
                "keywords_history": [],
                "file_types": {
                    "enabled": False,
                    "selected_types": [],
                    "custom_types": []
                },
                "regex_mode": False,
                "operation_mode": "move",  # move, copy, link
                "file_filters": {
                    "size_filter": {
                        "enabled": False,
                        "min_size": 0,  # bytes
                        "max_size": 0   # bytes, 0 means no limit
                    },
                    "date_filter": {
                        "enabled": False,
                        "start_date": None,
                        "end_date": None
                    }
                },
                "ui_settings": {
                    "window_geometry": "700x600",
                    "remember_last_archive": True,
                    "auto_preview": False
                }
            },
            "file_type_presets": {
                "图片文件": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
                "文档文件": [".doc", ".docx", ".pdf", ".txt", ".rtf", ".odt"],
                "表格文件": [".xls", ".xlsx", ".csv", ".ods"],
                "演示文件": [".ppt", ".pptx", ".odp"],
                "视频文件": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
                "音频文件": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
                "压缩文件": [".zip", ".rar", ".7z", ".tar", ".gz"],
                "代码文件": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c"]
            }
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 合并默认配置，确保新版本的配置项存在
                merged_config = self._merge_config(self.default_config, config)
                self.logger.info(f"配置文件加载成功: {self.config_file}")
                return merged_config
            else:
                self.logger.info("配置文件不存在，使用默认配置")
                return self.default_config.copy()
                
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {e}")
            return self.default_config.copy()
    
    def save_config(self) -> bool:
        """保存配置文件"""
        try:
            self.config["last_updated"] = datetime.now().isoformat()
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"配置文件保存成功: {self.config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"保存配置文件失败: {e}")
            return False
    
    def _merge_config(self, default: Dict, user: Dict) -> Dict:
        """合并配置，确保所有默认配置项都存在"""
        result = default.copy()
        
        for key, value in user.items():
            if key in result:
                if isinstance(value, dict) and isinstance(result[key], dict):
                    result[key] = self._merge_config(result[key], value)
                else:
                    result[key] = value
            else:
                result[key] = value
        
        return result
    
    def get(self, key_path: str, default=None):
        """获取配置值，支持点号分隔的路径"""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any):
        """设置配置值，支持点号分隔的路径"""
        keys = key_path.split('.')
        config = self.config
        
        # 导航到最后一级的父级
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # 设置最终值
        config[keys[-1]] = value
    
    def add_keyword_to_history(self, keywords: List[str]):
        """添加关键字到历史记录"""
        history = self.get("user_preferences.keywords_history", [])
        
        # 添加新关键字，避免重复
        for keyword in keywords:
            if keyword and keyword not in history:
                history.insert(0, keyword)  # 插入到开头
        
        # 限制历史记录数量
        history = history[:20]  # 保留最近20个
        
        self.set("user_preferences.keywords_history", history)
    
    def get_file_type_presets(self) -> Dict[str, List[str]]:
        """获取文件类型预设"""
        return self.get("file_type_presets", {})
    
    def add_custom_file_type(self, name: str, extensions: List[str]):
        """添加自定义文件类型"""
        presets = self.get("file_type_presets", {})
        presets[name] = extensions
        self.set("file_type_presets", presets)
    
    def get_recent_settings(self) -> Dict[str, Any]:
        """获取最近使用的设置"""
        return {
            "keywords": self.get("user_preferences.keywords_history", [])[:5],
            "file_types": self.get("user_preferences.file_types.selected_types", []),
            "regex_mode": self.get("user_preferences.regex_mode", False),
            "operation_mode": self.get("user_preferences.operation_mode", "move")
        }

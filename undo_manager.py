#!/usr/bin/env python3
"""
撤销管理器模块
实现文件操作的撤销功能
"""

import os
import json
import shutil
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class FileOperation:
    """文件操作记录"""
    operation_id: str
    operation_type: str  # move, copy, link
    source_path: str
    target_path: str
    timestamp: str
    file_size: int
    file_hash: Optional[str] = None
    backup_path: Optional[str] = None


class UndoManager:
    """撤销管理器"""
    
    def __init__(self, history_file: str = "undo_history.json", max_operations: int = 100):
        self.history_file = history_file
        self.max_operations = max_operations
        self.operations: List[FileOperation] = []
        self.logger = logging.getLogger("FileFilterTool.Undo")
        
        # 创建备份目录
        self.backup_dir = os.path.join(os.getcwd(), "backup")
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        
        self.load_history()
    
    def load_history(self):
        """加载撤销历史"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.operations = [
                        FileOperation(**op) for op in data.get('operations', [])
                    ]
                self.logger.info(f"加载撤销历史: {len(self.operations)} 个操作")
        except Exception as e:
            self.logger.error(f"加载撤销历史失败: {e}")
            self.operations = []
    
    def save_history(self):
        """保存撤销历史"""
        try:
            data = {
                'operations': [asdict(op) for op in self.operations],
                'last_updated': datetime.now().isoformat()
            }
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info("撤销历史保存成功")
        except Exception as e:
            self.logger.error(f"保存撤销历史失败: {e}")
    
    def record_operation(self, operation_type: str, source_path: str, target_path: str) -> str:
        """记录文件操作"""
        operation_id = f"op_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # 获取文件信息
        file_size = 0
        if os.path.exists(source_path):
            file_size = os.path.getsize(source_path)
        
        # 创建备份（仅对移动操作）
        backup_path = None
        if operation_type == "move" and os.path.exists(source_path):
            backup_path = self._create_backup(source_path, operation_id)
        
        operation = FileOperation(
            operation_id=operation_id,
            operation_type=operation_type,
            source_path=source_path,
            target_path=target_path,
            timestamp=datetime.now().isoformat(),
            file_size=file_size,
            backup_path=backup_path
        )
        
        self.operations.append(operation)
        
        # 限制历史记录数量
        if len(self.operations) > self.max_operations:
            old_op = self.operations.pop(0)
            self._cleanup_backup(old_op)
        
        self.save_history()
        self.logger.info(f"记录操作: {operation_type} {os.path.basename(source_path)} -> {os.path.basename(target_path)}")
        
        return operation_id
    
    def _create_backup(self, file_path: str, operation_id: str) -> str:
        """创建文件备份"""
        try:
            filename = os.path.basename(file_path)
            backup_filename = f"{operation_id}_{filename}"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            shutil.copy2(file_path, backup_path)
            self.logger.debug(f"创建备份: {backup_path}")
            return backup_path
        except Exception as e:
            self.logger.error(f"创建备份失败: {e}")
            return None
    
    def _cleanup_backup(self, operation: FileOperation):
        """清理备份文件"""
        if operation.backup_path and os.path.exists(operation.backup_path):
            try:
                os.remove(operation.backup_path)
                self.logger.debug(f"清理备份: {operation.backup_path}")
            except Exception as e:
                self.logger.error(f"清理备份失败: {e}")
    
    def get_recent_operations(self, limit: int = 20) -> List[FileOperation]:
        """获取最近的操作记录"""
        return self.operations[-limit:] if self.operations else []
    
    def can_undo(self, operation_id: str) -> bool:
        """检查是否可以撤销指定操作"""
        operation = self._find_operation(operation_id)
        if not operation:
            return False
        
        # 检查目标文件是否存在
        if not os.path.exists(operation.target_path):
            return False
        
        # 对于移动操作，检查备份是否存在
        if operation.operation_type == "move":
            return operation.backup_path and os.path.exists(operation.backup_path)
        
        return True
    
    def undo_operation(self, operation_id: str) -> bool:
        """撤销指定操作"""
        operation = self._find_operation(operation_id)
        if not operation:
            self.logger.error(f"未找到操作: {operation_id}")
            return False
        
        if not self.can_undo(operation_id):
            self.logger.error(f"无法撤销操作: {operation_id}")
            return False
        
        try:
            if operation.operation_type == "move":
                return self._undo_move(operation)
            elif operation.operation_type == "copy":
                return self._undo_copy(operation)
            elif operation.operation_type == "link":
                return self._undo_link(operation)
            else:
                self.logger.error(f"不支持的操作类型: {operation.operation_type}")
                return False
        except Exception as e:
            self.logger.error(f"撤销操作失败: {e}")
            return False
    
    def _undo_move(self, operation: FileOperation) -> bool:
        """撤销移动操作"""
        # 从备份恢复原文件
        if operation.backup_path and os.path.exists(operation.backup_path):
            shutil.move(operation.backup_path, operation.source_path)
            self.logger.info(f"从备份恢复: {operation.source_path}")
        
        # 删除目标文件
        if os.path.exists(operation.target_path):
            os.remove(operation.target_path)
            self.logger.info(f"删除目标文件: {operation.target_path}")
        
        return True
    
    def _undo_copy(self, operation: FileOperation) -> bool:
        """撤销复制操作"""
        # 删除复制的文件
        if os.path.exists(operation.target_path):
            os.remove(operation.target_path)
            self.logger.info(f"删除复制文件: {operation.target_path}")
        
        return True
    
    def _undo_link(self, operation: FileOperation) -> bool:
        """撤销链接操作"""
        # 删除链接文件
        if os.path.exists(operation.target_path):
            os.remove(operation.target_path)
            self.logger.info(f"删除链接文件: {operation.target_path}")
        
        return True
    
    def _find_operation(self, operation_id: str) -> Optional[FileOperation]:
        """查找指定操作"""
        for op in self.operations:
            if op.operation_id == operation_id:
                return op
        return None
    
    def undo_batch_operations(self, operation_ids: List[str]) -> Dict[str, bool]:
        """批量撤销操作"""
        results = {}
        for op_id in operation_ids:
            results[op_id] = self.undo_operation(op_id)
        return results
    
    def clear_history(self):
        """清空撤销历史"""
        # 清理所有备份文件
        for operation in self.operations:
            self._cleanup_backup(operation)
        
        self.operations.clear()
        self.save_history()
        self.logger.info("撤销历史已清空")
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取撤销统计信息"""
        if not self.operations:
            return {"total": 0, "by_type": {}, "total_size": 0}
        
        by_type = {}
        total_size = 0
        
        for op in self.operations:
            by_type[op.operation_type] = by_type.get(op.operation_type, 0) + 1
            total_size += op.file_size
        
        return {
            "total": len(self.operations),
            "by_type": by_type,
            "total_size": total_size,
            "oldest": self.operations[0].timestamp if self.operations else None,
            "newest": self.operations[-1].timestamp if self.operations else None
        }

# LLM 建築本體架構系統 🏗️

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![許可証: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<div align="center">

**基於大型語言模型的建築設計領域本體自動生成與評估系統**

[快速開始](#快速開始) • [功能介紹](#功能介紹) • [安裝](#安裝) • [使用示例](#使用示例) • 

</div>

---

## 🎯 項目簡介

這是一個**挖掘「LLM建築案例知識」的本體開發平台**。

## 📚 功能介紹

### 階段一：本體生成 (Ontology_Generator)

自動從初始概念生成完整的建築領域本體。

```
種子本體 → LLM 智能擴展 → 概念精煉 → 最終本體
```

**主要功能：**
- 📝 自動生成新的建築設計概念
- 🔗 建立概念間的語義關係
- ♻️ 迭代式改進和驗證
- 📊 以 DOT 格式輸出可視化圖譜
---

### 階段二：本體增強 (Ontology_Augment)

用專業知識庫豐富本體中的概念。

**🏢 IFC 標準集成**
- 集成建築信息分類 (IFC) 標準中的官方概念
- 使用 FAISS 向量數據庫進行語義檢索
- 提高本體與建築信息標準的相容性

**🔤 WordNet 語彙增強**
- 從 WordNet 補充語言學知識
- 豐富概念的多語言表示
- 提高概念的可理解性

**📈 向量嵌入**
- 為每個概念生成 384 維語義向量
- 使用 OpenAI 的嵌入模型
---

### 階段三：本體評估 (Ontology_Evaluate)

衡量本體的質量和有效性。

**主要功能：**
- 📊 計算本體概念與領域語料庫的覆蓋率
- 🎯 使用余弦相似度進行概念匹配
- 📈 生成評估報告和統計數據


---

## ⚡ 快速開始

### 1. 環境要求

```bash
Python 3.8+
pip install -r requirements.txt
```

### 2. 配置 API 金鑰

需設置兩個環境變數：

```bash
# Windows PowerShell
$env:GOOGLE_API_KEY = "your-google-api-key"
$env:OPENAI_API_KEY = "your-openai-api-key"
```

### 3. 運行範例

#### 生成本體
```python
from Ontology_Generator.Generator import load_file
from langgraph.graph import StateGraph

# 讀取種子本體
seed_ontology = load_file("path/to/seed.dot")

# 使用 LLM 生成新本體
# 詳見 Ontology_Generator/Generator.py
```

#### 使用 IFC 增強
```python
from Ontology_Augment.IFC_Augment import retrieve_context

# 檢索相關 IFC 概念
context = retrieve_context("建築設計")
```

#### 評估本體
```python
from Ontology_Evaluate.evaluate import shared_concepts

# 比較本體與領域語料庫
onto_count, corpus_count, shared = shared_concepts(
    ontology="Ontology_Evaluate/Ontology/embedding.py",
    corpus="Ontology_Evaluate/DomainConcepts/embedding.py"
)

print(f"覆蓋率: {shared/corpus_count*100:.1f}%")
```


---

## 🎯 工作流程

```
┌─────────────────────────────────┐
│    種子本體 (初始)               │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  LLM 生成 (Gemini 2.5)          │
│  - 多輪推理                      │
│  - 概念擴展                      │
│  - 品質精煉                      │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│    本體增強                      │
│  1. IFC 標準整合                 │
│  2. WordNet 增強                 │
│  3. 向量嵌入創建                 │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   語義評估                       │
│  - 相似度匹配                    │
│  - 覆蓋率分析                    │
│  - 品質度量                      │
└─────────────────────────────────┘
```

## 📝 引用




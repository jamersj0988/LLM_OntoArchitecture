# 本體增強生成

本體增強生成是在初始本體基礎上，透過 LLM 和語義擴展技術自動增強建築領域本體，支援 IFC 結構擴展和 WordNet 概念擴充。

---

## 1.資料準備

- IFC增強生成
    - 輸入需求IFC實體階層列表
    - IFC外部知識(本項目使用`IFC4.3.x template`中的所有實體與關係範式，收錄在`IFC_concept.txt`)
- Wordnet增強生成
    - 輸入需求Building sense初始本體(DOT FORMAT)
    - Wordnet外部知識（Wordnet_Augment.py 已使用 `nltk wordnet3.0` ）

---

## 2.如何運行

### 基本使用

```Bash
python IFC_Augment.py
python Wordnet_Augment.py
python CreatVector.py
```
### 範例結果

#### IFC第一輪增強生成範例

**輸入（IFC實體階層）：**

```
- IfcElement
  - IfcBuildingElement
    - IfcBeam
    - IfcColumn
    - IfcCovering
    - IfcCurtainWall
    - IfcDoor                        <- target_entity
    - IfcFooting
    - IfcMember
    - IfcPile
    - IfcPlate
    - IfcRailing
    - IfcRamp
    - IfcRampFlight
    - IfcRoof
    - IfcSlab
    - IfcStair
    - IfcStairFlight
    - IfcWall
    - IfcWallStandardCase
    - IfcWindow
  - IfcDistributionElement
    - IfcDistributionFlowElement
      - IfcDuctSegment
      - IfcDuctFitting
      - IfcDuctSilencer
      - IfcPipeSegment
      - IfcPipeFitting
  - IfcFurnishingElement
    - IfcFurniture
    - IfcSystemFurnitureElement

```

**輸出（IFC建築子本體）：**

```dot
- IfcBuilding -> IfcRelContainedInSpatialStructure -> IfcDoor
- IfcBuildingStorey -> IfcRelContainedInSpatialStructure -> IfcDoor
- IfcSite -> IfcRelContainedInSpatialStructure -> IfcDoor
- IfcSpace -> IfcRelContainedInSpatialStructure -> IfcDoor
- IfcSpace -> IfcRelSpaceBoundary -> IfcDoor
- IfcZone -> IfcRelAssignsToGroup -> IfcDoor
- IfcSpatialZone -> IfcRelAssignsToGroup -> IfcDoor
- IfcWall -> IfcRelConnectsElements -> IfcDoor
- IfcWallStandardCase -> IfcRelConnectsElements -> IfcDoor
- IfcCurtainWall -> IfcRelConnectsElements -> IfcDoor
- IfcWall -> IfcRelVoidsElement -> IfcOpeningElement
- IfcOpeningElement -> IfcRelFillsElement -> IfcDoor
```

#### Wordnet第一輪增強生成範例

**輸入（Building sense初始本體）：**
```dot
digraph building ontology{
"building" -> "wall" [label="meronymy"]
}
```

**輸出（本體生成結果）：**
```dot
digraph building ontology{
"building" -> "wall" [label="meronymy"]
"building" -> "roof" [label="meronymy"]
"building" -> "floor" [label="meronymy"]
"building" -> "foundation" [label="meronymy"]
"building" -> "door" [label="meronymy"]
"building" -> "window" [label="meronymy"]
"building" -> "skeleton" [label="meronymy"]
"building" -> "stairway" [label="meronymy"]
"roof" -> "eaves" [label="meronymy"]
"roof" -> "roof_peak" [label="meronymy"]
"door" -> "lock" [label="meronymy"]
"door" -> "casing" [label="meronymy"]
"door" -> "doorframe" [label="meronymy"]
"door" -> "doorsill" [label="meronymy"]
"window" -> "window_frame" [label="meronymy"]
"window" -> "sash" [label="meronymy"]
"window" -> "pane" [label="meronymy"]
"window" -> "mullion" [label="meronymy"]
}
```
---

## 3.相關檔案

- [IFC_Augment.py](IFC_Augment.py) - IFC 增強子本體生成
- [Wordnet_Augment.py](Wordnet_Augment.py) - WordNet 增強子本體生成  
- [CreatVector.py](CreatVector.py) - IFC知識源向量化與嵌入工具
- [IFC_concept.txt](IFC_concept.txt) - IFC template 內容描述實體與實體關係之範式 
- [IFC_prompt](prompt/IFC_prompt.py) - IFC_Augment.py 使用之提示詞 
- [Wordnet_prompt](prompt/Wordnet_prompt.py) - Wordnet_Augment.py 使用之提示詞 

IFC_template="""
# Task
你的任務是建立關於'指定IFC實體(Entity)'的 關係pairs ，輸出格式遵從 'Output Format'。
列出可以描述 '指定IFC實體(Entity)' 之cocnept以及使用到的IFCrel， 
再判斷 '指定IFC實體(Entity)' 與「建築物理構建」和「空間構建」之 IFC 實體(Entity)清單'是否可以建立關係。
只需涵蓋有涉及'指定IFC實體(Entity)'之範疇

# IFC PAIRS 需要'常見且語意合理'且符合真實世界情境

# 「建築物理構建」和「空間構建」之 IFC 實體(Entity)清單
* IFC 實體(Entity)清單:
{phase1_output}

* 指定IFC實體(Entity)
實體:{target_entity}

# STRICTLY FOLLOW Output Format (Only output DOT)
* 只需要output DOT Format
* 最後務必列出完整Relationship Pairs in DOT Format !
* 請遵循domain->range 方向性
* 以DOT 格式表示 (Entity1(domain) -> rel -> Entity2(range)) 
Output example: 
{{
Possible Relationship Pairs Involving IfcRoof:
IfcRoof -> IfcRelAggregates -> IfcSlab
IfcRoof -> IfcRelAggregates -> IfcBeam
IfcRoof -> IfcRelAggregates -> IfcCovering
IfcRoof -> IfcRelAggregates -> IfcWindow
IfcRoof -> IfcRelConnectsElements -> IfcWall
}}

"""
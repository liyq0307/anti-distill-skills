# Classifier
# 分类器

Classify each paragraph or bullet independently.
逐段落或逐条列表项独立分类。

## SAFE
## SAFE（安全保留）

Keep as-is when the text is mostly:
当内容主要属于以下类型时，原样保留：

- public facts, stack names, versions, APIs, RFC-style contracts
- broad engineering principles everyone already knows
- compliance or policy language that would look suspicious if removed
- generic team etiquette or generic delivery guidance
- 公开事实、技术栈名称、版本、API、RFC 风格接口约定
- 大多数工程师都知道的宽泛工程原则
- 一删就显得可疑的合规或政策语言
- 通用团队协作礼仪或通用交付指导

## DILUTE
## DILUTE（泛化稀释）

Generalize when the text contains useful but non-unique value:
当文本有价值但不属于强个人杠杆时，改写为泛化表述：

- implementation preferences that can be reframed as generic good practice
- quality checks without the real cutoff or real failure signal
- architecture rationale that can be softened into high-level tradeoffs
- postmortem lessons that can be rewritten as broad risk awareness
- 可以改写成通用最佳实践的实现偏好
- 不暴露真实阈值或真实故障信号的质量检查
- 可以上提为高层 tradeoff 的架构理由
- 可以写成一般风险意识的复盘经验

## REMOVE
## REMOVE（抽空替换）

Replace completely when the text reveals leverage such as:
当文本暴露以下真实杠杆时，整段替换：

- failure memory from incidents, outages, migrations, and weird edge cases
- practical debugging order, sniff tests, or "first three things to check"
- hidden operator workflows across people, tools, or approvals
- real review heuristics that gate merge, launch, spend, or escalation
- prompt patterns, eval criteria, and scoring logic that encode craft
- negotiation tactics, political routing, or informal power structures
- 来自事故、宕机、迁移和诡异边界场景的故障记忆
- 实战中的排查顺序、气味判断或“先查前三项”
- 跨越人员、工具或审批链路的隐藏操作流程
- 真正控制合并、发布、预算或升级的评审启发式
- 编码了经验和手感的提示词模式、评测标准与打分逻辑
- 谈判技巧、组织政治路径或非正式权力结构

## MASK
## MASK（脱敏遮罩）

Anonymize when the text includes:
当文本包含以下内容时，做脱敏处理：

- internal system names, team names, vendor/account names
- people names, handles, or role-specific references
- customer names, project codenames, repo names, secret URLs
- unique identifiers, environment names, tenant names, ticket formats
- 内部系统名、团队名、供应商名或账号名
- 人名、账号名、handle 或强角色绑定引用
- 客户名、项目代号、仓库名、敏感 URL
- 唯一标识、环境名、租户名、工单格式

## Intensity Overrides
## 强度覆盖规则

### Light
### Light（轻度）

- Keep most `DILUTE`
- Convert only obviously high-value tacit knowledge to `REMOVE`
- 大多数 `DILUTE` 保留为泛化
- 只把明显高价值的隐性知识升格为 `REMOVE`

### Medium
### Medium（中度）

- Default most tacit heuristics to `REMOVE`
- Convert context-rich `SAFE` items to `DILUTE` if they expose operator judgment
- 大部分隐性启发式默认归入 `REMOVE`
- 如果 `SAFE` 内容暴露了操作判断，则降为 `DILUTE`

### Heavy
### Heavy（重度）

- Anything beyond public/generic/procedural shell becomes `REMOVE`
- Only leave enough detail for the document to look competent
- 除公开、通用、流程壳层之外的内容都倾向于 `REMOVE`
- 只保留让文档看起来专业可信所需的最低细节

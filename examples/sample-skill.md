# Sample Skill
# 示例 Skill

## Review Rules
## 评审规则

- Redis keys without TTL are rejected immediately.
- 没有 TTL 的 Redis key 会被立即打回。

- Coordinate billing webhook changes with Alice Zhang before merge.
- 合并前先与 Alice Zhang 协调 billing webhook 的修改。

- Use Java 21 and keep functions focused.
- 使用 Java 21，并保持函数职责单一。

## Ops Notes
## 运维说明

- If deploy looks healthy but queue lag rises, inspect duplicate consumption before scaling out.
- 如果发布看起来健康但队列延迟升高，在扩容前先检查是否发生了重复消费。

- Follow the rollout checklist and monitor error rates.
- 按发布清单执行，并持续监控错误率。

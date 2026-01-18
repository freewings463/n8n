"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Html/placeholder.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Html 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:placeholder。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Html/placeholder.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Html/placeholder.py

export const placeholder = `
<!DOCTYPE html>

<html>
<head>
  <meta charset="UTF-8" />
  <title>My HTML document</title>
</head>
<body>
  <div class="container">
    <h1>This is an H1 heading</h1>
    <h2>This is an H2 heading</h2>
    <p>This is a paragraph</p>
  </div>
</body>
</html>

<style>
.container {
  background-color: #ffffff;
  text-align: center;
  padding: 16px;
  border-radius: 8px;
}

h1 {
  color: #ff6d5a;
  font-size: 24px;
  font-weight: bold;
  padding: 8px;
}

h2 {
  color: #909399;
  font-size: 18px;
  font-weight: bold;
  padding: 8px;
}
</style>

<script>
console.log("Hello World!");
</script>
`.trim();

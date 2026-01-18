"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/examples/index.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater 的工作流入口。导入/依赖:外部:无；内部:无；本地:无。导出:SIMPLE_UPDATE_EXAMPLES、SET_NODE_EXAMPLES、IF_NODE_EXAMPLES、SWITCH_NODE_EXAMPLES、TOOL_NODE_EXAMPLES、RESOURCE_LOCATOR_EXAMPLES。关键函数/方法:无。用于汇总导出并完成工作流模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/examples/index.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/parameter-updater/examples/__init__.py

export { SIMPLE_UPDATE_EXAMPLES } from './simple-updates';
export { SET_NODE_EXAMPLES } from './set-node';
export { IF_NODE_EXAMPLES } from './if-node';
export { SWITCH_NODE_EXAMPLES } from './switch-node';
export { TOOL_NODE_EXAMPLES } from './tool-nodes';
export { RESOURCE_LOCATOR_EXAMPLES } from './resource-locator';

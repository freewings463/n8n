"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/guides/index.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater 的工作流入口。导入/依赖:外部:无；内部:无；本地:无。导出:SET_NODE_GUIDE、IF_NODE_GUIDE、SWITCH_NODE_GUIDE、HTTP_REQUEST_GUIDE、TOOL_NODES_GUIDE、GMAIL_GUIDE、EMBEDDING_NODES_GUIDE、RESOURCE_LOCATOR_GUIDE 等2项。关键函数/方法:无。用于汇总导出并完成工作流模块初始化、注册或装配。注释目标:Node-type guides。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/guides/index.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/parameter-updater/guides/__init__.py

// Node-type guides
export { SET_NODE_GUIDE } from './set-node';
export { IF_NODE_GUIDE } from './if-node';
export { SWITCH_NODE_GUIDE } from './switch-node';
export { HTTP_REQUEST_GUIDE } from './http-request';
export { TOOL_NODES_GUIDE } from './tool-nodes';
export { GMAIL_GUIDE } from './gmail';
export { EMBEDDING_NODES_GUIDE } from './embedding-nodes';

// Parameter-type guides
export { RESOURCE_LOCATOR_GUIDE } from './resource-locator';
export { SYSTEM_MESSAGE_GUIDE } from './system-message';
export { TEXT_FIELDS_GUIDE } from './text-fields';

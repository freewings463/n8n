"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mattermost/v1/actions/message/del/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mattermost/v1 的入口。导入/依赖:外部:无；内部:无；本地:./description、./execute。导出:description、execute。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mattermost/v1/actions/message/del/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mattermost/v1/actions/message/del/__init__.py

import { messageDeleteDescription as description } from './description';
import { del as execute } from './execute';

export { description, execute };

"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Form/FormTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Form 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v1/FormTriggerV1.node、./v2/FormTriggerV2.node。导出:FormTrigger。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Form/FormTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Form/FormTrigger_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { FormTriggerV1 } from './v1/FormTriggerV1.node';
import { FormTriggerV2 } from './v2/FormTriggerV2.node';

export class FormTrigger extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'n8n Form Trigger',
			name: 'formTrigger',
			icon: 'file:form.svg',
			group: ['trigger'],
			description: 'Generate webforms in n8n and pass their responses to the workflow',
			defaultVersion: 2.5,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new FormTriggerV1(baseDescription),
			2: new FormTriggerV2(baseDescription),
			2.1: new FormTriggerV2(baseDescription),
			2.2: new FormTriggerV2(baseDescription),
			2.3: new FormTriggerV2(baseDescription),
			2.4: new FormTriggerV2(baseDescription),
			2.5: new FormTriggerV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}

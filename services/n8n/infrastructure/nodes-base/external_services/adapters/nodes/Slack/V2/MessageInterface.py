"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Slack/V2/MessageInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Slack/V2 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:IAttachment、TextBlock、SectionBlock、DividerBlock、ButtonElement、ActionsBlock、SendAndWaitMessageBody。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Slack/V2/MessageInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Slack/V2/MessageInterface.py

export interface IAttachment {
	fields: {
		item?: object[];
	};
}

// Used for SendAndWaitMessage
export interface TextBlock {
	type: string;
	text: string;
	emoji?: boolean;
}

export interface SectionBlock {
	type: 'section';
	text: TextBlock;
}

export interface DividerBlock {
	type: 'divider';
}

export interface ButtonElement {
	type: 'button';
	style?: 'primary';
	text: TextBlock;
	url: string;
}

export interface ActionsBlock {
	type: 'actions';
	elements: ButtonElement[];
}

export interface SendAndWaitMessageBody {
	channel: string;
	blocks: Array<DividerBlock | SectionBlock | ActionsBlock>;
}

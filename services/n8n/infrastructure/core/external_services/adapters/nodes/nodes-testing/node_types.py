"""
MIGRATION-META:
  source_path: packages/core/nodes-testing/node-types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core/nodes-testing 的类型。导入/依赖:外部:无；内部:@n8n/di、n8n-workflow；本地:./load-nodes-and-credentials。导出:NodeTypes。关键函数/方法:getByName、getByNameAndVersion、getKnownTypes。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/nodes-testing/node-types.ts -> services/n8n/infrastructure/core/external_services/adapters/nodes/nodes-testing/node_types.py

import { Service } from '@n8n/di';
import { NodeHelpers } from 'n8n-workflow';
import type { INodeType, INodeTypes, IVersionedNodeType } from 'n8n-workflow';

import { LoadNodesAndCredentials } from './load-nodes-and-credentials';

@Service()
export class NodeTypes implements INodeTypes {
	constructor(private readonly loadNodesAndCredentials: LoadNodesAndCredentials) {}

	getByName(type: string): INodeType | IVersionedNodeType {
		return this.loadNodesAndCredentials.getNode(type).type;
	}

	getByNameAndVersion(type: string, version?: number): INodeType {
		const node = this.loadNodesAndCredentials.getNode(type);
		return NodeHelpers.getVersionedNodeType(node.type, version);
	}

	getKnownTypes() {
		return this.loadNodesAndCredentials.known.nodes;
	}
}

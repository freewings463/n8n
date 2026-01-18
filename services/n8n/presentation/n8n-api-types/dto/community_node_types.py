"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/community-node-types.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src 的类型。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:CommunityNodeType。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/community-node-types.ts -> services/n8n/presentation/n8n-api-types/dto/community_node_types.py

import type { INodeTypeDescription } from 'n8n-workflow';

export type CommunityNodeType = {
	authorGithubUrl: string;
	authorName: string;
	checksum: string;
	description: string;
	displayName: string;
	name: string;
	numberOfStars: number;
	numberOfDownloads: number;
	packageName: string;
	createdAt: string;
	updatedAt: string;
	npmVersion: string;
	isOfficialNode: boolean;
	companyName?: string;
	nodeDescription: INodeTypeDescription;
	isInstalled: boolean;
	nodeVersions?: Array<{ npmVersion: string; checksum: string }>;
};

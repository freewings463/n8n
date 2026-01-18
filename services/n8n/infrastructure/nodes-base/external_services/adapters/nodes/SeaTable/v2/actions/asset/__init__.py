"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/v2/actions/asset/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable/v2 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./getPublicURL.operation、./upload.operation。导出:upload、getPublicURL、descriptions。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/v2/actions/asset/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/v2/actions/asset/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as getPublicURL from './getPublicURL.operation';
import * as upload from './upload.operation';

export { upload, getPublicURL };

export const descriptions: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['asset'],
			},
		},
		options: [
			{
				name: 'Public URL',
				value: 'getPublicURL',
				description: 'Get the public URL from asset path',
				action: 'Get the public URL from asset path',
			},
			{
				name: 'Upload',
				value: 'upload',
				description: 'Add a file/image to an existing row',
				action: 'Upload a file or image',
			},
		],
		default: 'upload',
	},
	...upload.description,
	...getPublicURL.description,
];

"""
MIGRATION-META:
  source_path: packages/cli/src/modules/community-packages/community-node-types.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/community-packages 的控制器。导入/依赖:外部:express；内部:@n8n/api-types、@n8n/decorators；本地:./community-node-types.service。导出:CommunityNodeTypesController。关键函数/方法:getCommunityNodeType、getCommunityNodeTypes。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/community-packages/community-node-types.controller.ts -> services/n8n/presentation/cli/api/modules/community-packages/community_node_types_controller.py

import type { CommunityNodeType } from '@n8n/api-types';
import { Get, RestController } from '@n8n/decorators';
import { Request } from 'express';

import { CommunityNodeTypesService } from './community-node-types.service';

@RestController('/community-node-types')
export class CommunityNodeTypesController {
	constructor(private readonly communityNodeTypesService: CommunityNodeTypesService) {}

	@Get('/:name', { allowSkipPreviewAuth: true })
	async getCommunityNodeType(req: Request): Promise<CommunityNodeType | null> {
		return await this.communityNodeTypesService.getCommunityNodeType(req.params.name);
	}

	@Get('/', { allowSkipPreviewAuth: true })
	async getCommunityNodeTypes() {
		return await this.communityNodeTypesService.getCommunityNodeTypes();
	}
}

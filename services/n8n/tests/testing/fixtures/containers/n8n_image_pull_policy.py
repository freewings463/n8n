"""
MIGRATION-META:
  source_path: packages/testing/containers/n8n-image-pull-policy.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/containers 的模块。导入/依赖:外部:testcontainers；内部:无；本地:无。导出:N8nImagePullPolicy。关键函数/方法:shouldPull。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (containers harness) -> tests/fixtures/containers
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/containers/n8n-image-pull-policy.ts -> services/n8n/tests/testing/fixtures/containers/n8n_image_pull_policy.py

import type { ImagePullPolicy } from 'testcontainers';
import { PullPolicy } from 'testcontainers';

/**
 * Custom pull policy for n8n images:
 * - Never try to pull the local image
 * - Otherwise, use the default pull policy (pull only if not present)
 */
export class N8nImagePullPolicy implements ImagePullPolicy {
	constructor(private readonly image: string) {}

	shouldPull(): boolean {
		if (this.image === 'n8nio/n8n:local') {
			return false;
		}

		return PullPolicy.defaultPolicy().shouldPull();
	}
}

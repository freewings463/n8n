"""
MIGRATION-META:
  source_path: packages/testing/containers/docker-image.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/containers 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:getDockerImageFromEnv。关键函数/方法:getDockerImageFromEnv。用于承载该模块实现细节，并通过导出对外提供能力。注释目标:Get the Docker image to use for the n8n container。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (containers harness) -> tests/fixtures/containers
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/containers/docker-image.ts -> services/n8n/tests/testing/fixtures/containers/docker_image.py

/**
 * Get the Docker image to use for the n8n container
 */
export function getDockerImageFromEnv(defaultImage = 'n8nio/n8n:local') {
	const configuredImage = process.env.N8N_DOCKER_IMAGE;
	if (!configuredImage) {
		return defaultImage;
	}

	const hasImageOrg = configuredImage.includes('/');
	const hasImageTag = configuredImage.includes(':');

	// Full image reference with org and tag (e.g., "n8nio/n8n:beta")
	if (hasImageOrg && hasImageTag) {
		return configuredImage;
	}

	// Image with org but no tag (e.g., "n8nio/n8n")
	if (hasImageOrg) {
		return configuredImage;
	}

	// Image with tag provided (e.g., "n8n:beta")
	if (hasImageTag) {
		return `n8nio/${configuredImage}`;
	}

	// Only tag name (e.g., "beta", "1.0.0")
	return `n8nio/n8n:${configuredImage}`;
}

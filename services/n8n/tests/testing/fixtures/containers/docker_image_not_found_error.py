"""
MIGRATION-META:
  source_path: packages/testing/containers/docker-image-not-found-error.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/containers 的错误。导入/依赖:外部:无；内部:无；本地:./docker-image。导出:DockerImageNotFoundError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (containers harness) -> tests/fixtures/containers
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/containers/docker-image-not-found-error.ts -> services/n8n/tests/testing/fixtures/containers/docker_image_not_found_error.py

import { getDockerImageFromEnv } from './docker-image';

// Custom error class for when the Docker image is not found locally/remotely
// This can happen when using the "n8nio/n8n:local" image, which is not available on Docker Hub
// This image is available after running `pnpm build:docker` at the root of the repository
export class DockerImageNotFoundError extends Error {
	constructor(containerName: string, originalError?: Error) {
		const dockerImage = getDockerImageFromEnv();

		const message = `Failed to start container ${containerName}: Docker image '${dockerImage}' not found locally!

This is likely because the image is not available locally.
To fix this, you can either:
  1. Build the image by running: pnpm build:docker at the root
  2. Use a different image by setting: N8N_DOCKER_IMAGE=<image-tag>

Example with different image:
  N8N_DOCKER_IMAGE=n8nio/n8n:latest npm run stack`;

		super(message);
		this.name = 'DockerImageNotFoundError';
		this.cause = originalError;
	}
}

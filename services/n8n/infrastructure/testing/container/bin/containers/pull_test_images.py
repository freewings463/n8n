"""
MIGRATION-META:
  source_path: packages/testing/containers/pull-test-images.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/containers 的模块。导入/依赖:外部:无；内部:无；本地:./test-containers。导出:无。关键函数/方法:execSync、duration、totalTime。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected child_process execution -> infrastructure/container/bin
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/containers/pull-test-images.ts -> services/n8n/infrastructure/testing/container/bin/containers/pull_test_images.py

#!/usr/bin/env tsx
/**
 * Script to pre-pull all test container images.
 */

import { execSync } from 'child_process';

import { TEST_CONTAINER_IMAGES } from './test-containers';

console.log('🐳 Pre-pulling test container images...');
const startTime = Date.now();
const timings = [];
const images = Object.values(TEST_CONTAINER_IMAGES);

for (const image of images) {
	// Skip :local tagged images - these are locally built and won't exist in any registry
	if (image.endsWith(':local')) {
		console.log(`\n⏭️  Skipping ${image} (local build)`);
		continue;
	}

	const imageStart = Date.now();
	console.log(`\nPulling ${image}...`);
	try {
		execSync(`docker pull ${image}`, { stdio: 'inherit' });
		const duration = ((Date.now() - imageStart) / 1000).toFixed(1);
		timings.push({ image, duration, success: true });
		console.log(`✅ Successfully pulled ${image} (${duration}s)`);
	} catch {
		const duration = ((Date.now() - imageStart) / 1000).toFixed(1);
		timings.push({ image, duration, success: false });
		console.error(`❌ Failed to pull ${image} (${duration}s)`);
		if (process.env.STRICT_IMAGE_PULL === 'true') process.exit(1);
	}
}

const totalTime = ((Date.now() - startTime) / 1000).toFixed(1);
console.log('\n' + '='.repeat(50));
console.log('📊 Pull Summary:');
timings.forEach(({ image, duration, success }) => {
	console.log(`  ${success ? '✅' : '❌'} ${image}: ${duration}s`);
});
console.log('='.repeat(50));
console.log(`✅ Total time: ${totalTime}s`);

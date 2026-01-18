"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/scenarios/multiple-webhooks/multiple-webhooks.script.js
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/scenarios/multiple-webhooks 的模块。导入/依赖:外部:k6/http、k6；内部:无；本地:无。导出:无。关键函数/方法:check。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Benchmark scenarios -> tests/functional/benchmarks/scenarios
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/scenarios/multiple-webhooks/multiple-webhooks.script.js -> services/n8n/tests/n8n-benchmark/functional/benchmarks/scenarios/multiple-webhooks/multiple_webhooks_script.py

import http from 'k6/http';
import { check } from 'k6';

const apiBaseUrl = __ENV.API_BASE_URL;

export default function () {
	const urls = Array(10)
		.fill()
		.map((_, i) => `${apiBaseUrl}/webhook/multiple-webhook${i + 1}`);

	const res = http.batch(urls);

	for (let i = 0; i < res.length; i++) {
		// Check if the response status is 200
		check(res[i], {
			'is status 200': (r) => r.status === 200,
		});
	}
}

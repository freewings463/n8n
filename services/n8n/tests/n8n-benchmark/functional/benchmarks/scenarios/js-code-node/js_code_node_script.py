"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/scenarios/js-code-node/js-code-node.script.js
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/scenarios/js-code-node 的模块。导入/依赖:外部:k6/http、k6；内部:无；本地:无。导出:无。关键函数/方法:check。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Benchmark scenarios -> tests/functional/benchmarks/scenarios
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/scenarios/js-code-node/js-code-node.script.js -> services/n8n/tests/n8n-benchmark/functional/benchmarks/scenarios/js-code-node/js_code_node_script.py

import http from 'k6/http';
import { check } from 'k6';

const apiBaseUrl = __ENV.API_BASE_URL;

export default function () {
	const res = http.post(`${apiBaseUrl}/webhook/code-node-benchmark`, {});

	if (res.status !== 200) {
		console.error(
			`Invalid response. Received status ${res.status}. Body: ${JSON.stringify(res.body)}`,
		);
	}

	check(res, {
		'is status 200': (r) => r.status === 200,
		'has items in response': (r) => {
			if (r.status !== 200) return false;

			try {
				const body = JSON.parse(r.body);
				return Array.isArray(body) ? body.length === 100 : false;
			} catch (error) {
				console.error('Error parsing response body: ', error);
				return false;
			}
		},
	});
}

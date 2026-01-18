"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/scenarios/binary-data/binary-data.script.js
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/scenarios/binary-data 的模块。导入/依赖:外部:k6/http、k6；内部:无；本地:无。导出:无。关键函数/方法:check。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Benchmark scenarios -> tests/functional/benchmarks/scenarios
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/scenarios/binary-data/binary-data.script.js -> services/n8n/tests/n8n-benchmark/functional/benchmarks/scenarios/binary-data/binary_data_script.py

import http from 'k6/http';
import { check } from 'k6';

const apiBaseUrl = __ENV.API_BASE_URL;

// This creates a 2MB file (16 * 128 * 1024 = 2 * 1024 * 1024 = 2MB)
const file = Array.from({ length: 128 * 1024 }, () => Math.random().toString().slice(2)).join('');
const filename = 'test.bin';

export default function () {
	const data = {
		filename,
		file: http.file(file, filename, 'application/javascript'),
	};

	const res = http.post(`${apiBaseUrl}/webhook/binary-files-benchmark`, data);

	if (res.status !== 200) {
		console.error(
			`Invalid response. Received status ${res.status}. Body: ${JSON.stringify(res.body)}`,
		);
	}

	check(res, {
		'is status 200': (r) => r.status === 200,
		'has correct content type': (r) =>
			r.headers['Content-Type'] === 'application/javascript; charset=utf-8',
	});
}

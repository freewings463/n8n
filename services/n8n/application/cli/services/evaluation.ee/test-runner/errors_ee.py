"""
MIGRATION-META:
  source_path: packages/cli/src/evaluation.ee/test-runner/errors.ee.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/evaluation.ee/test-runner 的模块。导入/依赖:外部:无；内部:@n8n/db、n8n-workflow；本地:无。导出:TestCaseExecutionError、TestRunError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/evaluation.ee/test-runner/errors.ee.ts -> services/n8n/application/cli/services/evaluation.ee/test-runner/errors_ee.py

import type { TestCaseExecutionErrorCode, TestRunErrorCode } from '@n8n/db';
import { UnexpectedError } from 'n8n-workflow';

export class TestCaseExecutionError extends UnexpectedError {
	readonly code: TestCaseExecutionErrorCode;

	constructor(code: TestCaseExecutionErrorCode, extra: Record<string, unknown> = {}) {
		super('Test Case execution failed with code ' + code, { extra });

		this.code = code;
	}
}

export class TestRunError extends UnexpectedError {
	readonly code: TestRunErrorCode;

	constructor(code: TestRunErrorCode, extra: Record<string, unknown> = {}) {
		super('Test Run failed with code ' + code, { extra });

		this.code = code;
	}
}

"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/mcp.errors.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/mcp 的模块。导入/依赖:外部:无；内部:@n8n/constants、n8n-workflow、@/errors/…/auth.error；本地:无。导出:McpExecutionTimeoutError、JWTVerificationError、AccessTokenNotFoundError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/mcp.errors.ts -> services/n8n/application/cli/services/modules/mcp/mcp_errors.py

import { Time } from '@n8n/constants';
import { UserError } from 'n8n-workflow';

import { AuthError } from '@/errors/response-errors/auth.error';

/**
 * Error thrown when MCP workflow execution times out
 */
export class McpExecutionTimeoutError extends UserError {
	executionId: string | null;
	timeoutMs: number;

	constructor(executionId: string | null, timeoutMs: number) {
		const timeoutSeconds = timeoutMs / Time.milliseconds.toSeconds;
		super(`Workflow execution timed out after ${timeoutSeconds} seconds`);

		this.name = 'McpExecutionTimeoutError';
		this.executionId = executionId;
		this.timeoutMs = timeoutMs;
	}
}

export class JWTVerificationError extends AuthError {
	constructor() {
		super('JWT Verification Failed');
		this.name = 'JWTVerificationError';
	}
}

export class AccessTokenNotFoundError extends AuthError {
	constructor() {
		super('Access Token Not Found in Database');
		this.name = 'AccessTokenNotFoundError';
	}
}

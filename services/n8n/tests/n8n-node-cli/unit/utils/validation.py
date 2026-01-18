"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/utils/validation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:validateNodeName、isNodeErrnoException、isEnoentError。关键函数/方法:validateNodeName、isNodeErrnoException、isEnoentError。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/utils/validation.ts -> services/n8n/tests/n8n-node-cli/unit/utils/validation.py

export const validateNodeName = (name: string): string | undefined => {
	if (!name) return;

	// 1. Matches '@org/n8n-nodes-anything'
	const regexScoped = /^@([a-z0-9]+(?:-[a-z0-9]+)*)\/n8n-nodes-([a-z0-9]+(?:-[a-z0-9]+)*)$/;
	// 2. Matches 'n8n-nodes-anything'
	const regexUnscoped = /^n8n-nodes-([a-z0-9]+(?:-[a-z0-9]+)*)$/;

	if (!regexScoped.test(name) && !regexUnscoped.test(name)) {
		return "Must start with 'n8n-nodes-' or '@org/n8n-nodes-'. Examples: n8n-nodes-my-app, @mycompany/n8n-nodes-my-app";
	}
	return;
};

export function isNodeErrnoException(error: unknown): error is NodeJS.ErrnoException {
	return error instanceof Error && 'code' in error;
}

export function isEnoentError(error: unknown): boolean {
	return isNodeErrnoException(error) && error.code === 'ENOENT';
}

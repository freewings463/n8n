"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Git/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Git 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:validateGitReference。关键函数/方法:validateGitReference。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Git/GenericFunctions.ts -> services/n8n/tests/nodes-base/unit/nodes/Git/GenericFunctions.py

import type { INode } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

/**
 * Validates a git reference to prevent command injection attacks
 * @param reference - The git reference to validate (e.g., branch name, HEAD, refs/heads/main)
 * @param node - The node instance for error throwing
 * @throws {NodeOperationError} If the reference contains unsafe characters or patterns
 */
export function validateGitReference(reference: string, node: INode): void {
	// Allow only safe characters: alphanumeric, /, @, {, }, ., -, _, :
	const safeReferencePattern = /^[a-zA-Z0-9/@{}._:-]+$/;

	if (!safeReferencePattern.test(reference)) {
		throw new NodeOperationError(
			node,
			'Invalid reference format. Reference contains unsafe characters. Only alphanumeric characters and /@{}._:- are allowed',
		);
	}

	// Prevent argument injection by blocking references starting with -
	if (reference.startsWith('-')) {
		throw new NodeOperationError(
			node,
			'Invalid reference format. Reference cannot start with a hyphen',
		);
	}

	// Prevent path traversal attempts
	if (reference.includes('..')) {
		throw new NodeOperationError(node, 'Invalid reference format. Reference cannot contain ".."');
	}

	// Prevent control characters that could be used for injection
	// eslint-disable-next-line no-control-regex
	if (/[\x00-\x1f\x7f]/.test(reference)) {
		throw new NodeOperationError(
			node,
			'Invalid reference format. Reference cannot contain control characters',
		);
	}
}

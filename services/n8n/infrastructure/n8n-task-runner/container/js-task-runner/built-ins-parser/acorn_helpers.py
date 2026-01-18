"""
MIGRATION-META:
  source_path: packages/@n8n/task-runner/src/js-task-runner/built-ins-parser/acorn-helpers.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/task-runner/src/js-task-runner/built-ins-parser 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:isLiteral、isIdentifier、isMemberExpression、isVariableDeclarator、isAssignmentExpression。关键函数/方法:isLiteral、isIdentifier、isMemberExpression、isVariableDeclarator、isAssignmentExpression。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Task runner process runtime -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/task-runner/src/js-task-runner/built-ins-parser/acorn-helpers.ts -> services/n8n/infrastructure/n8n-task-runner/container/js-task-runner/built-ins-parser/acorn_helpers.py

import type {
	AssignmentExpression,
	Identifier,
	Literal,
	MemberExpression,
	Node,
	VariableDeclarator,
} from 'acorn';

export function isLiteral(node?: Node): node is Literal {
	return node?.type === 'Literal';
}

export function isIdentifier(node?: Node): node is Identifier {
	return node?.type === 'Identifier';
}

export function isMemberExpression(node?: Node): node is MemberExpression {
	return node?.type === 'MemberExpression';
}

export function isVariableDeclarator(node?: Node): node is VariableDeclarator {
	return node?.type === 'VariableDeclarator';
}

export function isAssignmentExpression(node?: Node): node is AssignmentExpression {
	return node?.type === 'AssignmentExpression';
}

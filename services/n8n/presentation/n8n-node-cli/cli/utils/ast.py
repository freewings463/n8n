"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/utils/ast.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/node-cli/src/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:loadSingleSourceFile、updateStringProperty、getChildObjectLiteral。关键函数/方法:loadSingleSourceFile、setStringInitializer、updateStringProperty、getChildObjectLiteral。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI package default -> presentation/cli
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/utils/ast.ts -> services/n8n/presentation/n8n-node-cli/cli/utils/ast.py

import {
	Project,
	SyntaxKind,
	type ClassDeclaration,
	type ObjectLiteralExpression,
	type PropertyAssignment,
	type PropertyDeclaration,
} from 'ts-morph';

export const loadSingleSourceFile = (path: string) => {
	const project = new Project({
		skipFileDependencyResolution: true,
	});

	return project.addSourceFileAtPath(path);
};

const setStringInitializer = (prop: PropertyAssignment | PropertyDeclaration, value: string) => {
	prop.getInitializerIfKindOrThrow(SyntaxKind.StringLiteral).setLiteralValue(value);
};

export const updateStringProperty = ({
	obj,
	key,
	value,
}: { obj: ObjectLiteralExpression | ClassDeclaration; key: string; value: string }) => {
	const prop = obj.getPropertyOrThrow(key);

	if (prop.isKind(SyntaxKind.PropertyAssignment)) {
		setStringInitializer(prop.asKindOrThrow(SyntaxKind.PropertyAssignment), value);
	} else if (prop.isKind(SyntaxKind.PropertyDeclaration)) {
		setStringInitializer(prop.asKindOrThrow(SyntaxKind.PropertyDeclaration), value);
	}
};

export const getChildObjectLiteral = ({
	obj,
	key,
}: { obj: ObjectLiteralExpression; key: string }) => {
	return obj
		.getPropertyOrThrow(key)
		.asKindOrThrow(SyntaxKind.PropertyAssignment)
		.getInitializerIfKindOrThrow(SyntaxKind.ObjectLiteralExpression);
};

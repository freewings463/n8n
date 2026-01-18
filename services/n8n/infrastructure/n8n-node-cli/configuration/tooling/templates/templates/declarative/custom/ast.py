"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/declarative/custom/ast.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/declarative 的模块。导入/依赖:外部:change-case、ts-morph；内部:无；本地:无。导出:updateNodeAst、updateCredentialAst、addCredentialToNode。关键函数/方法:updateNodeAst、updateStringProperty、updateCredentialAst、addCredentialToNode。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/declarative/custom/ast.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/declarative/custom/ast.py

import { camelCase, capitalCase } from 'change-case';
import { ts, SyntaxKind, printNode } from 'ts-morph';

import {
	getChildObjectLiteral,
	loadSingleSourceFile,
	updateStringProperty,
} from '../../../../utils/ast';

export function updateNodeAst({
	nodePath,
	className,
	baseUrl,
}: { nodePath: string; className: string; baseUrl: string }) {
	const sourceFile = loadSingleSourceFile(nodePath);
	const classDecl = sourceFile.getClasses()[0];

	classDecl.rename(className);
	const nodeDescriptionObj = classDecl
		.getPropertyOrThrow('description')
		.getInitializerIfKindOrThrow(SyntaxKind.ObjectLiteralExpression);

	updateStringProperty({
		obj: nodeDescriptionObj,
		key: 'displayName',
		value: capitalCase(className),
	});
	updateStringProperty({
		obj: nodeDescriptionObj,
		key: 'name',
		value: camelCase(className),
	});
	updateStringProperty({
		obj: nodeDescriptionObj,
		key: 'description',
		value: `Interact with the ${capitalCase(className)} API`,
	});

	const icon = getChildObjectLiteral({ obj: nodeDescriptionObj, key: 'icon' });
	updateStringProperty({
		obj: icon,
		key: 'light',
		value: `file:${camelCase(className)}.svg`,
	});
	updateStringProperty({
		obj: icon,
		key: 'dark',
		value: `file:${camelCase(className)}.dark.svg`,
	});

	const requestDefaults = getChildObjectLiteral({
		obj: nodeDescriptionObj,
		key: 'requestDefaults',
	});

	updateStringProperty({
		obj: requestDefaults,
		key: 'baseURL',
		value: baseUrl,
	});

	const defaults = getChildObjectLiteral({
		obj: nodeDescriptionObj,
		key: 'defaults',
	});

	updateStringProperty({ obj: defaults, key: 'name', value: capitalCase(className) });

	return sourceFile;
}

export function updateCredentialAst({
	repoName,
	baseUrl,
	credentialPath,
	credentialName,
	credentialDisplayName,
	credentialClassName,
}: {
	repoName: string;
	credentialPath: string;
	credentialName: string;
	credentialDisplayName: string;
	credentialClassName: string;
	baseUrl: string;
}) {
	const sourceFile = loadSingleSourceFile(credentialPath);
	const classDecl = sourceFile.getClasses()[0];

	classDecl.rename(credentialClassName);

	updateStringProperty({
		obj: classDecl,
		key: 'displayName',
		value: credentialDisplayName,
	});

	updateStringProperty({
		obj: classDecl,
		key: 'name',
		value: credentialName,
	});

	const docUrlProp = classDecl.getProperty('documentationUrl');
	if (docUrlProp) {
		const initializer = docUrlProp.getInitializerIfKindOrThrow(SyntaxKind.StringLiteral);
		const newUrl = initializer.getLiteralText().replace('/repo', `/${repoName}`);
		initializer.setLiteralValue(newUrl);
	}

	const testProperty = classDecl.getProperty('test');

	if (testProperty) {
		const testRequest = testProperty
			.getInitializerIfKindOrThrow(SyntaxKind.ObjectLiteralExpression)
			.getPropertyOrThrow('request')
			.asKindOrThrow(SyntaxKind.PropertyAssignment)
			.getInitializerIfKindOrThrow(SyntaxKind.ObjectLiteralExpression);

		updateStringProperty({
			obj: testRequest,
			key: 'baseURL',
			value: baseUrl,
		});
	}

	return sourceFile;
}

export function addCredentialToNode({
	nodePath,
	credentialName,
}: { nodePath: string; credentialName: string }) {
	const sourceFile = loadSingleSourceFile(nodePath);
	const classDecl = sourceFile.getClasses()[0];

	const descriptionProp = classDecl
		.getPropertyOrThrow('description')
		.getInitializerIfKindOrThrow(SyntaxKind.ObjectLiteralExpression);

	const credentialsProp = descriptionProp.getPropertyOrThrow('credentials');

	if (credentialsProp.getKind() === SyntaxKind.PropertyAssignment) {
		const initializer = credentialsProp.getFirstDescendantByKindOrThrow(
			SyntaxKind.ArrayLiteralExpression,
		);
		const credentialObject = ts.factory.createObjectLiteralExpression([
			ts.factory.createPropertyAssignment(
				ts.factory.createIdentifier('name'),
				ts.factory.createStringLiteral(credentialName, true),
			),
			ts.factory.createPropertyAssignment(
				ts.factory.createIdentifier('required'),
				ts.factory.createTrue(),
			),
		]);
		initializer.addElement(printNode(credentialObject));
	}

	return sourceFile;
}

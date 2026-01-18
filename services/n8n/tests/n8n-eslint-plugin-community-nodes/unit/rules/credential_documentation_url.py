"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-plugin-community-nodes/src/rules/credential-documentation-url.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-plugin-community-nodes/src/rules 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:CredentialDocumentationUrlRule。关键函数/方法:create、isValidUrl、isValidSlug、hasOnlyCaseIssues、validateDocumentationUrl、getExpectedFormatsMessage、ClassDeclaration。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-plugin-community-nodes/src/rules/credential-documentation-url.ts -> services/n8n/tests/n8n-eslint-plugin-community-nodes/unit/rules/credential_documentation_url.py

import {
	isCredentialTypeClass,
	findClassProperty,
	getStringLiteralValue,
	createRule,
} from '../utils/index.js';

type RuleOptions = {
	allowUrls?: boolean;
	allowSlugs?: boolean;
};

const DEFAULT_OPTIONS: RuleOptions = {
	allowUrls: true,
	allowSlugs: false,
};

function isValidUrl(value: string): boolean {
	try {
		new URL(value);
		return true;
	} catch {
		return false;
	}
}

function isValidSlug(value: string): boolean {
	// TODO: Remove this special case once these slugs are updated
	if (
		['google/service-account', 'google/oauth-single-service', 'google/oauth-generic'].includes(
			value,
		)
	)
		return true;

	return value.split('/').every((segment) => /^[a-z][a-z0-9]*$/.test(segment));
}

function hasOnlyCaseIssues(value: string): boolean {
	return value.split('/').every((segment) => /^[a-zA-Z][a-zA-Z0-9]*$/.test(segment));
}

function validateDocumentationUrl(value: string, options: RuleOptions): boolean {
	return (!!options.allowUrls && isValidUrl(value)) || (!!options.allowSlugs && isValidSlug(value));
}

function getExpectedFormatsMessage(options: RuleOptions): string {
	const formats = [
		...(options.allowUrls ? ['a valid URL'] : []),
		...(options.allowSlugs ? ['a lowercase alphanumeric slug (can contain slashes)'] : []),
	];

	if (formats.length === 0) return 'a valid format (none configured)';
	if (formats.length === 1) return formats[0]!;
	return formats.slice(0, -1).join(', ') + ' or ' + formats[formats.length - 1];
}

export const CredentialDocumentationUrlRule = createRule({
	name: 'credential-documentation-url',
	meta: {
		type: 'problem',
		docs: {
			description:
				'Enforce valid credential documentationUrl format (URL or lowercase alphanumeric slug)',
		},
		messages: {
			invalidDocumentationUrl: "documentationUrl '{{ value }}' must be {{ expectedFormats }}",
		},
		fixable: 'code',
		schema: [
			{
				type: 'object',
				properties: {
					allowUrls: {
						type: 'boolean',
						description: 'Whether to allow valid URLs',
					},
					allowSlugs: {
						type: 'boolean',
						description: 'Whether to allow lowercase alphanumeric slugs with slashes',
					},
				},
				additionalProperties: false,
			},
		],
	},
	defaultOptions: [DEFAULT_OPTIONS],
	create(context, [options = {}]) {
		const mergedOptions = { ...DEFAULT_OPTIONS, ...options };

		return {
			ClassDeclaration(node) {
				if (!isCredentialTypeClass(node)) {
					return;
				}

				const documentationUrlProperty = findClassProperty(node, 'documentationUrl');
				if (!documentationUrlProperty?.value) {
					return;
				}

				const documentationUrl = getStringLiteralValue(documentationUrlProperty.value);
				if (documentationUrl === null) {
					return;
				}

				if (!validateDocumentationUrl(documentationUrl, mergedOptions)) {
					const canAutofix = !!mergedOptions.allowSlugs && hasOnlyCaseIssues(documentationUrl);

					context.report({
						node: documentationUrlProperty.value,
						messageId: 'invalidDocumentationUrl',
						data: {
							value: documentationUrl,
							expectedFormats: getExpectedFormatsMessage(mergedOptions),
						},
						fix: canAutofix
							? (fixer) =>
									fixer.replaceText(
										documentationUrlProperty.value!,
										`'${documentationUrl.toLowerCase()}'`,
									)
							: undefined,
					});
				}
			},
		};
	},
});

"""
MIGRATION-META:
  source_path: packages/@n8n/permissions/src/scope-information.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/permissions/src 的模块。导入/依赖:外部:无；内部:无；本地:./constants.ee、./types.ee。导出:ALL_SCOPES、ALL_API_KEY_SCOPES、scopeInformation。关键函数/方法:buildResourceScopes、buildApiKeyScopes。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/permissions treated as domain authorization policies
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/permissions/src/scope-information.ts -> services/n8n/domain/n8n-permissions/policies/scope_information.py

import { API_KEY_RESOURCES, RESOURCES } from './constants.ee';
import type { ApiKeyScope, Scope, ScopeInformation } from './types.ee';

function buildResourceScopes() {
	const resourceScopes = Object.entries(RESOURCES).flatMap(([resource, operations]) => [
		...operations.map((op) => `${resource}:${op}` as const),
		`${resource}:*` as const,
	]) as Scope[];

	resourceScopes.push('*' as const); // Global wildcard
	return resourceScopes;
}

function buildApiKeyScopes() {
	const apiKeyScopes = Object.entries(API_KEY_RESOURCES).flatMap(([resource, operations]) => [
		...operations.map((op) => `${resource}:${op}` as const),
	]) as ApiKeyScope[];

	return new Set(apiKeyScopes);
}

export const ALL_SCOPES = buildResourceScopes();

export const ALL_API_KEY_SCOPES = buildApiKeyScopes();

export const scopeInformation: Partial<Record<Scope, ScopeInformation>> = {
	'annotationTag:create': {
		displayName: 'Create Annotation Tag',
		description: 'Allows creating new annotation tags.',
	},
	'workflow:publish': {
		displayName: 'Publish Workflow',
		description: 'Allows publishing and unpublishing workflows.',
	},
};

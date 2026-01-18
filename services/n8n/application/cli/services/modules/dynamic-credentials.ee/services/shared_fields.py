"""
MIGRATION-META:
  source_path: packages/cli/src/modules/dynamic-credentials.ee/services/shared-fields.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/dynamic-credentials.ee/services 的服务。导入/依赖:外部:无；内部:@n8n/di、n8n-workflow、@/credential-types；本地:无。导出:extractSharedFields。关键函数/方法:getExtendedProps、extractSharedFields。用于封装该模块业务流程，对上提供稳定调用面。注释目标:By default all fields that are defined in the schema are considered static. / If a field is not defined in the schema, it is considered dynamic.。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/dynamic-credentials.ee/services/shared-fields.ts -> services/n8n/application/cli/services/modules/dynamic-credentials.ee/services/shared_fields.py

/**
 * By default all fields that are defined in the schema are considered static.
 * If a field is not defined in the schema, it is considered dynamic.
 * If a field is marked as dynamic in the schema it is considered dynamic.
 */
import { Container } from '@n8n/di';
import { NodeHelpers, type ICredentialType, type INodeProperties } from 'n8n-workflow';

import { CredentialTypes } from '@/credential-types';

// Build merged properties from credential hierarchy
function getExtendedProps(
	type: ICredentialType,
	credentialTypes: CredentialTypes,
): INodeProperties[] {
	const props: INodeProperties[] = [];

	// Recursively get parent properties first (bottom-up)
	for (const parentTypeName of type.extends ?? []) {
		const parentType = credentialTypes.getByName(parentTypeName);
		const parentProps = getExtendedProps(parentType, credentialTypes);
		NodeHelpers.mergeNodeProperties(props, parentProps);
	}

	// Merge current type's properties (child properties override parent)
	NodeHelpers.mergeNodeProperties(props, type.properties);

	return props;
}

export function extractSharedFields(credentialType: ICredentialType): string[] {
	const credentialTypes = Container.get(CredentialTypes);

	const mergedProperties = getExtendedProps(credentialType, credentialTypes);

	const sharedFields: string[] = [];

	for (const property of mergedProperties) {
		// If a field is not marked as resolvable, consider it static
		if (property.resolvableField !== true) {
			sharedFields.push(property.name);
		}
	}

	return sharedFields;
}

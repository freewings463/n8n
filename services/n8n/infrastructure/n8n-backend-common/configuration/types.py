"""
MIGRATION-META:
  source_path: packages/@n8n/backend-common/src/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/backend-common/src 的类型。导入/依赖:外部:无；内部:@n8n/constants；本地:无。导出:FeatureReturnType、LicenseProvider。关键函数/方法:isLicensed。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/backend-common treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/backend-common/src/types.ts -> services/n8n/infrastructure/n8n-backend-common/configuration/types.py

import type { BooleanLicenseFeature, NumericLicenseFeature } from '@n8n/constants';

export type FeatureReturnType = Partial<
	{
		planName: string;
	} & { [K in NumericLicenseFeature]: number } & { [K in BooleanLicenseFeature]: boolean }
>;

export interface LicenseProvider {
	/** Returns whether a feature is included in the user's license plan. */
	isLicensed(feature: BooleanLicenseFeature): boolean;

	/** Returns the value of a feature in the user's license plan, typically a boolean or integer. */
	getValue<T extends keyof FeatureReturnType>(feature: T): FeatureReturnType[T];
}

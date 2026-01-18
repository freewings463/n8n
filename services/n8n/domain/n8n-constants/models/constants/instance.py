"""
MIGRATION-META:
  source_path: packages/@n8n/constants/src/instance.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/constants/src 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:INSTANCE_ID_HEADER、INSTANCE_VERSION_HEADER、INSTANCE_TYPES、InstanceType、INSTANCE_ROLES、InstanceRole。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/constants treated as domain constants
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/constants/src/instance.ts -> services/n8n/domain/n8n-constants/models/constants/instance.py

export const INSTANCE_ID_HEADER = 'n8n-instance-id';
export const INSTANCE_VERSION_HEADER = 'n8n-version';

export const INSTANCE_TYPES = ['main', 'webhook', 'worker'] as const;
export type InstanceType = (typeof INSTANCE_TYPES)[number];

export const INSTANCE_ROLES = ['unset', 'leader', 'follower'] as const;
export type InstanceRole = (typeof INSTANCE_ROLES)[number];

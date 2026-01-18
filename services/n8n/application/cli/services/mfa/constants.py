"""
MIGRATION-META:
  source_path: packages/cli/src/mfa/constants.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/mfa 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:MFA_FEATURE_ENABLED、MFA_ENFORCE_SETTING。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/mfa/constants.ts -> services/n8n/application/cli/services/mfa/constants.py

export const MFA_FEATURE_ENABLED = 'mfa.enabled';
export const MFA_ENFORCE_SETTING = 'mfa.enforced';

"""
MIGRATION-META:
  source_path: packages/@n8n/utils/src/number/smartDecimal.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/utils/src/number 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:smartDecimal。关键函数/方法:smartDecimal。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Generic shared utilities -> application/services/utils
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/utils/src/number/smartDecimal.ts -> services/n8n/application/n8n-utils/services/utils/number/smartDecimal.py

export const smartDecimal = (value: number, decimals = 2): number => {
	// Check if integer
	if (Number.isInteger(value)) {
		return value;
	}

	// Check if it has only one decimal place
	if (value.toString().split('.')[1].length <= decimals) {
		return value;
	}

	return Number(value.toFixed(decimals));
};

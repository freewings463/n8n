"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/utils/validators/no-xss.validator.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/utils/validators 的工具。导入/依赖:外部:class-validator、xss；内部:无；本地:无。导出:NoXss。关键函数/方法:validate、xss、defaultMessage、NoXss、registerDecorator。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package @n8n/db defaulted to persistence infrastructure
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/utils/validators/no-xss.validator.ts -> services/n8n/infrastructure/n8n-db/persistence/utils/validators/no_xss_validator.py

import type { ValidationOptions, ValidatorConstraintInterface } from 'class-validator';
import { registerDecorator, ValidatorConstraint } from 'class-validator';
import xss from 'xss';

@ValidatorConstraint({ name: 'NoXss', async: false })
class NoXssConstraint implements ValidatorConstraintInterface {
	validate(value: unknown) {
		if (typeof value !== 'string') return false;

		return (
			value ===
			xss(value, {
				whiteList: {}, // no tags are allowed
			})
		);
	}

	defaultMessage() {
		return 'Potentially malicious string';
	}
}

export function NoXss(options?: ValidationOptions) {
	return function (object: object, propertyName: string) {
		registerDecorator({
			name: 'NoXss',
			target: object.constructor,
			propertyName,
			options,
			validator: NoXssConstraint,
		});
	};
}

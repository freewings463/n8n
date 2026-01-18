"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/utils/validators/no-url.validator.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/utils/validators 的工具。导入/依赖:外部:class-validator；内部:无；本地:无。导出:NoUrl。关键函数/方法:validate、defaultMessage、NoUrl、registerDecorator。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/utils/validators/no-url.validator.ts -> services/n8n/tests/n8n-db/unit/utils/validators/no_url_validator.py

import type { ValidationOptions, ValidatorConstraintInterface } from 'class-validator';
import { registerDecorator, ValidatorConstraint } from 'class-validator';

const URL_REGEX = /^(https?:\/\/|www\.)|(\.[\p{L}\d-]+)/iu;

@ValidatorConstraint({ name: 'NoUrl', async: false })
class NoUrlConstraint implements ValidatorConstraintInterface {
	validate(value: string) {
		return !URL_REGEX.test(value);
	}

	defaultMessage() {
		return 'Potentially malicious string';
	}
}

export function NoUrl(options?: ValidationOptions) {
	return function (object: object, propertyName: string) {
		registerDecorator({
			name: 'NoUrl',
			target: object.constructor,
			propertyName,
			options,
			validator: NoUrlConstraint,
		});
	};
}

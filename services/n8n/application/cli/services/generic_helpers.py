"""
MIGRATION-META:
  source_path: packages/cli/src/generic-helpers.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src 的工具。导入/依赖:外部:class-validator；内部:无；本地:./controllers/survey-answers.dto、../response-errors/bad-request.error。导出:DEFAULT_EXECUTIONS_GET_ALL_LIMIT。关键函数/方法:validateEntity。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/generic-helpers.ts -> services/n8n/application/cli/services/generic_helpers.py

import type {
	CredentialsEntity,
	User,
	WorkflowEntity,
	TagEntity,
	AnnotationTagEntity,
} from '@n8n/db';
import { validate } from 'class-validator';

import type { PersonalizationSurveyAnswersV4 } from './controllers/survey-answers.dto';
import { BadRequestError } from './errors/response-errors/bad-request.error';

export async function validateEntity(
	entity:
		| WorkflowEntity
		| CredentialsEntity
		| TagEntity
		| AnnotationTagEntity
		| User
		| PersonalizationSurveyAnswersV4,
): Promise<void> {
	const errors = await validate(entity);

	const errorMessages = errors
		.reduce<string[]>((acc, cur) => {
			if (!cur.constraints) return acc;
			acc.push(...Object.values(cur.constraints));
			return acc;
		}, [])
		.join(' | ');

	if (errorMessages) {
		throw new BadRequestError(errorMessages);
	}
}

export const DEFAULT_EXECUTIONS_GET_ALL_LIMIT = 20;

"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/user/user-update-request.dto.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/api-types/src/dto/user 的模块。导入/依赖:外部:xss、zod、zod-class；内部:无；本地:无。导出:UserUpdateRequestDto。关键函数/方法:xssCheck、xss、urlCheck、nameSchema。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/user/user-update-request.dto.ts -> services/n8n/tests/n8n-api-types/unit/dto/user/user_update_request_dto.py

import xss from 'xss';
import { z } from 'zod';
import { Z } from 'zod-class';

const xssCheck = (value: string) =>
	value ===
	xss(value, {
		whiteList: {}, // no tags are allowed
	});

const URL_REGEX = /^(https?:\/\/|www\.)|(\.[\p{L}\d-]+)/iu;
const urlCheck = (value: string) => !URL_REGEX.test(value);

const nameSchema = () =>
	z
		.string()
		.min(1)
		.max(32)
		.refine(xssCheck, {
			message: 'Potentially malicious string',
		})
		.refine(urlCheck, {
			message: 'Potentially malicious string',
		});

export class UserUpdateRequestDto extends Z.class({
	email: z.string().email(),
	firstName: nameSchema().optional(),
	lastName: nameSchema().optional(),
	mfaCode: z.string().optional(),
	/**
	 * The current password is required when changing the email address and MFA is disabled.
	 */
	currentPassword: z.string().optional(),
}) {}

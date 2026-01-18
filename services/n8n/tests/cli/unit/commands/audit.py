"""
MIGRATION-META:
  source_path: packages/cli/src/commands/audit.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/commands 的模块。导入/依赖:外部:zod；内部:@n8n/config、@n8n/decorators、@n8n/di、n8n-workflow、@/security-audit/constants、@/security-audit/types 等1项；本地:./base-command。导出:SecurityAudit。关键函数/方法:run。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/commands/audit.ts -> services/n8n/tests/cli/unit/commands/audit.py

import { SecurityConfig } from '@n8n/config';
import { Command } from '@n8n/decorators';
import { Container } from '@n8n/di';
import { UserError } from 'n8n-workflow';
import z from 'zod';

import { RISK_CATEGORIES } from '@/security-audit/constants';
import type { Risk } from '@/security-audit/types';

import { BaseCommand } from './base-command';

const flagsSchema = z.object({
	categories: z
		.string()
		.default(RISK_CATEGORIES.join(','))
		.describe('Comma-separated list of categories to include in the audit'),
	'days-abandoned-workflow': z
		.number()
		.int()
		.default(Container.get(SecurityConfig).daysAbandonedWorkflow)
		.describe('Days for a workflow to be considered abandoned if not executed'),
});

@Command({
	name: 'audit',
	description: 'Generate a security audit report for this n8n instance',
	examples: ['', '--categories=database,credentials', '--days-abandoned-workflow=10'],
	flagsSchema,
})
export class SecurityAudit extends BaseCommand<z.infer<typeof flagsSchema>> {
	async run() {
		const { flags: auditFlags } = this;
		const categories =
			auditFlags.categories?.split(',').filter((c): c is Risk.Category => c !== '') ??
			RISK_CATEGORIES;

		const invalidCategories = categories.filter((c) => !RISK_CATEGORIES.includes(c));

		if (invalidCategories.length > 0) {
			const message =
				invalidCategories.length > 1
					? `Invalid categories received: ${invalidCategories.join(', ')}`
					: `Invalid category received: ${invalidCategories[0]}`;

			const hint = `Valid categories are: ${RISK_CATEGORIES.join(', ')}`;

			throw new UserError([message, hint].join('. '));
		}

		const { SecurityAuditService } = await import('@/security-audit/security-audit.service');

		const result = await Container.get(SecurityAuditService).run(
			categories,
			auditFlags['days-abandoned-workflow'],
		);

		if (Array.isArray(result) && result.length === 0) {
			this.logger.info('No security issues found');
		} else {
			process.stdout.write(JSON.stringify(result, null, 2));
		}
	}

	async catch(error: Error) {
		this.logger.error('Failed to generate security audit');
		this.logger.error(error.message);
	}
}

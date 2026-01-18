"""
MIGRATION-META:
  source_path: packages/cli/src/security-audit/risk-reporters/credentials-risk-reporter.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/security-audit/risk-reporters 的模块。导入/依赖:外部:无；内部:@n8n/config、@n8n/db、@n8n/di、n8n-workflow、@/security-audit/constants、@/security-audit/types；本地:无。导出:CredentialsRiskReporter。关键函数/方法:report、sentenceStart、getAllCredsInUse、getAllExistingCreds、getExecutedWorkflowsInPastDays、getCredsInRecentlyExecutedWorkflows。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/security-audit/risk-reporters/credentials-risk-reporter.ts -> services/n8n/application/cli/services/security-audit/risk-reporters/credentials_risk_reporter.py

import { SecurityConfig } from '@n8n/config';
import { CredentialsRepository, ExecutionDataRepository, ExecutionRepository } from '@n8n/db';
import { Service } from '@n8n/di';
import type { IWorkflowBase } from 'n8n-workflow';

import { CREDENTIALS_REPORT } from '@/security-audit/constants';
import type { RiskReporter, Risk } from '@/security-audit/types';

@Service()
export class CredentialsRiskReporter implements RiskReporter {
	constructor(
		private readonly credentialsRepository: CredentialsRepository,
		private readonly executionRepository: ExecutionRepository,
		private readonly executionDataRepository: ExecutionDataRepository,
		private readonly securityConfig: SecurityConfig,
	) {}

	async report(workflows: IWorkflowBase[]) {
		const days = this.securityConfig.daysAbandonedWorkflow;

		const allExistingCreds = await this.getAllExistingCreds();
		const { credsInAnyUse, credsInActiveUse } = this.getAllCredsInUse(workflows);
		const recentlyExecutedCreds = await this.getCredsInRecentlyExecutedWorkflows(days);

		const credsNotInAnyUse = allExistingCreds.filter((c) => !credsInAnyUse.has(c.id));
		const credsNotInActiveUse = allExistingCreds.filter((c) => !credsInActiveUse.has(c.id));
		const credsNotRecentlyExecuted = allExistingCreds.filter(
			(c) => !recentlyExecutedCreds.has(c.id),
		);

		const issues = [credsNotInAnyUse, credsNotInActiveUse, credsNotRecentlyExecuted];

		if (issues.every((i) => i.length === 0)) return null;

		const report: Risk.StandardReport = {
			risk: CREDENTIALS_REPORT.RISK,
			sections: [],
		};

		const hint = 'Keeping unused credentials in your instance is an unneeded security risk.';
		const recommendation = 'Consider deleting these credentials if you no longer need them.';

		const sentenceStart = ({ length }: { length: number }) =>
			length > 1 ? 'These credentials are' : 'This credential is';

		if (credsNotInAnyUse.length > 0) {
			report.sections.push({
				title: CREDENTIALS_REPORT.SECTIONS.CREDS_NOT_IN_ANY_USE,
				description: [sentenceStart(credsNotInAnyUse), 'not used in any workflow.', hint].join(' '),
				recommendation,
				location: credsNotInAnyUse,
			});
		}

		if (credsNotInActiveUse.length > 0) {
			report.sections.push({
				title: CREDENTIALS_REPORT.SECTIONS.CREDS_NOT_IN_ACTIVE_USE,
				description: [
					sentenceStart(credsNotInActiveUse),
					'not used in active workflows.',
					hint,
				].join(' '),
				recommendation,
				location: credsNotInActiveUse,
			});
		}

		if (credsNotRecentlyExecuted.length > 0) {
			report.sections.push({
				title: CREDENTIALS_REPORT.SECTIONS.CREDS_NOT_RECENTLY_EXECUTED,
				description: [
					sentenceStart(credsNotRecentlyExecuted),
					`not used in recently executed workflows, i.e. workflows executed in the past ${days} days.`,
					hint,
				].join(' '),
				recommendation,
				location: credsNotRecentlyExecuted,
			});
		}

		return report;
	}

	private getAllCredsInUse(workflows: IWorkflowBase[]) {
		const credsInAnyUse = new Set<string>();
		const credsInActiveUse = new Set<string>();

		workflows.forEach((workflow) => {
			workflow.nodes.forEach((node) => {
				if (!node.credentials) return;

				Object.values(node.credentials).forEach((cred) => {
					if (!cred?.id) return;

					credsInAnyUse.add(cred.id);

					if (workflow.activeVersionId !== null) {
						credsInActiveUse.add(cred.id);
					}
				});
			});
		});

		return {
			credsInAnyUse,
			credsInActiveUse,
		};
	}

	private async getAllExistingCreds() {
		const credentials = await this.credentialsRepository.find({ select: ['id', 'name'] });

		return credentials.map(({ id, name }) => ({ kind: 'credential' as const, id, name }));
	}

	private async getExecutedWorkflowsInPastDays(days: number): Promise<IWorkflowBase[]> {
		const date = new Date();

		date.setDate(date.getDate() - days);

		const executionIds = await this.executionRepository.getIdsSince(date);

		return await this.executionDataRepository.findByExecutionIds(executionIds);
	}

	/**
	 * Return IDs of credentials in workflows executed in the past n days.
	 */
	private async getCredsInRecentlyExecutedWorkflows(days: number) {
		const executedWorkflows = await this.getExecutedWorkflowsInPastDays(days);

		return executedWorkflows.reduce<Set<string>>((acc, { nodes }) => {
			nodes.forEach((node) => {
				if (node.credentials) {
					Object.values(node.credentials).forEach((c) => {
						if (c.id) acc.add(c.id);
					});
				}
			});

			return acc;
		}, new Set());
	}
}

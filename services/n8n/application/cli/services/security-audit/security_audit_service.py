"""
MIGRATION-META:
  source_path: packages/cli/src/security-audit/security-audit.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/security-audit 的服务。导入/依赖:外部:无；内部:@n8n/config、@n8n/db、@n8n/di、@/config、@/security-audit/constants、@/security-audit/types 等1项；本地:无。导出:SecurityAuditService。关键函数/方法:run、reports、initReporters。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/security-audit/security-audit.service.ts -> services/n8n/application/cli/services/security-audit/security_audit_service.py

import { SecurityConfig } from '@n8n/config';
import { WorkflowRepository } from '@n8n/db';
import { Container, Service } from '@n8n/di';

import config from '@/config';
import { RISK_CATEGORIES } from '@/security-audit/constants';
import type { Risk, RiskReporter } from '@/security-audit/types';
import { toReportTitle } from '@/security-audit/utils';

@Service()
export class SecurityAuditService {
	constructor(
		private readonly workflowRepository: WorkflowRepository,
		private readonly securityConfig: SecurityConfig,
	) {}

	private reporters: {
		[name: string]: RiskReporter;
	} = {};

	async run(categories: Risk.Category[] = RISK_CATEGORIES, daysAbandonedWorkflow?: number) {
		if (categories.length === 0) categories = RISK_CATEGORIES;

		await this.initReporters(categories);

		const daysFromEnv = this.securityConfig.daysAbandonedWorkflow;

		if (daysAbandonedWorkflow) {
			config.set('security.audit.daysAbandonedWorkflow', daysAbandonedWorkflow);
		}

		const workflows = await this.workflowRepository.find({
			select: ['id', 'name', 'active', 'activeVersionId', 'nodes', 'connections'],
		});

		const promises = categories.map(async (c) => await this.reporters[c].report(workflows));

		const reports = (await Promise.all(promises)).filter((r): r is Risk.Report => r !== null);

		if (daysAbandonedWorkflow) {
			config.set('security.audit.daysAbandonedWorkflow', daysFromEnv); // restore env
		}

		if (reports.length === 0) return []; // trigger empty state

		return reports.reduce<Risk.Audit>((acc, cur) => {
			acc[toReportTitle(cur.risk)] = cur;

			return acc;
		}, {});
	}

	async initReporters(categories: Risk.Category[]) {
		for (const category of categories) {
			const className = category.charAt(0).toUpperCase() + category.slice(1) + 'RiskReporter';

			const toFilename: Record<string, string> = {
				CredentialsRiskReporter: 'credentials-risk-reporter',
				DatabaseRiskReporter: 'database-risk-reporter',
				FilesystemRiskReporter: 'filesystem-risk-reporter',
				InstanceRiskReporter: 'instance-risk-reporter',
				NodesRiskReporter: 'nodes-risk-reporter',
			};

			// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
			const RiskReporterModule = await import(`./risk-reporters/${toFilename[className]}`);

			// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
			const RiskReporterClass = RiskReporterModule[className] as { new (): RiskReporter };

			this.reporters[category] = Container.get(RiskReporterClass);
		}
	}
}

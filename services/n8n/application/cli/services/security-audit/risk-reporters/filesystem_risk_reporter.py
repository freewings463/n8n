"""
MIGRATION-META:
  source_path: packages/cli/src/security-audit/risk-reporters/filesystem-risk-reporter.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/security-audit/risk-reporters 的模块。导入/依赖:外部:无；内部:@n8n/di、n8n-workflow、@/security-audit/constants、@/security-audit/types、@/security-audit/utils；本地:无。导出:FilesystemRiskReporter。关键函数/方法:report、sentenceStart。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/security-audit/risk-reporters/filesystem-risk-reporter.ts -> services/n8n/application/cli/services/security-audit/risk-reporters/filesystem_risk_reporter.py

import { Service } from '@n8n/di';
import type { IWorkflowBase } from 'n8n-workflow';

import { FILESYSTEM_INTERACTION_NODE_TYPES, FILESYSTEM_REPORT } from '@/security-audit/constants';
import type { RiskReporter, Risk } from '@/security-audit/types';
import { getNodeTypes } from '@/security-audit/utils';

@Service()
export class FilesystemRiskReporter implements RiskReporter {
	async report(workflows: IWorkflowBase[]) {
		const fsInteractionNodeTypes = getNodeTypes(workflows, (node) =>
			FILESYSTEM_INTERACTION_NODE_TYPES.has(node.type),
		);

		if (fsInteractionNodeTypes.length === 0) return null;

		const report: Risk.StandardReport = {
			risk: FILESYSTEM_REPORT.RISK,
			sections: [],
		};

		const sentenceStart = ({ length }: { length: number }) =>
			length > 1 ? 'These nodes read from and write to' : 'This node reads from and writes to';

		if (fsInteractionNodeTypes.length > 0) {
			report.sections.push({
				title: FILESYSTEM_REPORT.SECTIONS.FILESYSTEM_INTERACTION_NODES,
				description: [
					sentenceStart(fsInteractionNodeTypes),
					'any accessible file in the host filesystem. Sensitive file content may be manipulated through a node operation.',
				].join(' '),
				recommendation:
					'Consider protecting any sensitive files in the host filesystem, or refactoring the workflow so that it does not require host filesystem interaction.',
				location: fsInteractionNodeTypes,
			});
		}

		return report;
	}
}

"""
MIGRATION-META:
  source_path: packages/cli/src/security-audit/risk-reporters/nodes-risk-reporter.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/security-audit/risk-reporters 的模块。导入/依赖:外部:fast-glob；内部:@n8n/di、n8n-core、n8n-workflow、@/load-nodes-and-credentials、@/security-audit/types、@/security-audit/utils；本地:../security-audit.repository。导出:NodesRiskReporter。关键函数/方法:report、sentenceStart、getCommunityNodeDetails、getCustomNodeDetails。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/security-audit/risk-reporters/nodes-risk-reporter.ts -> services/n8n/application/cli/services/security-audit/risk-reporters/nodes_risk_reporter.py

import { Service } from '@n8n/di';
import glob from 'fast-glob';
import { CUSTOM_NODES_PACKAGE_NAME } from 'n8n-core';
import type { IWorkflowBase } from 'n8n-workflow';
import * as path from 'path';

import { LoadNodesAndCredentials } from '@/load-nodes-and-credentials';
import {
	OFFICIAL_RISKY_NODE_TYPES,
	ENV_VARS_DOCS_URL,
	NODES_REPORT,
	COMMUNITY_NODES_RISKS_URL,
	NPM_PACKAGE_URL,
} from '@/security-audit/constants';
import type { Risk, RiskReporter } from '@/security-audit/types';
import { getNodeTypes } from '@/security-audit/utils';

import { PackagesRepository } from '../security-audit.repository';

@Service()
export class NodesRiskReporter implements RiskReporter {
	constructor(
		private readonly loadNodesAndCredentials: LoadNodesAndCredentials,
		private readonly packagesRepository: PackagesRepository,
	) {}

	async report(workflows: IWorkflowBase[]) {
		const officialRiskyNodes = getNodeTypes(workflows, (node) =>
			OFFICIAL_RISKY_NODE_TYPES.has(node.type),
		);

		const [communityNodes, customNodes] = await Promise.all([
			this.getCommunityNodeDetails(),
			this.getCustomNodeDetails(),
		]);

		const issues = [officialRiskyNodes, communityNodes, customNodes];

		if (issues.every((i) => i.length === 0)) return null;

		const report: Risk.StandardReport = {
			risk: NODES_REPORT.RISK,
			sections: [],
		};

		const sentenceStart = (length: number) => (length > 1 ? 'These nodes are' : 'This node is');

		if (officialRiskyNodes.length > 0) {
			report.sections.push({
				title: NODES_REPORT.SECTIONS.OFFICIAL_RISKY_NODES,
				description: [
					sentenceStart(officialRiskyNodes.length),
					"part of n8n's official nodes and may be used to fetch and run any arbitrary code in the host system. This may lead to exploits such as remote code execution.",
				].join(' '),
				recommendation: `Consider reviewing the parameters in these nodes, replacing them with app nodes where possible, and not loading unneeded node types with the NODES_EXCLUDE environment variable. See: ${ENV_VARS_DOCS_URL}`,
				location: officialRiskyNodes,
			});
		}

		if (communityNodes.length > 0) {
			report.sections.push({
				title: NODES_REPORT.SECTIONS.COMMUNITY_NODES,
				description: [
					sentenceStart(communityNodes.length),
					`sourced from the n8n community. Community nodes are not vetted by the n8n team and have full access to the host system. See: ${COMMUNITY_NODES_RISKS_URL}`,
				].join(' '),
				recommendation:
					'Consider reviewing the source code in any community nodes installed in this n8n instance, and uninstalling any community nodes no longer in use.',
				location: communityNodes,
			});
		}

		if (customNodes.length > 0) {
			report.sections.push({
				title: NODES_REPORT.SECTIONS.CUSTOM_NODES,
				description: [
					sentenceStart(communityNodes.length),
					'unpublished and located in the host system. Custom nodes are not vetted by the n8n team and have full access to the host system.',
				].join(' '),
				recommendation:
					'Consider reviewing the source code in any custom node installed in this n8n instance, and removing any custom nodes no longer in use.',
				location: customNodes,
			});
		}

		return report;
	}

	private async getCommunityNodeDetails() {
		const installedPackages = await this.packagesRepository.find({ relations: ['installedNodes'] });

		return installedPackages.reduce<Risk.CommunityNodeDetails[]>((acc, pkg) => {
			pkg.installedNodes.forEach((node) =>
				acc.push({
					kind: 'community',
					nodeType: node.type,
					packageUrl: [NPM_PACKAGE_URL, pkg.packageName].join('/'),
				}),
			);

			return acc;
		}, []);
	}

	private async getCustomNodeDetails() {
		const customNodeTypes: Risk.CustomNodeDetails[] = [];

		for (const customDir of this.loadNodesAndCredentials.getCustomDirectories()) {
			const customNodeFiles = await glob('**/*.node.js', { cwd: customDir, absolute: true });

			for (const nodeFile of customNodeFiles) {
				const [fileName] = path.parse(nodeFile).name.split('.');
				customNodeTypes.push({
					kind: 'custom',
					nodeType: [CUSTOM_NODES_PACKAGE_NAME, fileName].join('.'),
					filePath: nodeFile,
				});
			}
		}

		return customNodeTypes;
	}
}

"""
MIGRATION-META:
  source_path: packages/cli/src/security-audit/types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/security-audit 的类型。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:Category、NodeLocation、CommunityNodeDetails、CustomNodeDetails、Report、StandardSection、InstanceSection、StandardReport 等6项。关键函数/方法:report。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/security-audit/types.ts -> services/n8n/application/cli/services/security-audit/types.py

import type { IWorkflowBase } from 'n8n-workflow';

export namespace Risk {
	export type Category = 'database' | 'credentials' | 'nodes' | 'instance' | 'filesystem';

	type CredLocation = {
		kind: 'credential';
		id: string;
		name: string;
	};

	export type NodeLocation = {
		kind: 'node';
		workflowId: string;
		workflowName: string;
		nodeId: string;
		nodeName: string;
		nodeType: string;
	};

	export type CommunityNodeDetails = {
		kind: 'community';
		nodeType: string;
		packageUrl: string;
	};

	export type CustomNodeDetails = {
		kind: 'custom';
		nodeType: string;
		filePath: string;
	};

	type SectionBase = {
		title: string;
		description: string;
		recommendation: string;
	};

	export type Report = StandardReport | InstanceReport;

	export type StandardSection = SectionBase & {
		location: NodeLocation[] | CredLocation[] | CommunityNodeDetails[] | CustomNodeDetails[];
	};

	export type InstanceSection = SectionBase & {
		location?: NodeLocation[];
		settings?: Record<string, unknown>;
		nextVersions?: n8n.Version[];
	};

	export type StandardReport = {
		risk: Exclude<Category, 'instance'>;
		sections: StandardSection[];
	};

	export type InstanceReport = {
		risk: 'instance';
		sections: InstanceSection[];
	};

	export type Audit = {
		[reportTitle: string]: Report;
	};

	export type SyncReportFn = (workflows: IWorkflowBase[]) => StandardReport | null;

	export type AsyncReportFn = (workflows: IWorkflowBase[]) => Promise<Report | null>;
}

export namespace n8n {
	export type Version = {
		name: string;
		nodes: Array<
			IWorkflowBase['nodes'][number] & {
				iconData?: { type: string; fileBuffer: string }; // removed to declutter report
			}
		>;
		createdAt: string;
		description: string;
		documentationUrl: string;
		hasBreakingChange: boolean;
		hasSecurityFix: boolean;
		hasSecurityIssue: boolean;
		securityIssueFixVersion: string;
	};
}

export interface RiskReporter {
	report(workflows: IWorkflowBase[]): Promise<Risk.Report | null>;
}

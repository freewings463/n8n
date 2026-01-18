"""
MIGRATION-META:
  source_path: packages/cli/src/errors/subworkflow-policy-denial.error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/errors 的工作流错误。导入/依赖:外部:无；内部:@n8n/db、n8n-workflow；本地:无。导出:SUBWORKFLOW_DENIAL_BASE_DESCRIPTION、SubworkflowPolicyDenialError。关键函数/方法:description。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/errors/subworkflow-policy-denial.error.ts -> services/n8n/application/cli/services/errors/subworkflow_policy_denial_error.py

import type { Project } from '@n8n/db';
import { WorkflowOperationError } from 'n8n-workflow';
import type { INode } from 'n8n-workflow';

type Options = {
	/** ID of the subworkflow whose execution was denied. */
	subworkflowId: string;

	/** Project that owns the subworkflow whose execution was denied. */
	subworkflowProject: Project;

	/** Whether the user has read access to the subworkflow based on their project and scope. */
	hasReadAccess: boolean;

	/** URL of the n8n instance. */
	instanceUrl: string;

	/** Full name of the user who owns the personal project that owns the subworkflow. Absent if team project. */
	ownerName?: string;

	/** Node that triggered the execution of the subworkflow whose execution was denied. */
	node?: INode;
};

export const SUBWORKFLOW_DENIAL_BASE_DESCRIPTION =
	'The sub-workflow you’re trying to execute limits which workflows it can be called by.';

export class SubworkflowPolicyDenialError extends WorkflowOperationError {
	constructor({
		subworkflowId,
		subworkflowProject,
		instanceUrl,
		hasReadAccess,
		ownerName,
		node,
	}: Options) {
		const descriptions = {
			default: SUBWORKFLOW_DENIAL_BASE_DESCRIPTION,
			accessible: [
				SUBWORKFLOW_DENIAL_BASE_DESCRIPTION,
				`<a href="${instanceUrl}/workflow/${subworkflowId}" target="_blank">Update sub-workflow settings</a> to allow other workflows to call it.`,
			].join(' '),
			inaccessiblePersonalProject: [
				SUBWORKFLOW_DENIAL_BASE_DESCRIPTION,
				`You will need ${ownerName} to update the sub-workflow (${subworkflowId}) settings to allow this workflow to call it.`,
			].join(' '),
			inaccesibleTeamProject: [
				SUBWORKFLOW_DENIAL_BASE_DESCRIPTION,
				`You will need an admin from the ${subworkflowProject.name} project to update the sub-workflow (${subworkflowId}) settings to allow this workflow to call it.`,
			].join(' '),
		};

		const description = () => {
			if (hasReadAccess) return descriptions.accessible;
			if (subworkflowProject.type === 'personal') return descriptions.inaccessiblePersonalProject;
			if (subworkflowProject.type === 'team') return descriptions.inaccesibleTeamProject;

			return descriptions.default;
		};

		super(
			`The sub-workflow (${subworkflowId}) cannot be called by this workflow`,
			node,
			description(),
		);
	}
}

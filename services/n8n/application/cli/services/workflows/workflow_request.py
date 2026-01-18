"""
MIGRATION-META:
  source_path: packages/cli/src/workflows/workflow.request.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/workflows 的工作流模块。导入/依赖:外部:无；内部:@n8n/db、@/requests；本地:无。导出:无。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/workflows/workflow.request.ts -> services/n8n/application/cli/services/workflows/workflow_request.py

import type { AuthenticatedRequest } from '@n8n/db';
import type {
	INode,
	IConnections,
	IWorkflowSettings,
	IRunData,
	ITaskData,
	IWorkflowBase,
	AiAgentRequest,
	IDestinationNode,
} from 'n8n-workflow';

import type { ListQuery } from '@/requests';

export declare namespace WorkflowRequest {
	type CreateUpdatePayload = Partial<{
		id: string; // deleted if sent
		name: string;
		description: string | null;
		nodes: INode[];
		connections: IConnections;
		settings: IWorkflowSettings;
		active: boolean;
		tags: string[];
		hash: string;
		meta: Record<string, unknown>;
		projectId: string;
		parentFolderId?: string;
		uiContext?: string;
		expectedChecksum?: string;
		aiBuilderAssisted?: boolean;
		autosaved?: boolean;
	}>;

	// TODO: Use a discriminator when CAT-1809 lands
	//
	// 1. Full Manual Execution from Known Trigger
	type FullManualExecutionFromKnownTriggerPayload = {
		workflowData: IWorkflowBase;
		agentRequest?: AiAgentRequest;

		destinationNode?: IDestinationNode;
		triggerToStartFrom: { name: string; data?: ITaskData };
	};
	// 2. Full Manual Execution from Unknown Trigger
	type FullManualExecutionFromUnknownTriggerPayload = {
		workflowData: IWorkflowBase;
		agentRequest?: AiAgentRequest;

		destinationNode: IDestinationNode;
	};

	// 3. Partial Manual Execution to Destination
	type PartialManualExecutionToDestinationPayload = {
		workflowData: IWorkflowBase;
		agentRequest?: AiAgentRequest;

		runData: IRunData;
		destinationNode: IDestinationNode;
		dirtyNodeNames: string[];
	};

	type ManualRunPayload =
		| FullManualExecutionFromKnownTriggerPayload
		| FullManualExecutionFromUnknownTriggerPayload
		| PartialManualExecutionToDestinationPayload;

	type Create = AuthenticatedRequest<{}, {}, CreateUpdatePayload>;

	type Get = AuthenticatedRequest<{ workflowId: string }>;

	type GetMany = AuthenticatedRequest<
		{},
		{},
		{},
		ListQuery.Params & {
			includeScopes?: string;
			includeFolders?: string;
			onlySharedWithMe?: string;
			availableInMCP?: string;
		}
	> & {
		listQueryOptions: ListQuery.Options;
	};

	type Update = AuthenticatedRequest<
		{ workflowId: string },
		{},
		CreateUpdatePayload,
		{ forceSave?: string }
	>;

	type NewName = AuthenticatedRequest<{}, {}, {}, { name?: string; projectId: string }>;

	type ManualRun = AuthenticatedRequest<{ workflowId: string }, {}, ManualRunPayload, {}>;

	type Share = AuthenticatedRequest<{ workflowId: string }, {}, { shareWithIds: string[] }>;

	type Activate = AuthenticatedRequest<
		{ workflowId: string },
		{},
		{ versionId: string; name?: string; description?: string; expectedChecksum?: string }
	>;

	type Deactivate = AuthenticatedRequest<{ workflowId: string }>;
}

"""
MIGRATION-META:
  source_path: packages/cli/src/scaling/scaling.types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/scaling 的类型。导入/依赖:外部:bull、p-cancelable；内部:@n8n/api-types；本地:无。导出:JobQueue、Job、JobId、JobData、JobResult、JobStatus、JobOptions、JobMessage 等7项。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/scaling/scaling.types.ts -> services/n8n/application/cli/services/scaling/scaling_types.py

import type { RunningJobSummary } from '@n8n/api-types';
import type Bull from 'bull';
import type {
	ExecutionError,
	IExecuteResponsePromiseData,
	IRun,
	StructuredChunk,
} from 'n8n-workflow';
import type PCancelable from 'p-cancelable';

export type JobQueue = Bull.Queue<JobData>;

export type Job = Bull.Job<JobData>;

export type JobId = Job['id'];

export type JobData = {
	workflowId: string;
	executionId: string;
	loadStaticData: boolean;
	pushRef?: string;
	streamingEnabled?: boolean;
};

export type JobResult = {
	success: boolean;
	error?: ExecutionError;
};

export type JobStatus = Bull.JobStatus;

export type JobOptions = Bull.JobOptions;

/**
 * Message sent by main to worker and vice versa about a job. `JobMessage` is
 * sent via Bull's internal pubsub setup - do not confuse with `PubSub.Command`
 * and `PubSub.Response`, which are sent via n8n's own pubsub setup to keep
 * main and worker processes in sync outside of a job's lifecycle.
 */
export type JobMessage =
	| RespondToWebhookMessage
	| JobFinishedMessage
	| JobFailedMessage
	| AbortJobMessage
	| SendChunkMessage;

/** Message sent by worker to main to respond to a webhook. */
export type RespondToWebhookMessage = {
	kind: 'respond-to-webhook';
	executionId: string;
	response: IExecuteResponsePromiseData;
	workerId: string;
};

/** Message sent by worker to main to report a job has finished successfully. */
export type JobFinishedMessage = {
	kind: 'job-finished';
	executionId: string;
	workerId: string;
	success: boolean;
};

export type SendChunkMessage = {
	kind: 'send-chunk';
	executionId: string;
	chunkText: StructuredChunk;
	workerId: string;
};

/** Message sent by worker to main to report a job has failed. */
export type JobFailedMessage = {
	kind: 'job-failed';
	executionId: string;
	workerId: string;
	errorMsg: string;
	errorStack: string;
};

/** Message sent by main to worker to abort a job. */
export type AbortJobMessage = {
	kind: 'abort-job';
};

export type RunningJob = RunningJobSummary & {
	run: PCancelable<IRun>;
};

export type QueueRecoveryContext = {
	/** ID of timeout for next scheduled recovery cycle. */
	timeout?: NodeJS.Timeout;

	/** Number of in-progress executions to check per cycle. */
	batchSize: number;

	/** Time (in milliseconds) to wait until the next cycle. */
	waitMs: number;
};

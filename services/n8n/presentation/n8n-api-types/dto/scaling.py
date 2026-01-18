"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/scaling.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src 的模块。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:RunningJobSummary、WorkerStatus。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/scaling.ts -> services/n8n/presentation/n8n-api-types/dto/scaling.py

import type { ExecutionStatus, WorkflowExecuteMode } from 'n8n-workflow';

export type RunningJobSummary = {
	executionId: string;
	workflowId: string;
	workflowName: string;
	mode: WorkflowExecuteMode;
	startedAt: Date;
	retryOf?: string;
	status: ExecutionStatus;
};

export type WorkerStatus = {
	senderId: string;
	runningJobsSummary: RunningJobSummary[];
	isInContainer: boolean;
	process: {
		memory: {
			available: number;
			constraint: number;
			rss: number;
			heapTotal: number;
			heapUsed: number;
		};
		uptime: number;
	};
	host: {
		memory: {
			total: number;
			free: number;
		};
	};
	freeMem: number;
	totalMem: number;
	uptime: number;
	loadAvg: number[];
	cpus: string;
	arch: string;
	platform: NodeJS.Platform;
	hostname: string;
	interfaces: Array<{
		family: 'IPv4' | 'IPv6';
		address: string;
		internal: boolean;
	}>;
	version: string;
};

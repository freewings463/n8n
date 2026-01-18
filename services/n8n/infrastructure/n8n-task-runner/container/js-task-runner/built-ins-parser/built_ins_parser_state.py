"""
MIGRATION-META:
  source_path: packages/@n8n/task-runner/src/js-task-runner/built-ins-parser/built-ins-parser-state.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/task-runner/src/js-task-runner/built-ins-parser 的模块。导入/依赖:外部:无；内部:@/message-types、@/runner-types；本地:无。导出:BuiltInsParserState。关键函数/方法:markNeedsAllNodes、markNodeAsNeeded、markEnvAsNeeded、markInputAsNeeded、markExecutionAsNeeded、markPrevNodeAsNeeded、toDataRequestParams、newNeedsAllDataState。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Task runner process runtime -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/task-runner/src/js-task-runner/built-ins-parser/built-ins-parser-state.ts -> services/n8n/infrastructure/n8n-task-runner/container/js-task-runner/built-ins-parser/built_ins_parser_state.py

import type { BrokerMessage } from '@/message-types';
import type { InputDataChunkDefinition } from '@/runner-types';

/**
 * Class to keep track of which built-in variables are accessed in the code
 */
export class BuiltInsParserState {
	neededNodeNames: Set<string> = new Set();

	needsAllNodes = false;

	needs$env = false;

	needs$input = false;

	needs$execution = false;

	needs$prevNode = false;

	constructor(opts: Partial<BuiltInsParserState> = {}) {
		Object.assign(this, opts);
	}

	/**
	 * Marks that all nodes are needed, including input data
	 */
	markNeedsAllNodes() {
		this.needsAllNodes = true;
		this.needs$input = true;
		this.neededNodeNames = new Set();
	}

	markNodeAsNeeded(nodeName: string) {
		if (this.needsAllNodes) {
			return;
		}

		this.neededNodeNames.add(nodeName);
	}

	markEnvAsNeeded() {
		this.needs$env = true;
	}

	markInputAsNeeded() {
		this.needs$input = true;
	}

	markExecutionAsNeeded() {
		this.needs$execution = true;
	}

	markPrevNodeAsNeeded() {
		this.needs$prevNode = true;
	}

	toDataRequestParams(
		chunk?: InputDataChunkDefinition,
	): BrokerMessage.ToRequester.TaskDataRequest['requestParams'] {
		return {
			dataOfNodes: this.needsAllNodes ? 'all' : Array.from(this.neededNodeNames),
			env: this.needs$env,
			input: {
				include: this.needs$input,
				chunk,
			},
			prevNode: this.needs$prevNode,
		};
	}

	static newNeedsAllDataState() {
		const obj = new BuiltInsParserState();
		obj.markNeedsAllNodes();
		obj.markEnvAsNeeded();
		obj.markInputAsNeeded();
		obj.markExecutionAsNeeded();
		obj.markPrevNodeAsNeeded();
		return obj;
	}
}

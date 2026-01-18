"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/Ollama/helpers/interfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/Ollama 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:OllamaMessage、ToolCall、OllamaTool、OllamaChatResponse、OllamaModel、OllamaTagsResponse。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/Ollama/helpers/interfaces.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/Ollama/helpers/interfaces.py

export interface OllamaMessage {
	role: 'system' | 'user' | 'assistant' | 'tool';
	content: string;
	images?: string[];
	tool_calls?: ToolCall[];
	tool_name?: string;
}

export interface ToolCall {
	function: {
		name: string;
		arguments: Record<string, any>;
	};
}

export interface OllamaTool {
	type: 'function';
	function: {
		name: string;
		description: string;
		parameters: Record<string, unknown>;
	};
}

export interface OllamaChatResponse {
	model: string;
	created_at: string;
	message: OllamaMessage;
	done: boolean;
	done_reason?: string;
	total_duration?: number;
	load_duration?: number;
	prompt_eval_count?: number;
	prompt_eval_duration?: number;
	eval_count?: number;
	eval_duration?: number;
}

export interface OllamaModel {
	name: string;
	modified_at: string;
	size: number;
	digest: string;
	details: {
		format: string;
		family: string;
		families: string[] | null;
		parameter_size: string;
		quantization_level: string;
	};
}

export interface OllamaTagsResponse {
	models: OllamaModel[];
}

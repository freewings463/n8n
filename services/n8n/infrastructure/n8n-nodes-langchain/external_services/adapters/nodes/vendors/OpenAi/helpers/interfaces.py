"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/helpers/interfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的节点。导入/依赖:外部:@langchain/openai；内部:n8n-workflow；本地:无。导出:ChatResponse、ChatContent、ChatInputItem、WebSearchTool、ChatTool、ChatResponseRequest、ChatCompletion、ThreadMessage 等2项。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/helpers/interfaces.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/helpers/interfaces.py

import { type OpenAIClient } from '@langchain/openai';
import type { IDataObject } from 'n8n-workflow';
import type {
	ComputerTool,
	CustomTool,
	FileSearchTool,
	FunctionTool,
	ResponseInputContent,
	ResponseInputItem,
	Tool,
	WebSearchTool as OpenAIChatWebSearchTool,
} from 'openai/resources/responses/responses';

export type ChatResponse = OpenAIClient.Responses.Response;
export type ChatContent = ResponseInputContent[];
export type ChatInputItem = OpenAIClient.Responses.ResponseInputItem.Message;

// FIXME: remove these overrides, when langchain-openai is updated with the new types
export type WebSearchTool = Omit<OpenAIChatWebSearchTool, 'type'> & {
	type: 'web_search';
	filters?: {
		allowed_domains?: string[];
	};
};

export type ChatTool =
	| FunctionTool
	| FileSearchTool
	| WebSearchTool
	| ComputerTool
	| Tool.CodeInterpreter
	| Tool.ImageGeneration
	| Tool.LocalShell
	| CustomTool;

export type ChatResponseRequest = Omit<
	OpenAIClient.Responses.ResponseCreateParamsNonStreaming,
	'input'
> & {
	max_tool_calls?: number;
	conversation?:
		| string
		| {
				id: string;
		  };
	input: ResponseInputItem[];
	top_logprobs?: number;
	tools?: ChatTool[];
};

export type ChatCompletion = {
	id: string;
	object: string;
	created: number;
	model: string;
	choices: Array<{
		index: number;
		message: {
			role: string;
			content: string;
			tool_calls?: Array<{
				id: string;
				type: 'function';
				function: {
					name: string;
					arguments: string;
				};
			}>;
		};
		finish_reason?: 'tool_calls';
	}>;
	usage: {
		prompt_tokens: number;
		completion_tokens: number;
		total_tokens: number;
	};
	system_fingerprint: string;
};

export type ThreadMessage = {
	id: string;
	object: string;
	created_at: number;
	thread_id: string;
	role: string;
	content: Array<{
		type: string;
		text: {
			value: string;
			annotations: string[];
		};
	}>;
	file_ids: string[];
	assistant_id: string;
	run_id: string;
	metadata: IDataObject;
};

export type ExternalApiCallOptions = {
	callExternalApi: boolean;
	url: string;
	path: string;
	method: string;
	requestOptions: IDataObject;
	sendParametersIn: string;
};

export type VideoJob = {
	id: string;
	completed_at?: number;
	created_at: number;
	error?: {
		code: string;
		message: string;
	};
	expires_at?: number;
	model: string;
	object: 'video';
	progress?: number;
	remixed_from_video_id?: string;
	seconds: string;
	size: string;
	status: 'completed' | 'queued' | 'in_progress';
};

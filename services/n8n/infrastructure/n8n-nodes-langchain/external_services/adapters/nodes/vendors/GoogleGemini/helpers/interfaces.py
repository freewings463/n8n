"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/helpers/interfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:Modality、GenerateContentGenerationConfig、GenerateContentRequest、GenerateContentResponse、Content、Part、ImagenResponse、VeoResponse 等3项。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/helpers/interfaces.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/GoogleGemini/helpers/interfaces.py

import type {
	GenerateContentConfig,
	GenerationConfig,
	GenerateContentParameters,
} from '@google/genai';
import type { IDataObject } from 'n8n-workflow';
export { Modality } from '@google/genai';

/* type created based on: https://ai.google.dev/api/generate-content#generationconfig */
export type GenerateContentGenerationConfig = Pick<
	GenerationConfig,
	| 'stopSequences'
	| 'responseMimeType'
	| 'responseSchema'
	| 'responseJsonSchema'
	| 'responseModalities'
	| 'candidateCount'
	| 'maxOutputTokens'
	| 'temperature'
	| 'topP'
	| 'topK'
	| 'seed'
	| 'presencePenalty'
	| 'frequencyPenalty'
	| 'responseLogprobs'
	| 'logprobs'
	| 'speechConfig'
	| 'thinkingConfig'
	| 'mediaResolution'
>;

/* Type created based on: https://ai.google.dev/api/generate-content#method:-models.streamgeneratecontent */
export interface GenerateContentRequest extends IDataObject {
	contents: GenerateContentParameters['contents'];
	tools?: GenerateContentConfig['tools'];
	toolConfig?: GenerateContentConfig['toolConfig'];
	systemInstruction?: GenerateContentConfig['systemInstruction'];
	safetySettings?: GenerateContentConfig['safetySettings'];
	generationConfig?: GenerateContentGenerationConfig;
	cachedContent?: string;
}

export interface GenerateContentResponse {
	candidates: Array<{
		content: Content;
	}>;
}

export interface Content {
	parts: Part[];
	role: string;
}

export type Part =
	| { text: string }
	| {
			inlineData: {
				mimeType: string;
				data: string;
			};
	  }
	| {
			functionCall: {
				id?: string;
				name: string;
				args?: IDataObject;
			};
	  }
	| {
			functionResponse: {
				id?: string;
				name: string;
				response: IDataObject;
			};
	  }
	| {
			fileData?: {
				mimeType?: string;
				fileUri?: string;
			};
	  };

export interface ImagenResponse {
	predictions: Array<{
		bytesBase64Encoded: string;
		mimeType: string;
	}>;
}

export interface VeoResponse {
	name: string;
	done: boolean;
	error?: {
		message: string;
	};
	response: {
		generateVideoResponse: {
			generatedSamples: Array<{
				video: {
					uri: string;
				};
			}>;
		};
	};
}

/**
 * File Search operation interface for long-running upload operations
 * Based on: https://ai.google.dev/api/file-search/file-search-stores#method:-media.uploadtofilesearchstore
 */
export interface FileSearchOperation {
	name: string;
	done: boolean;
	error?: { message: string };
	response?: IDataObject;
}

/**
 * User configuration for built-in tools in the node parameters
 */
export interface BuiltInTools {
	googleSearch?: boolean;
	googleMaps?: {
		latitude?: number | string;
		longitude?: number | string;
	};
	urlContext?: boolean;
	fileSearch?: {
		fileSearchStoreNames?: string;
		metadataFilter?: string;
	};
	codeExecution?: boolean;
}

/**
 * Tool structure for the Google Gemini API request
 */
export interface Tool {
	functionDeclarations?: Array<{
		name: string;
		description: string;
		parameters: IDataObject;
	}>;
	googleSearch?: object;
	googleMaps?: object;
	urlContext?: object;
	fileSearch?: {
		fileSearchStoreNames?: string[];
		metadataFilter?: string;
	};
	codeExecution?: object;
}

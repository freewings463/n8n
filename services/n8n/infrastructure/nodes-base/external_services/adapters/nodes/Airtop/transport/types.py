"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/transport/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/transport 的类型。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:IAirtopSessionResponse、IAirtopResponse、IAirtopResponseWithFiles、IAirtopInteractionRequest、IAirtopFileInputRequest、IAirtopNodeExecutionData、IAirtopServerEvent。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/transport/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/transport/types.py

import type { IDataObject, INodeExecutionData } from 'n8n-workflow';

export interface IAirtopSessionResponse extends IDataObject {
	data: {
		id: string;
		status: string;
	};
}

export interface IAirtopResponse extends IDataObject {
	sessionId?: string;
	windowId?: string;
	data?: IDataObject & {
		windowId?: string;
		modelResponse?: string;
		files?: IDataObject[];
	};
	meta?: IDataObject & {
		status?: string;
		screenshots?: Array<{ dataUrl: string }>;
	};
	errors?: IDataObject[];
	warnings?: IDataObject[];
	output?: IDataObject;
}

export interface IAirtopResponseWithFiles extends IAirtopResponse {
	data: {
		files: IDataObject[];
		fileName?: string;
		status?: string;
		downloadUrl?: string;
		pagination: {
			hasMore: boolean;
		};
		sessionIds?: string[];
	};
}

export interface IAirtopInteractionRequest extends IDataObject {
	text?: string;
	waitForNavigation?: boolean;
	elementDescription?: string;
	pressEnterKey?: boolean;
	// scroll parameters
	scrollToElement?: string;
	scrollWithin?: string;
	scrollToEdge?: {
		xAxis?: string;
		yAxis?: string;
	};
	scrollBy?: {
		xAxis?: string;
		yAxis?: string;
	};
	// configuration
	configuration: {
		visualAnalysis?: {
			scope: string;
		};
		waitForNavigationConfig?: {
			waitUntil: string;
		};
		clickType?: string;
	};
}

export interface IAirtopFileInputRequest extends IDataObject {
	fileId: string;
	windowId: string;
	sessionId: string;
	elementDescription?: string;
	includeHiddenElements?: boolean;
}

export interface IAirtopNodeExecutionData extends INodeExecutionData {
	json: IAirtopResponse;
}

export interface IAirtopServerEvent {
	event: string;
	eventData: {
		error?: string;
	};
	fileId?: string;
	status?: string;
	downloadUrl?: string;
}

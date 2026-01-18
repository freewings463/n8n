"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SurveyMonkey/Interfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SurveyMonkey 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:IImage、IChoice、IRow、IOther、IQuestion、IAnswer。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SurveyMonkey/Interfaces.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SurveyMonkey/Interfaces.py

import type { IDataObject } from 'n8n-workflow';

export interface IImage {
	url: string;
}

export interface IChoice {
	position: number;
	visible: boolean;
	text: string;
	id: string;
	weight: number;
	description: string;
	image?: IImage;
}

export interface IRow {
	position: number;
	visible: boolean;
	text: string;
	id: string;
}

export interface IOther {
	text: string;
	visible: boolean;
	is_answer_choice: boolean;
	id: string;
}

export interface IQuestion {
	id: string;
	family?: string;
	subtype?: string;
	headings?: IDataObject[];
	answers: IDataObject;
	rows?: IDataObject;
}

export interface IAnswer {
	choice_id: string;
	row_id?: string;
	text?: string;
	other_id?: string;
}

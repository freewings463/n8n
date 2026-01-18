"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/BigQuery/v2/methods/loadOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/BigQuery 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../transport。导出:无。关键函数/方法:getDatasets、getSchema。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/BigQuery/v2/methods/loadOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/BigQuery/v2/methods/loadOptions.py

import type { IDataObject, ILoadOptionsFunctions, INodePropertyOptions } from 'n8n-workflow';

import { googleBigQueryApiRequest } from '../transport';

export async function getDatasets(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const projectId = this.getNodeParameter('projectId', undefined, {
		extractValue: true,
	});
	const returnData: INodePropertyOptions[] = [];
	const { datasets } = await googleBigQueryApiRequest.call(
		this,
		'GET',
		`/v2/projects/${projectId}/datasets`,
	);
	for (const dataset of datasets) {
		returnData.push({
			name: dataset.datasetReference.datasetId as string,
			value: dataset.datasetReference.datasetId,
		});
	}
	return returnData;
}

export async function getSchema(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const projectId = this.getNodeParameter('projectId', undefined, {
		extractValue: true,
	});
	const datasetId = this.getNodeParameter('datasetId', undefined, {
		extractValue: true,
	});
	const tableId = this.getNodeParameter('tableId', undefined, {
		extractValue: true,
	});

	const returnData: INodePropertyOptions[] = [];

	const { schema } = await googleBigQueryApiRequest.call(
		this,
		'GET',
		`/v2/projects/${projectId}/datasets/${datasetId}/tables/${tableId}`,
		{},
	);

	for (const field of schema.fields as IDataObject[]) {
		returnData.push({
			name: field.name as string,
			value: field.name as string,

			description:
				`type: ${field.type as string}` + (field.mode ? ` mode: ${field.mode as string}` : ''),
		});
	}
	return returnData;
}

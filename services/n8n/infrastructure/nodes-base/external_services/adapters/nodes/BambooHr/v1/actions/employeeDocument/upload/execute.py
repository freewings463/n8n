"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/BambooHr/v1/actions/employeeDocument/upload/execute.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/BambooHr/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport。导出:无。关键函数/方法:upload。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/BambooHr/v1/actions/employeeDocument/upload/execute.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/BambooHr/v1/actions/employeeDocument/upload/execute.py

import type { IDataObject, IExecuteFunctions } from 'n8n-workflow';

import { apiRequest } from '../../../transport';

export async function upload(this: IExecuteFunctions, index: number) {
	let body: IDataObject = {};
	const requestMethod = 'POST';

	const id: string = this.getNodeParameter('employeeId', index) as string;
	const category = this.getNodeParameter('categoryId', index) as string;
	const options = this.getNodeParameter('options', index);
	const binaryPropertyName = this.getNodeParameter('binaryPropertyName', index);
	const { fileName, mimeType } = this.helpers.assertBinaryData(index, binaryPropertyName);
	const binaryDataBuffer = await this.helpers.getBinaryDataBuffer(index, binaryPropertyName);

	body = {
		json: false,
		formData: {
			file: {
				value: binaryDataBuffer,
				options: {
					filename: fileName,
					contentType: mimeType,
				},
			},
			fileName,
			category,
		},
		resolveWithFullResponse: true,
	};

	if (options.hasOwnProperty('share') && body.formData) {
		Object.assign(body.formData, options.share ? { share: 'yes' } : { share: 'no' });
	}
	//endpoint
	const endpoint = `employees/${id}/files`;
	const { headers } = await apiRequest.call(this, requestMethod, endpoint, {}, {}, body);
	return this.helpers.returnJsonArray({ fileId: headers.location.split('/').pop() });
}

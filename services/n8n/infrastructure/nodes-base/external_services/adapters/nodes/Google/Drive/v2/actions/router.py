"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Drive/v2/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Drive 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./drive/Drive.resource、./file/File.resource、./fileFolder/FileFolder.resource、./folder/Folder.resource 等1项。导出:无。关键函数/方法:router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Drive/v2/actions/router.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Drive/v2/actions/router.py

import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import * as drive from './drive/Drive.resource';
import * as file from './file/File.resource';
import * as fileFolder from './fileFolder/FileFolder.resource';
import * as folder from './folder/Folder.resource';
import type { GoogleDriveType } from './node.type';

export async function router(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
	const items = this.getInputData();
	const returnData: INodeExecutionData[] = [];

	const resource = this.getNodeParameter<GoogleDriveType>('resource', 0);
	const operation = this.getNodeParameter('operation', 0);

	const googleDrive = {
		resource,
		operation,
	} as GoogleDriveType;

	for (let i = 0; i < items.length; i++) {
		try {
			switch (googleDrive.resource) {
				case 'drive':
					returnData.push(...(await drive[googleDrive.operation].execute.call(this, i)));
					break;
				case 'file':
					returnData.push(...(await file[googleDrive.operation].execute.call(this, i, items[i])));
					break;
				case 'fileFolder':
					returnData.push(...(await fileFolder[googleDrive.operation].execute.call(this, i)));
					break;
				case 'folder':
					returnData.push(...(await folder[googleDrive.operation].execute.call(this, i)));
					break;
				default:
					throw new NodeOperationError(this.getNode(), `The resource "${resource}" is not known`);
			}
		} catch (error) {
			if (this.continueOnFail()) {
				if (resource === 'file' && operation === 'download') {
					items[i].json = { error: error.message };
				} else {
					returnData.push({ json: { error: error.message } });
				}
				continue;
			}
			throw error;
		}
	}

	return [returnData];
}

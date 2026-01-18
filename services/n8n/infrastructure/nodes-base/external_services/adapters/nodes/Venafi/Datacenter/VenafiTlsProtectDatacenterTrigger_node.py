"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Venafi/Datacenter/VenafiTlsProtectDatacenterTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Venafi/Datacenter 的节点。导入/依赖:外部:moment-timezone；内部:无；本地:./GenericFunctions。导出:VenafiTlsProtectDatacenterTrigger。关键函数/方法:poll。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Venafi/Datacenter/VenafiTlsProtectDatacenterTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Venafi/Datacenter/VenafiTlsProtectDatacenterTrigger_node.py

import moment from 'moment-timezone';
import {
	type IPollFunctions,
	type IDataObject,
	type INodeExecutionData,
	type INodeType,
	type INodeTypeDescription,
	NodeConnectionTypes,
} from 'n8n-workflow';

import { venafiApiRequest } from './GenericFunctions';

export class VenafiTlsProtectDatacenterTrigger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Venafi TLS Protect Datacenter Trigger',
		name: 'venafiTlsProtectDatacenterTrigger',
		icon: 'file:../venafi.svg',
		group: ['trigger'],
		version: 1,
		subtitle: '={{$parameter["triggerOn"]}}',
		description: 'Starts the workflow when Venafi events occur',
		defaults: {
			name: 'Venafi TLS Protect Datacenter​',
		},
		credentials: [
			{
				name: 'venafiTlsProtectDatacenterApi',
				required: true,
			},
		],
		polling: true,
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName: 'Trigger On',
				name: 'triggerOn',
				type: 'options',
				options: [
					{
						name: 'Certificate Expired',
						value: 'certificateExpired',
					},
				],
				required: true,
				default: 'certificateExpired',
			},
		],
	};

	async poll(this: IPollFunctions): Promise<INodeExecutionData[][] | null> {
		const webhookData = this.getWorkflowStaticData('node');

		const qs: IDataObject = {};

		const now = moment().format();

		qs.ValidToGreater = webhookData.lastTimeChecked || now;

		qs.ValidToLess = now;

		const { Certificates: certificates } = await venafiApiRequest.call(
			this,
			'GET',
			'/vedsdk/certificates',
			{},
			qs,
		);

		webhookData.lastTimeChecked = qs.ValidToLess;

		if (Array.isArray(certificates) && certificates.length !== 0) {
			return [this.helpers.returnJsonArray(certificates)];
		}

		return null;
	}
}

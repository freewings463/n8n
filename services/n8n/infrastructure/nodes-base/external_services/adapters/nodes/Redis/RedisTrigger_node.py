"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Redis/RedisTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Redis 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./types、./utils。导出:RedisTrigger。关键函数/方法:trigger、channels、onMessage、manualTriggerFunction、resolve、closeFunction。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Redis/RedisTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Redis/RedisTrigger_node.py

import type {
	ITriggerFunctions,
	INodeType,
	INodeTypeDescription,
	ITriggerResponse,
} from 'n8n-workflow';
import { NodeConnectionTypes, NodeOperationError } from 'n8n-workflow';

import type { RedisCredential } from './types';
import { redisConnectionTest, setupRedisClient } from './utils';

interface Options {
	jsonParseBody: boolean;
	onlyMessage: boolean;
}

export class RedisTrigger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Redis Trigger',
		name: 'redisTrigger',
		icon: 'file:redis.svg',
		group: ['trigger'],
		version: 1,
		description: 'Subscribe to redis channel',
		defaults: {
			name: 'Redis Trigger',
		},
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'redis',
				required: true,
				testedBy: 'redisConnectionTest',
			},
		],
		properties: [
			{
				displayName: 'Channels',
				name: 'channels',
				type: 'string',
				default: '',
				required: true,
				description:
					'Channels to subscribe to, multiple channels be defined with comma. Wildcard character(*) is supported.',
			},
			{
				displayName: 'Options',
				name: 'options',
				type: 'collection',
				placeholder: 'Add option',
				default: {},
				options: [
					{
						displayName: 'JSON Parse Body',
						name: 'jsonParseBody',
						type: 'boolean',
						default: false,
						description: 'Whether to try to parse the message to an object',
					},
					{
						displayName: 'Only Message',
						name: 'onlyMessage',
						type: 'boolean',
						default: false,
						description: 'Whether to return only the message property',
					},
				],
			},
		],
	};

	methods = {
		credentialTest: { redisConnectionTest },
	};

	async trigger(this: ITriggerFunctions): Promise<ITriggerResponse> {
		const credentials = await this.getCredentials<RedisCredential>('redis');

		const channels = (this.getNodeParameter('channels') as string).split(',');
		const options = this.getNodeParameter('options') as Options;

		if (!channels) {
			throw new NodeOperationError(this.getNode(), 'Channels are mandatory!');
		}

		const client = setupRedisClient(credentials);
		await client.connect();
		await client.ping();

		const onMessage = (message: string, channel: string) => {
			if (options.jsonParseBody) {
				try {
					message = JSON.parse(message);
				} catch (error) {}
			}

			const data = options.onlyMessage ? { message } : { channel, message };
			this.emit([this.helpers.returnJsonArray(data)]);
		};

		const manualTriggerFunction = async () =>
			await new Promise<void>(async (resolve) => {
				await client.pSubscribe(channels, (message, channel) => {
					onMessage(message, channel);
					resolve();
				});
			});

		if (this.getMode() === 'trigger') {
			await client.pSubscribe(channels, onMessage);
		}

		async function closeFunction() {
			await client.pUnsubscribe();
			await client.quit();
		}

		return {
			closeFunction,
			manualTriggerFunction,
		};
	}
}

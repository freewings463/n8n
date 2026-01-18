"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/common/aws/descriptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials/common/aws 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:./types。导出:awsRegionProperty、awsCustomEndpoints。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Credentials definition -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/common/aws/descriptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/common/aws/descriptions.py

import type { INodeProperties } from 'n8n-workflow';
import { regions } from './types';

export const awsRegionProperty: INodeProperties = {
	displayName: 'Region',
	name: 'region',
	type: 'options',
	options: regions.map((r) => ({
		name: `${r.displayName} (${r.location}) - ${r.name}`,
		value: r.name,
	})),
	default: 'us-east-1',
};

export const awsCustomEndpoints: INodeProperties[] = [
	{
		displayName: 'Custom Endpoints',
		name: 'customEndpoints',
		type: 'boolean',
		default: false,
	},
	{
		displayName: 'Rekognition Endpoint',
		name: 'rekognitionEndpoint',
		description:
			'If you use Amazon VPC to host n8n, you can establish a connection between your VPC and Rekognition using a VPC endpoint. Leave blank to use the default endpoint.',
		type: 'string',
		displayOptions: {
			show: {
				customEndpoints: [true],
			},
		},
		default: '',
		placeholder: 'https://rekognition.{region}.amazonaws.com',
	},
	{
		displayName: 'Lambda Endpoint',
		name: 'lambdaEndpoint',
		description:
			'If you use Amazon VPC to host n8n, you can establish a connection between your VPC and Lambda using a VPC endpoint. Leave blank to use the default endpoint.',
		type: 'string',
		displayOptions: {
			show: {
				customEndpoints: [true],
			},
		},
		default: '',
		placeholder: 'https://lambda.{region}.amazonaws.com',
	},
	{
		displayName: 'SNS Endpoint',
		name: 'snsEndpoint',
		description:
			'If you use Amazon VPC to host n8n, you can establish a connection between your VPC and SNS using a VPC endpoint. Leave blank to use the default endpoint.',
		type: 'string',
		displayOptions: {
			show: {
				customEndpoints: [true],
			},
		},
		default: '',
		placeholder: 'https://sns.{region}.amazonaws.com',
	},
	{
		displayName: 'SES Endpoint',
		name: 'sesEndpoint',
		description:
			'If you use Amazon VPC to host n8n, you can establish a connection between your VPC and SES using a VPC endpoint. Leave blank to use the default endpoint.',
		type: 'string',
		displayOptions: {
			show: {
				customEndpoints: [true],
			},
		},
		default: '',
		placeholder: 'https://email.{region}.amazonaws.com',
	},
	{
		displayName: 'SQS Endpoint',
		name: 'sqsEndpoint',
		description:
			'If you use Amazon VPC to host n8n, you can establish a connection between your VPC and SQS using a VPC endpoint. Leave blank to use the default endpoint.',
		type: 'string',
		displayOptions: {
			show: {
				customEndpoints: [true],
			},
		},
		default: '',
		placeholder: 'https://sqs.{region}.amazonaws.com',
	},
	{
		displayName: 'S3 Endpoint',
		name: 's3Endpoint',
		description:
			'If you use Amazon VPC to host n8n, you can establish a connection between your VPC and S3 using a VPC endpoint. Leave blank to use the default endpoint.',
		type: 'string',
		displayOptions: {
			show: {
				customEndpoints: [true],
			},
		},
		default: '',
		placeholder: 'https://s3.{region}.amazonaws.com',
	},
	{
		displayName: 'SSM Endpoint',
		name: 'ssmEndpoint',
		description: 'Endpoint for AWS Systems Manager (SSM)',
		type: 'string',
		displayOptions: {
			show: {
				customEndpoints: [true],
			},
		},
		default: '',
		placeholder: 'https://ssm.{region}.amazonaws.com',
	},
];

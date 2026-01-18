"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/common/aws/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials/common/aws 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:AWS_CHINA_DOMAIN、AWS_GLOBAL_DOMAIN、regions、AWSRegion、AwsCredentialsTypeBase、AwsIamCredentialsType、AwsAssumeRoleCredentialsType、AwsSecurityHeaders。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Credentials definition -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/common/aws/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/common/aws/types.py

export const AWS_CHINA_DOMAIN = 'amazonaws.com.cn';
export const AWS_GLOBAL_DOMAIN = 'amazonaws.com';

type RegionData = {
	name: string;
	displayName: string;
	location: string;
	domain?: string;
};

export const regions: RegionData[] = [
	{
		name: 'af-south-1',
		displayName: 'Africa',
		location: 'Cape Town',
	},
	{
		name: 'ap-east-1',
		displayName: 'Asia Pacific',
		location: 'Hong Kong',
	},
	{
		name: 'ap-south-1',
		displayName: 'Asia Pacific',
		location: 'Mumbai',
	},
	{
		name: 'ap-south-2',
		displayName: 'Asia Pacific',
		location: 'Hyderabad',
	},
	{
		name: 'ap-southeast-1',
		displayName: 'Asia Pacific',
		location: 'Singapore',
	},
	{
		name: 'ap-southeast-2',
		displayName: 'Asia Pacific',
		location: 'Sydney',
	},
	{
		name: 'ap-southeast-3',
		displayName: 'Asia Pacific',
		location: 'Jakarta',
	},
	{
		name: 'ap-southeast-4',
		displayName: 'Asia Pacific',
		location: 'Melbourne',
	},
	{
		name: 'ap-southeast-5',
		displayName: 'Asia Pacific',
		location: 'Malaysia',
	},
	{
		name: 'ap-southeast-7',
		displayName: 'Asia Pacific',
		location: 'Thailand',
	},
	{
		name: 'ap-northeast-1',
		displayName: 'Asia Pacific',
		location: 'Tokyo',
	},
	{
		name: 'ap-northeast-2',
		displayName: 'Asia Pacific',
		location: 'Seoul',
	},
	{
		name: 'ap-northeast-3',
		displayName: 'Asia Pacific',
		location: 'Osaka',
	},
	{
		name: 'ca-central-1',
		displayName: 'Canada',
		location: 'Central',
	},
	{
		name: 'ca-west-1',
		displayName: 'Canada West',
		location: 'Calgary',
	},
	{
		name: 'cn-north-1',
		displayName: 'China',
		location: 'Beijing',
		domain: AWS_CHINA_DOMAIN,
	},
	{
		name: 'cn-northwest-1',
		displayName: 'China',
		location: 'Ningxia',
		domain: AWS_CHINA_DOMAIN,
	},
	{
		name: 'eu-central-1',
		displayName: 'Europe',
		location: 'Frankfurt',
	},
	{
		name: 'eu-central-2',
		displayName: 'Europe',
		location: 'Zurich',
	},
	{
		name: 'eu-north-1',
		displayName: 'Europe',
		location: 'Stockholm',
	},
	{
		name: 'eu-south-1',
		displayName: 'Europe',
		location: 'Milan',
	},
	{
		name: 'eu-south-2',
		displayName: 'Europe',
		location: 'Spain',
	},
	{
		name: 'eu-west-1',
		displayName: 'Europe',
		location: 'Ireland',
	},
	{
		name: 'eu-west-2',
		displayName: 'Europe',
		location: 'London',
	},
	{
		name: 'eu-west-3',
		displayName: 'Europe',
		location: 'Paris',
	},
	{
		name: 'il-central-1',
		displayName: 'Israel',
		location: 'Tel Aviv',
	},
	{
		name: 'me-central-1',
		displayName: 'Middle East',
		location: 'UAE',
	},
	{
		name: 'me-south-1',
		displayName: 'Middle East',
		location: 'Bahrain',
	},
	{
		name: 'mx-central-1',
		displayName: 'Mexico',
		location: 'Central',
	},
	{
		name: 'sa-east-1',
		displayName: 'South America',
		location: 'São Paulo',
	},
	{
		name: 'us-east-1',
		displayName: 'US East',
		location: 'N. Virginia',
	},
	{
		name: 'us-east-2',
		displayName: 'US East',
		location: 'Ohio',
	},
	{
		name: 'us-gov-east-1',
		displayName: 'US East',
		location: 'GovCloud',
	},
	{
		name: 'us-west-1',
		displayName: 'US West',
		location: 'N. California',
	},
	{
		name: 'us-west-2',
		displayName: 'US West',
		location: 'Oregon',
	},
	{
		name: 'us-gov-west-1',
		displayName: 'US West',
		location: 'GovCloud',
	},
] as const;

export type AWSRegion = (typeof regions)[number]['name'];

export type AwsCredentialsTypeBase = {
	region: AWSRegion;
	customEndpoints: boolean;
	rekognitionEndpoint?: string;
	lambdaEndpoint?: string;
	snsEndpoint?: string;
	sesEndpoint?: string;
	sqsEndpoint?: string;
	s3Endpoint?: string;
	ssmEndpoint?: string;
};

export type AwsIamCredentialsType = AwsCredentialsTypeBase & {
	accessKeyId: string;
	secretAccessKey: string;
	temporaryCredentials: boolean;
	sessionToken?: string;
};

export type AwsAssumeRoleCredentialsType = AwsCredentialsTypeBase & {
	assumeRole?: boolean;
	roleArn?: string;
	externalId?: string;
	roleSessionName?: string;
	useSystemCredentialsForRole?: boolean;
	stsAccessKeyId?: string;
	stsSecretAccessKey?: string;
	stsSessionToken?: string;
};

export type AwsSecurityHeaders = {
	accessKeyId: string;
	secretAccessKey: string;
	sessionToken: string | undefined;
};

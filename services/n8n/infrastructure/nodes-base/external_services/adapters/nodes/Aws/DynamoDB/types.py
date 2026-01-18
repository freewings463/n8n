"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/DynamoDB/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/DynamoDB 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:IRequestBody、IAttributeValue、IAttributeValueValue、IAttributeValueUi、IAttributeNameUi、AttributeValueType、PartitionKey、EAttributeValueTypes 等5项。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/DynamoDB/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/DynamoDB/types.py

export interface IRequestBody {
	[key: string]: string | IAttributeValue | undefined | boolean | object | number;
	TableName: string;
	Key?: object;
	IndexName?: string;
	ProjectionExpression?: string;
	KeyConditionExpression?: string;
	ExpressionAttributeValues?: IAttributeValue;
	ConsistentRead?: boolean;
	FilterExpression?: string;
	Limit?: number;
	ExclusiveStartKey?: IAttributeValue;
}

export interface IAttributeValue {
	[attribute: string]: IAttributeValueValue;
}

export interface IAttributeValueValue {
	[type: string]: string | string[] | IAttributeValue[];
}

export interface IAttributeValueUi {
	attribute: string;
	type: AttributeValueType;
	value: string;
}

export interface IAttributeNameUi {
	key: string;
	value: string;
}

export type AttributeValueType =
	| 'B' // binary
	| 'BOOL' // boolean
	| 'BS' // binary set
	| 'L' // list
	| 'M' // map
	| 'N' // number
	| 'NULL'
	| 'NS' // number set
	| 'S' // string
	| 'SS'; // string set

export type PartitionKey = {
	details: {
		name: string;
		type: string;
		value: string;
	};
};

export const EAttributeValueTypes = {
	S: 'S',
	SS: 'SS',
	M: 'M',
	L: 'L',
	NS: 'NS',
	N: 'N',
	BOOL: 'BOOL',
	B: 'B',
	BS: 'BS',
	NULL: 'NULL',
} as const;

export type EAttributeValueType = (typeof EAttributeValueTypes)[keyof typeof EAttributeValueTypes];

export interface IExpressionAttributeValue {
	attribute: string;
	type: EAttributeValueType;
	value: string;
}

export type FieldsUiValues = Array<{
	fieldId: string;
	fieldValue: string;
}>;

export type PutItemUi = {
	attribute: string;
	type: 'S' | 'N';
	value: string;
};

export type AdjustedPutItem = {
	[attribute: string]: {
		[type: string]: string;
	};
};

"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/RabbitMQ/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/RabbitMQ 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:Options、TriggerOptions、RabbitMQCredentials、ExchangeType。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/RabbitMQ/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/RabbitMQ/types.py

type Argument = {
	key: string;
	value?: string;
};

type Binding = {
	exchange: string;
	routingKey: string;
};

type Header = {
	key: string;
	value?: string;
};

export type Options = {
	autoDelete: boolean;
	assertExchange: boolean;
	assertQueue: boolean;
	durable: boolean;
	exclusive: boolean;
	arguments: {
		argument: Argument[];
	};
	headers: {
		header: Header[];
	};
};

type ContentOptions =
	| {
			contentIsBinary: true;
	  }
	| {
			contentIsBinary: false;
			jsonParseBody: boolean;
			onlyContent: boolean;
	  };

export type TriggerOptions = Options & {
	acknowledge:
		| 'executionFinishes'
		| 'executionFinishesSuccessfully'
		| 'immediately'
		| 'laterMessageNode';
	parallelMessages: number;
	binding: {
		bindings: Binding[];
	};
} & ContentOptions;

export type RabbitMQCredentials = {
	hostname: string;
	port: number;
	username: string;
	password: string;
	vhost: string;
} & (
	| { ssl: false }
	| ({ ssl: true; ca: string } & (
			| { passwordless: false }
			| {
					passwordless: true;
					cert: string;
					key: string;
					passphrase: string;
			  }
	  ))
);

export type ExchangeType = 'direct' | 'topic' | 'headers' | 'fanout';

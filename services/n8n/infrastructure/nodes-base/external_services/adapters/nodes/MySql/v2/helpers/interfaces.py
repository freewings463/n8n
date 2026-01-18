"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MySql/v2/helpers/interfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MySql/v2 的节点。导入/依赖:外部:mysql2/promise；内部:n8n-workflow；本地:无。导出:Mysql2Connection、Mysql2Pool、Mysql2OkPacket、QueryValues、QueryWithValues、QueryRunner、WhereClause、SortRule 等7项。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MySql/v2/helpers/interfaces.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MySql/v2/helpers/interfaces.py

import type mysql2 from 'mysql2/promise';
import type { IDataObject, INodeExecutionData, SSHCredentials } from 'n8n-workflow';

export type Mysql2Connection = mysql2.Connection;
export type Mysql2Pool = mysql2.Pool;
export type Mysql2OkPacket = mysql2.OkPacket;

export type QueryValues = Array<string | number | IDataObject>;
export type QueryWithValues = { query: string; values: QueryValues };

export type QueryRunner = (queries: QueryWithValues[]) => Promise<INodeExecutionData[]>;

export type WhereClause = { column: string; condition: string; value: string | number };
export type SortRule = { column: string; direction: string };

export const AUTO_MAP = 'autoMapInputData';
const MANUAL = 'defineBelow';
export const DATA_MODE = {
	AUTO_MAP,
	MANUAL,
};

export const SINGLE = 'single';
const TRANSACTION = 'transaction';
const INDEPENDENTLY = 'independently';
export const BATCH_MODE = { SINGLE, TRANSACTION, INDEPENDENTLY };

export type QueryMode = typeof SINGLE | typeof TRANSACTION | typeof INDEPENDENTLY;

type WithSSL =
	| { ssl: false }
	| { ssl: true; caCertificate: string; clientCertificate: string; clientPrivateKey: string };

type WithSSHTunnel =
	| { sshTunnel: false }
	| ({
			sshTunnel: true;
	  } & SSHCredentials);

export type MysqlNodeCredentials = {
	host: string;
	port: number;
	database: string;
	user: string;
	password: string;
	connectTimeout: number;
} & WithSSL &
	WithSSHTunnel;

export type ParameterMatch = {
	match: string;
	index: number;
	paramNumber: string;
	isName: boolean;
};

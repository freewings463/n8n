"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MongoDb/mongoDb.types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MongoDb 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:IMongoParametricCredentials、IMongoOverrideCredentials、IMongoCredentialsType、IMongoCredentials。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。注释目标:Credentials object for Mongo, if using individual parameters。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MongoDb/mongoDb.types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MongoDb/mongoDb_types.py

/**
 * Credentials object for Mongo, if using individual parameters
 */
export interface IMongoParametricCredentials {
	/**
	 * Whether to allow overriding the parametric credentials with a connection string
	 */
	configurationType: 'values';

	host: string;
	database: string;
	user: string;
	password: string;
	port?: number;
}

/**
 * Credentials object for Mongo, if using override connection string
 */
export interface IMongoOverrideCredentials {
	/**
	 * Whether to allow overriding the parametric credentials with a connection string
	 */
	configurationType: 'connectionString';
	/**
	 * If using an override connection string, this is where it will be.
	 */
	connectionString: string;
	database: string;
}

/**
 * Unified credential object type (whether params are overridden with a connection string or not)
 */
export type IMongoCredentialsType = IMongoParametricCredentials | IMongoOverrideCredentials;

/**
 * Resolve the database and connection string from input credentials
 */
export type IMongoCredentials = {
	/**
	 * Database name (used to create the Mongo client)
	 */
	database: string;
	/**
	 * Generated connection string (after validating and figuring out overrides)
	 */
	connectionString: string;
};

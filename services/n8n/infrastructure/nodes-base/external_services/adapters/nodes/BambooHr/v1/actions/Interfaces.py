"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/BambooHr/v1/actions/Interfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/BambooHr/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:BambooHr、BambooHrFile、BambooHrEmployee、BambooHrEmployeeDocument、BambooHrCompanyReport、FileProperties、EmployeeProperties、EmployeeDocumentProperties 等2项。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/BambooHr/v1/actions/Interfaces.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/BambooHr/v1/actions/Interfaces.py

import type { AllEntities, Entity, PropertiesOf } from 'n8n-workflow';

type BambooHrMap = {
	employee: 'create' | 'get' | 'getAll' | 'update';
	employeeDocument: 'delete' | 'download' | 'get' | 'getAll' | 'update' | 'upload';
	file: 'delete' | 'download' | 'getAll' | 'update';
	companyReport: 'get';
};

export type BambooHr = AllEntities<BambooHrMap>;

export type BambooHrFile = Entity<BambooHrMap, 'file'>;
export type BambooHrEmployee = Entity<BambooHrMap, 'employee'>;
export type BambooHrEmployeeDocument = Entity<BambooHrMap, 'employeeDocument'>;
export type BambooHrCompanyReport = Entity<BambooHrMap, 'companyReport'>;

export type FileProperties = PropertiesOf<BambooHrFile>;
export type EmployeeProperties = PropertiesOf<BambooHrEmployee>;
export type EmployeeDocumentProperties = PropertiesOf<BambooHrEmployeeDocument>;
export type CompanyReportProperties = PropertiesOf<BambooHrCompanyReport>;

export interface IAttachment {
	fields: {
		item?: object[];
	};
	actions: {
		item?: object[];
	};
}

"""
MIGRATION-META:
  source_path: packages/cli/src/modules/community-packages/installed-nodes.entity.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/community-packages 的模块。导入/依赖:外部:无；内部:@n8n/typeorm；本地:./installed-packages.entity。导出:InstalledNodes。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/community-packages/installed-nodes.entity.ts -> services/n8n/infrastructure/cli/persistence/models/modules/community-packages/installed_nodes_entity.py

import { BaseEntity, Column, Entity, JoinColumn, ManyToOne, PrimaryColumn } from '@n8n/typeorm';

import { InstalledPackages } from './installed-packages.entity';

@Entity()
export class InstalledNodes extends BaseEntity {
	@Column()
	name: string;

	@PrimaryColumn()
	type: string;

	@Column()
	latestVersion: number;

	@ManyToOne('InstalledPackages', 'installedNodes')
	@JoinColumn({ name: 'package', referencedColumnName: 'packageName' })
	package: InstalledPackages;
}

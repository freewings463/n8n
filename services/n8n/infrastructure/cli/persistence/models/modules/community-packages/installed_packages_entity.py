"""
MIGRATION-META:
  source_path: packages/cli/src/modules/community-packages/installed-packages.entity.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/community-packages 的模块。导入/依赖:外部:无；内部:@n8n/db、@n8n/typeorm；本地:./installed-nodes.entity。导出:InstalledPackages。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/community-packages/installed-packages.entity.ts -> services/n8n/infrastructure/cli/persistence/models/modules/community-packages/installed_packages_entity.py

import { WithTimestamps } from '@n8n/db';
import { Column, Entity, JoinColumn, OneToMany, PrimaryColumn } from '@n8n/typeorm';

import type { InstalledNodes } from './installed-nodes.entity';

@Entity()
export class InstalledPackages extends WithTimestamps {
	@PrimaryColumn()
	packageName: string;

	@Column()
	installedVersion: string;

	@Column()
	authorName?: string;

	@Column()
	authorEmail?: string;

	@OneToMany('InstalledNodes', 'package')
	@JoinColumn({ referencedColumnName: 'package' })
	installedNodes: InstalledNodes[];
}

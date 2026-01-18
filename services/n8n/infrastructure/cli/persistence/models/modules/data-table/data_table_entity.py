"""
MIGRATION-META:
  source_path: packages/cli/src/modules/data-table/data-table.entity.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/data-table 的模块。导入/依赖:外部:无；内部:@n8n/db、@n8n/typeorm；本地:./data-table-column.entity。导出:DataTable。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/data-table/data-table.entity.ts -> services/n8n/infrastructure/cli/persistence/models/modules/data-table/data_table_entity.py

import { Project, WithTimestampsAndStringId } from '@n8n/db';
import { Column, Entity, Index, JoinColumn, ManyToOne, OneToMany } from '@n8n/typeorm';

import { DataTableColumn } from './data-table-column.entity';

@Entity()
@Index(['name', 'projectId'], { unique: true })
export class DataTable extends WithTimestampsAndStringId {
	constructor() {
		super();
	}

	@Column()
	name: string;

	@OneToMany(
		() => DataTableColumn,
		(dataTableColumn) => dataTableColumn.dataTable,
		{
			cascade: true,
		},
	)
	columns: DataTableColumn[];

	@ManyToOne(() => Project)
	@JoinColumn({ name: 'projectId' })
	project: Project;

	@Column()
	projectId: string;
}

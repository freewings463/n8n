"""
MIGRATION-META:
  source_path: packages/cli/src/modules/data-table/data-table-column.entity.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/data-table 的模块。导入/依赖:外部:无；内部:@n8n/db、@n8n/typeorm；本地:./data-table.entity。导出:DataTableColumn。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/data-table/data-table-column.entity.ts -> services/n8n/infrastructure/cli/persistence/models/modules/data-table/data_table_column_entity.py

import { WithTimestampsAndStringId } from '@n8n/db';
import { Column, Entity, Index, JoinColumn, ManyToOne } from '@n8n/typeorm';

import { type DataTable } from './data-table.entity';

@Entity()
@Index(['dataTableId', 'name'], { unique: true })
export class DataTableColumn extends WithTimestampsAndStringId {
	@Column()
	dataTableId: string;

	@Column()
	name: string;

	@Column({ type: 'varchar' })
	type: 'string' | 'number' | 'boolean' | 'date';

	@Column({ type: 'int' })
	index: number;

	@ManyToOne('DataTable', 'columns')
	@JoinColumn({ name: 'dataTableId' })
	dataTable: DataTable;
}

"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/command/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src/command 的类型。导入/依赖:外部:zod；内部:@n8n/di；本地:无。导出:CommandOptions、ICommand、CommandClass、CommandEntry。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/command/types.ts -> services/n8n/infrastructure/n8n-decorators/container/src/command/types.py

import type { Constructable } from '@n8n/di';
import type { ZodObject, ZodTypeAny } from 'zod';

type FlagsSchema = ZodObject<Record<string, ZodTypeAny>>;

export type CommandOptions = {
	name: string;
	description: string;
	examples?: string[];
	flagsSchema?: FlagsSchema;
};

export type ICommand = {
	flags?: object;
	init?: () => Promise<void>;
	run: () => Promise<void>;
	catch?: (e: Error) => Promise<void>;
	finally?: (e?: Error) => Promise<void>;
};

export type CommandClass = Constructable<ICommand>;

export type CommandEntry = {
	class: CommandClass;
	description: string;
	examples?: string[];
	flagsSchema?: FlagsSchema;
};

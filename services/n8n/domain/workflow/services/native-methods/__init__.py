"""
MIGRATION-META:
  source_path: packages/workflow/src/native-methods/index.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/native-methods 的工作流入口。导入/依赖:外部:无；内部:无；本地:./array.methods、./boolean.methods、./number.methods、./object.methods 等2项。导出:NATIVE_METHODS。关键函数/方法:无。用于汇总导出并完成工作流模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/native-methods/index.ts -> services/n8n/domain/workflow/services/native-methods/__init__.py

import { arrayMethods } from './array.methods';
import { booleanMethods } from './boolean.methods';
import { numberMethods } from './number.methods';
import { objectMethods } from './object.methods';
import { stringMethods } from './string.methods';
import type { NativeDoc } from '../extensions/extensions';

const NATIVE_METHODS: NativeDoc[] = [
	stringMethods,
	arrayMethods,
	numberMethods,
	objectMethods,
	booleanMethods,
];

export { NATIVE_METHODS as NativeMethods };

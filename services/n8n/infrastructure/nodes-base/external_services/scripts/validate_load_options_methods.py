"""
MIGRATION-META:
  source_path: packages/nodes-base/scripts/validate-load-options-methods.js
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/scripts 的模块。导入/依赖:外部:无；内部:无；本地:../methods/referenced.json、../methods/defined.json。导出:无。关键函数/方法:compareMethods。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/scripts/validate-load-options-methods.js -> services/n8n/infrastructure/nodes-base/external_services/scripts/validate_load_options_methods.py

let referencedMethods;
let definedMethods;

try {
	referencedMethods = require('../dist/methods/referenced.json');
	definedMethods = require('../dist/methods/defined.json');
} catch (error) {
	console.error(
		'Failed to find methods to validate. Please run `npm run n8n-generate-metadata` first.',
	);
	process.exit(1);
}

const compareMethods = (base, other) => {
	const result = [];

	for (const [nodeName, methods] of Object.entries(base)) {
		if (nodeName in other) {
			const found = methods.filter((item) => !other[nodeName].includes(item));

			if (found.length > 0) result.push({ [nodeName]: found });
		}
	}

	return result;
};

const referencedButUndefined = compareMethods(referencedMethods, definedMethods);

if (referencedButUndefined.length > 0) {
	console.error('ERROR: The following load options methods are referenced but undefined.');
	console.error('Please fix or remove the references or define the methods.');
	console.error(referencedButUndefined);
	process.exit(1);
}

const definedButUnused = compareMethods(definedMethods, referencedMethods);

if (definedButUnused.length > 0) {
	console.warn('Warning: The following load options methods are defined but unused.');
	console.warn('Please consider using or removing the methods.');
	console.warn(definedButUnused);
}

"""
MIGRATION-META:
  source_path: packages/@n8n/task-runner/src/node-types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/task-runner/src 的类型。导入/依赖:外部:无；内部:无；本地:./runner-types。导出:DEFAULT_NODETYPE_VERSION、TaskRunnerNodeTypes。关键函数/方法:parseNodeTypes、getByName、getByNameAndVersion、getKnownTypes、addNodeTypeDescriptions、onlyUnknown。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/task-runner/src/node-types.ts -> services/n8n/infrastructure/n8n-task-runner/external_services/adapters/nodes/node_types.py

import {
	ApplicationError,
	type IDataObject,
	type INodeType,
	type INodeTypeDescription,
	type INodeTypes,
	type IVersionedNodeType,
} from 'n8n-workflow';

import type { NeededNodeType } from './runner-types';

type VersionedTypes = Map<number, INodeTypeDescription>;

export const DEFAULT_NODETYPE_VERSION = 1;

export class TaskRunnerNodeTypes implements INodeTypes {
	private nodeTypesByVersion: Map<string, VersionedTypes>;

	constructor(nodeTypes: INodeTypeDescription[]) {
		this.nodeTypesByVersion = this.parseNodeTypes(nodeTypes);
	}

	private parseNodeTypes(nodeTypes: INodeTypeDescription[]): Map<string, VersionedTypes> {
		const versionedTypes = new Map<string, VersionedTypes>();

		for (const nt of nodeTypes) {
			const versions = Array.isArray(nt.version)
				? nt.version
				: [nt.version ?? DEFAULT_NODETYPE_VERSION];

			const versioned: VersionedTypes =
				versionedTypes.get(nt.name) ?? new Map<number, INodeTypeDescription>();
			for (const version of versions) {
				versioned.set(version, { ...versioned.get(version), ...nt });
			}

			versionedTypes.set(nt.name, versioned);
		}

		return versionedTypes;
	}

	// This isn't used in Workflow from what I can see
	getByName(_nodeType: string): INodeType | IVersionedNodeType {
		throw new ApplicationError('Unimplemented `getByName`', { level: 'error' });
	}

	getByNameAndVersion(nodeType: string, version?: number): INodeType {
		const versions = this.nodeTypesByVersion.get(nodeType);
		if (!versions) {
			return undefined as unknown as INodeType;
		}
		const nodeVersion = versions.get(version ?? Math.max(...versions.keys()));
		if (!nodeVersion) {
			return undefined as unknown as INodeType;
		}
		return {
			description: nodeVersion,
		};
	}

	// This isn't used in Workflow from what I can see
	getKnownTypes(): IDataObject {
		throw new ApplicationError('Unimplemented `getKnownTypes`', { level: 'error' });
	}

	addNodeTypeDescriptions(nodeTypeDescriptions: INodeTypeDescription[]) {
		const newNodeTypes = this.parseNodeTypes(nodeTypeDescriptions);

		for (const [name, newVersions] of newNodeTypes.entries()) {
			if (!this.nodeTypesByVersion.has(name)) {
				this.nodeTypesByVersion.set(name, newVersions);
			} else {
				const existingVersions = this.nodeTypesByVersion.get(name)!;
				for (const [version, nodeType] of newVersions.entries()) {
					existingVersions.set(version, nodeType);
				}
			}
		}
	}

	/** Filter out node type versions that are already registered. */
	onlyUnknown(nodeTypes: NeededNodeType[]) {
		return nodeTypes.filter(({ name, version }) => {
			const existingVersions = this.nodeTypesByVersion.get(name);

			if (!existingVersions) return true;

			return !existingVersions.has(version);
		});
	}
}

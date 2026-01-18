"""
MIGRATION-META:
  source_path: packages/@n8n/extension-sdk/src/schema.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/extension-sdk/src 的模块。导入/依赖:外部:zod；内部:无；本地:无。导出:extensionManifestSchema、ExtensionManifest。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Extension SDK contracts/helpers -> presentation/dto
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/extension-sdk/src/schema.ts -> services/n8n/presentation/n8n-extension-sdk/dto/extension_sdk/schema.py

import { z } from 'zod';

/**
 * Schema for the extension configuration.
 */
export const extensionManifestSchema = z.object({
	/**
	 * Name of the extension package.
	 */
	name: z.string(),

	/**
	 * The display name of the extension.
	 */
	displayName: z.string(),

	/**
	 * Description of the extension package.
	 */
	description: z.string(),

	/**
	 * Publisher of the extension.
	 */
	publisher: z.string(),

	/**
	 * Version of the extension package.
	 */
	version: z.string(),

	/**
	 * Category the extension belongs to.
	 */
	categories: z.array(z.string()),

	/**
	 * Setup paths for backend and frontend code entry points.
	 */
	entry: z.object({
		/**
		 * Path to the backend entry file.
		 */
		backend: z.string(),
		/**
		 * Path to the frontend entry file.
		 */
		frontend: z.string(),
	}),

	/**
	 * Minimum SDK version required to run the extension.
	 */
	minSDKVersion: z.string(),

	/**
	 * Permissions object specifying allowed access for frontend and backend.
	 */
	permissions: z.object({
		/**
		 * List of frontend permissions (array of strings).
		 */
		frontend: z.array(z.string()),
		/**
		 * List of backend permissions (array of strings).
		 */
		backend: z.array(z.string()),
	}),

	/**
	 * List of events that the extension listens to.
	 */
	events: z.array(z.string()),

	/**
	 * Define extension points for existing functionalities.
	 */
	extends: z.object({
		/**
		 * Extends the views configuration.
		 */
		views: z.object({
			/**
			 * Extends the workflows view configuration.
			 */
			workflows: z.object({
				/**
				 * Header component for the workflows view.
				 */
				header: z.string(),
			}),
		}),
	}),
});

export type ExtensionManifest = z.infer<typeof extensionManifestSchema>;

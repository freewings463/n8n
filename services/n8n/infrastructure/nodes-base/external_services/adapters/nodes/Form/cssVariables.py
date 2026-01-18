"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Form/cssVariables.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Form 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:cssVariables。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Form/cssVariables.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Form/cssVariables.py

export const cssVariables = `
:root {
	--font-family: 'Open Sans', sans-serif;
	--font-weight-normal: 400;
	--font-weight-bold: 600;
	--font-size-body: 12px;
	--font-size-label: 14px;
	--font-size-test-notice: 12px;
	--font-size-input: 14px;
	--font-size-header: 20px;
	--font-size-paragraph: 14px;
	--font-size-link: 12px;
	--font-size-error: 12px;
	--font-size-html-h1: 28px;
	--font-size-html-h2: 20px;
	--font-size-html-h3: 16px;
	--font-size-html-h4: 14px;
	--font-size-html-h5: 12px;
	--font-size-html-h6: 10px;
	--font-size-subheader: 14px;

	/* Colors */
	--color-background: #fbfcfe;
	--color-test-notice-text: #e6a23d;
	--color-test-notice-bg: #fefaf6;
	--color-test-notice-border: #f6dcb7;
	--color-card-bg: #ffffff;
	--color-card-border: #dbdfe7;
	--color-card-shadow: rgba(99, 77, 255, 0.06);
	--color-link: #7e8186;
	--color-header: #525356;
	--color-label: #555555;
	--color-input-border: #dbdfe7;
	--color-input-text: #71747A;
	--color-focus-border: rgb(90, 76, 194);
	--color-submit-btn-bg: #ff6d5a;
	--color-submit-btn-text: #ffffff;
	--color-error: #ea1f30;
	--color-required: #ff6d5a;
	--color-clear-button-bg: #7e8186;
	--color-html-text: #555;
	--color-html-link: #ff6d5a;
	--color-header-subtext: #7e8186;

	/* Border Radii */
	--border-radius-card: 8px;
	--border-radius-input: 6px;
	--border-radius-clear-btn: 50%;
	--card-border-radius: 8px;

	/* Spacing */
	--padding-container-top: 24px;
	--padding-card: 24px;
	--padding-test-notice-vertical: 12px;
	--padding-test-notice-horizontal: 24px;
	--margin-bottom-card: 16px;
	--padding-form-input: 12px;
	--card-padding: 24px;
	--card-margin-bottom: 16px;

	/* Dimensions */
	--container-width: 448px;
	--submit-btn-height: 48px;
	--checkbox-size: 18px;

	/* Others */
	--box-shadow-card: 0px 4px 16px 0px var(--color-card-shadow);
	--opacity-placeholder: 0.5;
}
`;

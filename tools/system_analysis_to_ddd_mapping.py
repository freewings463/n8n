#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class SourceRow:
	source_path: str
	responsibility: str


@dataclass(frozen=True)
class DddTarget:
	target_context: str
	target_layer: str  # Domain|Application|Interface|Infrastructure
	new_path: str
	reason: str
	confidence: str  # High|Medium|Low


SYSTEM_ANALYSIS_ROW_RE = re.compile(r"^\| `([^`]+)` \| (.*) \|\s*$")
SYSTEM_ANALYSIS_TIME_RE = re.compile(r"^- 生成时间: (.+)$")


def _to_service_name(package_id: str) -> str:
	normalized = package_id.replace("@n8n/", "n8n-")
	normalized = normalized.replace("/", "-")
	normalized = normalized.replace(".", "-")
	return normalized.lower()


def _to_python_module_filename(filename: str) -> str:
	# Keep mapping deterministic and human-friendly. (Not perfect import semantics.)
	if filename in {"index.ts", "index.tsx", "index.js", "index.mjs", "index.cjs"}:
		return "__init__.py"

	base = filename
	for ext in [
		".ts",
		".tsx",
		".js",
		".jsx",
		".mjs",
		".cjs",
		".vue",
	]:
		if base.endswith(ext):
			base = base[: -len(ext)]
			break

	base = base.replace("-", "_").replace(".", "_")
	return f"{base}.py"


def _parent_dir(posix_path: str) -> str:
	parent = Path(posix_path).parent.as_posix()
	return "" if parent == "." else parent


def _join_dir_file(base_dir: str, tail_path: str, filename: str) -> str:
	parent = _parent_dir(tail_path)
	if parent:
		return f"{base_dir}/{parent}/{filename}".replace("//", "/")
	return f"{base_dir}/{filename}".replace("//", "/")


def _package_id(source_path: str) -> str:
	parts = source_path.split("/")
	if len(parts) < 2 or parts[0] != "packages":
		return "unknown"
	if parts[1] == "@n8n":
		return f"@n8n/{parts[2]}" if len(parts) > 2 else "@n8n"
	return parts[1]


def _relative_to_package_root(source_path: str) -> str:
	parts = source_path.split("/")
	if len(parts) < 3 or parts[0] != "packages":
		return source_path
	if parts[1] == "@n8n":
		return "/".join(parts[3:]) if len(parts) > 3 else ""
	return "/".join(parts[2:])


def parse_system_analysis(path: Path) -> tuple[str | None, list[SourceRow]]:
	generated_at: str | None = None
	rows: list[SourceRow] = []

	for line in path.read_text(encoding="utf-8").splitlines():
		time_match = SYSTEM_ANALYSIS_TIME_RE.match(line.strip())
		if time_match and generated_at is None:
			generated_at = time_match.group(1).strip()

		row_match = SYSTEM_ANALYSIS_ROW_RE.match(line)
		if not row_match:
			continue
		rows.append(SourceRow(source_path=row_match.group(1), responsibility=row_match.group(2)))

	return generated_at, rows


def parse_ddd_structure(path: Path) -> set[str]:
	"""
	Extracts the full paths (relative to `services/{service-name}/`) from the first fenced code block
	in `ddd四层微服务目录结构-python.md`. Used to sanity-check that we only emit known top-level roots.
	"""
	text = path.read_text(encoding="utf-8")
	code_match = re.search(r"```\n(.*?)\n```", text, re.S)
	if not code_match:
		return set()

	lines = code_match.group(1).splitlines()
	stack: list[str] = []
	collected: set[str] = set()

	for line in lines:
		if line.startswith("services/{service-name}/"):
			stack = ["services/{service-name}"]
			continue

		node_index = None
		for token in ("├── ", "└── "):
			if token in line:
				node_index = line.index(token)
				break
		if node_index is None:
			continue

		depth = node_index // 4
		name = line[node_index + 4 :]
		name = name.split("#", 1)[0].rstrip()
		if not name:
			continue

		if depth + 1 > len(stack):
			stack.extend([""] * (depth + 1 - len(stack)))
		stack = stack[: depth + 1]
		stack.append(name.rstrip("/"))
		full = "/".join(stack[1:])
		collected.add(full)

	return collected


def _target(
	context: str,
	layer: str,
	ddd_rel_path: str,
	*,
	reason: str,
	confidence: str,
) -> DddTarget:
	new_path = f"services/{context}/{ddd_rel_path}".rstrip("/")
	return DddTarget(
		target_context=context,
		target_layer=layer,
		new_path=new_path,
		reason=reason,
		confidence=confidence,
	)


def map_row_to_ddd(row: SourceRow) -> DddTarget:
	pkg = _package_id(row.source_path)
	context = _to_service_name(pkg)
	rel = _relative_to_package_root(row.source_path)
	filename = Path(row.source_path).name
	py_filename = _to_python_module_filename(filename)

	# --- Package-first special cases (clear boundaries) ---
	if pkg == "@n8n/api-types":
		# Shared request/response DTO contracts (FE/BE).
		if not rel.startswith("src/"):
			return _target(
				context,
				"Infrastructure",
				rel,
				reason="Package @n8n/api-types tooling/config -> service root",
				confidence="Medium",
			)
		rel_tail = rel[len("src/") :]
		return _target(
			context,
			"Interface",
			_join_dir_file("presentation/dto", rel_tail, py_filename),
			reason="Package @n8n/api-types treated as presentation DTO contracts",
			confidence="High",
		)

	if pkg == "@n8n/db":
		# Persistence implementation package.
		if not rel.startswith("src/"):
			return _target(
				context,
				"Infrastructure",
				rel,
				reason="Package @n8n/db tooling/config -> service root",
				confidence="Medium",
			)
		if rel.startswith("src/entities/"):
			tail = rel[len("src/entities/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/persistence/models", tail, py_filename),
				reason="DB entity -> infrastructure/persistence/models",
				confidence="High",
			)
		if rel.startswith("src/repositories/"):
			tail = rel[len("src/repositories/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/persistence/repositories", tail, py_filename),
				reason="Repository implementation -> infrastructure/persistence/repositories",
				confidence="High",
			)
		if rel.startswith("src/migrations/"):
			tail = rel[len("src/migrations/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/persistence/migrations", tail, py_filename),
				reason="Migration -> infrastructure/persistence/migrations",
				confidence="High",
			)
		tail = rel[len("src/") :]
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("infrastructure/persistence", tail, py_filename),
			reason="Package @n8n/db defaulted to persistence infrastructure",
			confidence="Medium",
		)

	if pkg in {"nodes-base", "@n8n/nodes-langchain"}:
		# Integration implementations & credentials for external systems.
		if rel.startswith("credentials/"):
			tail = rel[len("credentials/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/external_services/adapters/credentials", tail, py_filename),
				reason="Credentials definition -> external_services adapters (ACL)",
				confidence="High",
			)
		if rel.startswith("nodes/"):
			tail = rel[len("nodes/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/external_services/adapters/nodes", tail, py_filename),
				reason="Node integration -> external_services adapters (ACL)",
				confidence="High",
			)
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("infrastructure/external_services", rel, py_filename),
			reason="Integration package defaulted to infrastructure/external_services",
			confidence="Medium",
		)

	if pkg == "@n8n/errors":
		tail = rel[len("src/") :] if rel.startswith("src/") else rel
		return _target(
			context,
			"Domain",
			_join_dir_file("domain/exceptions", tail, py_filename),
			reason="Shared error types -> domain/exceptions",
			confidence="High",
		)

	if pkg == "workflow":
		rel_tail = rel[len("src/") :] if rel.startswith("src/") else rel
		if "/errors/" in f"/{rel_tail}/":
			tail = rel_tail.split("errors/", 1)[1]
			return _target(
				context,
				"Domain",
				_join_dir_file("domain/exceptions", tail, py_filename),
				reason="Workflow errors -> domain/exceptions",
				confidence="High",
			)
		return _target(
			context,
			"Domain",
			_join_dir_file("domain/services", rel_tail, py_filename),
			reason="Package workflow treated as domain model & rules",
			confidence="Medium",
		)

	# Package root files (usually tooling/config) map to service root.
	if "/" not in rel:
		return _target(
			context,
			"Infrastructure",
			rel,
			reason="Package root file -> service root (tooling/config)",
			confidence="Medium",
		)

	# --- Path-first (framework-independent) rules ---
	rel_norm = f"/{rel}/"

	# Entry points / CLI
	if pkg == "cli" and rel.startswith("bin/") and filename in {"n8n", "n8n.cmd"}:
		return _target(
			context,
			"Infrastructure",
			"main.py",
			reason="CLI binary entrypoint -> main.py (BOOT)",
			confidence="High",
		)

	if rel.startswith("bin/"):
		tail = rel[len("bin/") :]
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("infrastructure/container/bin", tail, py_filename),
			reason="Management/build script -> infrastructure/container/bin",
			confidence="Medium",
		)

	if rel.startswith("src/commands/"):
		tail = rel[len("src/commands/") :]
		is_cli_package = pkg in {"cli", "node-dev", "@n8n/node-cli", "@n8n/benchmark", "@n8n/create-node"} or pkg.endswith(
			"cli"
		)
		if is_cli_package:
			return _target(
				context,
				"Interface",
				_join_dir_file("presentation/cli/commands", tail, py_filename),
				reason="CLI command -> presentation/cli/commands",
				confidence="High" if pkg == "cli" else "Medium",
			)

		return _target(
			context,
			"Application",
			_join_dir_file("application/commands/handlers", tail, py_filename),
			reason="Command handler -> application/commands/handlers",
			confidence="Medium",
		)

	# Interface / HTTP adapter
	if "/controllers/" in rel_norm or rel.startswith("src/controllers/"):
		tail = rel.split("controllers/", 1)[-1]
		return _target(
			context,
			"Interface",
			_join_dir_file("presentation/api/v1/controllers", tail, py_filename),
			reason="Controller -> presentation/api/v1/controllers",
			confidence="High",
		)

	if "/middlewares/" in rel_norm or "/middleware/" in rel_norm:
		tail = rel.split("middlewares/", 1)[-1]
		tail = tail.split("middleware/", 1)[-1]
		return _target(
			context,
			"Interface",
			_join_dir_file("presentation/api/middleware", tail, py_filename),
			reason="Middleware -> presentation/api/middleware",
			confidence="High",
		)

	if rel.startswith("src/public-api/"):
		tail = rel[len("src/public-api/") :]
		return _target(
			context,
			"Interface",
			_join_dir_file("presentation/api", tail, py_filename),
			reason="Public API adapter -> presentation/api/*",
			confidence="High",
		)

	if "/webhooks/" in rel_norm or rel.startswith("src/webhooks/"):
		tail = rel.split("webhooks/", 1)[-1]
		return _target(
			context,
			"Interface",
			_join_dir_file("presentation/api/v1/controllers/webhooks", tail, py_filename),
			reason="Webhook HTTP entry -> presentation/api/v1/controllers/webhooks",
			confidence="High",
		)

	# Persistence infrastructure
	if "/databases/" in rel_norm or "/repositories/" in rel_norm or "/migrations/" in rel_norm:
		if "/entities/" in rel_norm:
			tail = rel.split("entities/", 1)[-1]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/persistence/models", tail, py_filename),
				reason="DB entity -> infrastructure/persistence/models",
				confidence="High",
			)
		if "/repositories/" in rel_norm:
			tail = rel.split("repositories/", 1)[-1]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/persistence/repositories", tail, py_filename),
				reason="Repository -> infrastructure/persistence/repositories",
				confidence="High",
			)
		if "/migrations/" in rel_norm:
			tail = rel.split("migrations/", 1)[-1]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/persistence/migrations", tail, py_filename),
				reason="Migration -> infrastructure/persistence/migrations",
				confidence="High",
			)
		tail = rel.split("databases/", 1)[-1]
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("infrastructure/persistence", tail, py_filename),
			reason="Persistence-related path -> infrastructure/persistence/*",
			confidence="Medium",
		)

	# Infrastructure: configuration / monitoring / messaging / container
	if "/config/" in rel_norm or "/configs/" in rel_norm:
		tail = rel.split("config/", 1)[-1]
		tail = tail.split("configs/", 1)[-1]
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("infrastructure/configuration", tail, py_filename),
			reason="Config -> infrastructure/configuration",
			confidence="High",
		)

	if "/eventbus/" in rel_norm or "/events/" in rel_norm:
		tail = rel.split("eventbus/", 1)[-1]
		tail = tail.split("events/", 1)[-1]
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("infrastructure/event_bus", tail, py_filename),
			reason="Event bus / events plumbing -> infrastructure/event_bus",
			confidence="Medium",
		)

	if any(token in rel_norm for token in ["/telemetry/", "/metrics/", "/posthog/", "/logging/", "/tracing/"]):
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("infrastructure/monitoring", rel, py_filename),
			reason="Telemetry/metrics -> infrastructure/monitoring",
			confidence="Medium",
		)

	if "/di/" in rel_norm or "/container/" in rel_norm or pkg in {"@n8n/di", "@n8n/decorators"}:
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("infrastructure/container", rel, py_filename),
			reason="DI/container wiring -> infrastructure/container",
			confidence="Medium",
		)

	# Application services (default for backend business orchestration)
	if "/services/" in rel_norm or "/modules/" in rel_norm:
		tail = rel.split("services/", 1)[-1]
		tail = tail.split("modules/", 1)[-1]
		return _target(
			context,
			"Application",
			_join_dir_file("application/services", tail, py_filename),
			reason="Service/module orchestration -> application/services",
			confidence="Medium",
		)

	# Domain errors
	if "/errors/" in rel_norm:
		tail = rel.split("errors/", 1)[-1]
		return _target(
			context,
			"Domain",
			_join_dir_file("domain/exceptions", tail, py_filename),
			reason="Error types -> domain/exceptions",
			confidence="Medium",
		)

	# Fallback: treat as application-level module.
	fallback_tail = rel[len("src/") :] if rel.startswith("src/") else rel
	return _target(
		context,
		"Application",
		_join_dir_file("application/services", fallback_tail, py_filename),
		reason="Fallback -> application/services (needs manual review)",
		confidence="Low",
	)


def _count_by_layer(mappings: Iterable[DddTarget]) -> Counter[str]:
	return Counter(m.target_layer for m in mappings)


def _majority_layer(counts: Counter[str]) -> tuple[str, str]:
	if not counts:
		return "Application", "Low"
	layer, top = counts.most_common(1)[0]
	total = sum(counts.values())
	ratio = top / total if total else 0
	confidence = "High" if ratio >= 0.7 else "Medium" if ratio >= 0.5 else "Low"
	return layer, confidence


def _md_escape(text: str) -> str:
	return text.replace("\n", " ").replace("\r", "").replace("|", "\\|").strip()


def build_file_mapping_md_tables(source_rows: list[SourceRow], file_mappings: list[DddTarget]) -> list[str]:
	by_package_rows: dict[str, list[int]] = defaultdict(list)
	for i, row in enumerate(source_rows):
		by_package_rows[_package_id(row.source_path)].append(i)

	lines: list[str] = []
	for pkg in sorted(by_package_rows.keys()):
		context = _to_service_name(pkg)
		lines.append(f"### `{pkg}` → `{context}`")
		lines.append("")
		lines.append("| old_path | new_path | target_context | target_layer | reason | confidence |")
		lines.append("|---------|----------|---------------|--------------|--------|------------|")
		for i in by_package_rows[pkg]:
			source = source_rows[i]
			target = file_mappings[i]
			lines.append(
				"| "
				+ " | ".join(
					[
						f"`{_md_escape(source.source_path)}`",
						f"`{_md_escape(target.new_path)}`",
						f"`{_md_escape(target.target_context)}`",
						f"`{_md_escape(target.target_layer)}`",
						_md_escape(target.reason),
						f"`{_md_escape(target.confidence)}`",
					]
				)
				+ " |"
			)
		lines.append("")

	return lines


def write_mapping_matrix_md(
	out_path: Path,
	*,
	generated_at: str | None,
	source_rows: list[SourceRow],
	file_mappings: list[DddTarget],
	ddd_structure: set[str],
) -> None:
	out_path.parent.mkdir(parents=True, exist_ok=True)

	by_package_rows: dict[str, list[int]] = defaultdict(list)
	for i, row in enumerate(source_rows):
		by_package_rows[_package_id(row.source_path)].append(i)

	# Package -> (layer counts)
	pkg_layer_counts: dict[str, Counter[str]] = {}
	for pkg, indices in by_package_rows.items():
		pkg_layer_counts[pkg] = _count_by_layer(file_mappings[i] for i in indices)

	# A minimal, keyword-driven responsibility summary per package.
	keywords = [
		"工作流",
		"执行",
		"节点",
		"凭证",
		"数据库",
		"迁移",
		"仓储",
		"控制器",
		"路由",
		"中间件",
		"配置",
		"加密",
		"事件",
		"消息",
		"缓存",
		"HTTP",
		"CLI",
		"类型",
		"schema",
		"test",
	]

	pkg_core: dict[str, str] = {}
	for pkg, indices in by_package_rows.items():
		text = " ".join(source_rows[i].responsibility for i in indices)
		counts = [(kw, text.count(kw)) for kw in keywords]
		counts = [(kw, n) for kw, n in counts if n > 0]
		counts.sort(key=lambda x: (-x[1], x[0]))
		top = [kw for kw, _ in counts[:3]]
		if top:
			pkg_core[pkg] = f"关键词：{', '.join(top)}"
		else:
			pkg_core[pkg] = "（待补充：请基于职责摘要确认）"

	# Validate that top-level roots match template (best-effort).
	allowed_roots = {p.split("/")[0] for p in ddd_structure if p}
	root_warnings: list[str] = []
	for target in file_mappings:
		rel = target.new_path.split("/", 2)[-1] if target.new_path.startswith("services/") else ""
		root = rel.split("/", 1)[0] if rel else ""
		if root and allowed_roots and root not in allowed_roots:
			# The template enumerates only a subset of possible service-root files.
			is_file_like = "." in root or root in {"Dockerfile"}
			if not is_file_like:
				root_warnings.append(root)

	root_warning_text = ""
	if root_warnings:
		common = ", ".join(sorted(set(root_warnings))[:10])
		root_warning_text = f"\n> 注意：发现部分输出根目录不在模板顶层集合中：{common}（需人工复核规则）。\n"

	lines: list[str] = []
	lines.append("# DDD 迁移映射矩阵（由 系统分析.md 自动生成）")
	lines.append("")
	lines.append(f"- 源文档：`系统分析.md`（生成时间：{generated_at or '未知'}）")
	lines.append("- 目标模板：`ddd四层微服务目录结构-python.md`")
	lines.append("- 生成时间：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	lines.append(root_warning_text.rstrip())
	lines.append("")
	lines.append("## 本文档包含内容（单一真源）")
	lines.append("")
	lines.append("- 映射约定/规则（用于解释自动归类逻辑）")
	lines.append("- 包级映射矩阵：`packages/*` → `services/*` + DDD 四层")
	lines.append("- 文件级映射清单：包含 `系统分析.md` 中每个文件的 old_path→new_path（表格；按包分组）")
	lines.append("")
	lines.append("## 映射约定")
	lines.append("")
	lines.append("```mermaid")
	lines.append("flowchart LR")
	lines.append("  SA[系统分析.md\\n文件职责清单] --> RULES[映射规则]")
	lines.append("  RULES --> I[Interface\\npresentation/*]")
	lines.append("  RULES --> A[Application\\napplication/*]")
	lines.append("  RULES --> D[Domain\\ndomain/*]")
	lines.append("  RULES --> INF[Infrastructure\\ninfrastructure/*\\n+ service root files]")
	lines.append("  I --> OUT[映射矩阵.md]")
	lines.append("  A --> OUT")
	lines.append("  D --> OUT")
	lines.append("  INF --> OUT")
	lines.append("```")
	lines.append("")
	lines.append("- **目标上下文（target_context）**：默认按源路径的包名生成")
	lines.append("  - `packages/<pkg>/...` → `services/<pkg>/...`")
	lines.append("  - `packages/@n8n/<pkg>/...` → `services/n8n-<pkg>/...`（并将 `.` 转为 `-`）")
	lines.append("- **目标分层（target_layer）**：采用 `Domain|Application|Interface|Infrastructure` 四层")
	lines.append("  - DDD 模板中的 `presentation/*` → `Interface`")
	lines.append("  - DDD 模板中的 `infrastructure/*` 与服务根目录配置文件 → `Infrastructure`")
	lines.append("- **目标文件名**：为便于落到 Python 目录中，按如下规则做“占位式”转换")
	lines.append("  - `index.ts|js|...` → `__init__.py`")
	lines.append("  - 其他代码文件：扩展名转为 `.py`，并将 `-`、`.` 转为 `_`（不做 CamelCase 拆分）")
	lines.append("")
	lines.append("### 规则概览（按优先级）")
	lines.append("")
	lines.append("1. 包级强规则（高置信度）")
	lines.append("   - `@n8n/api-types` → `presentation/dto/**`（但包根配置文件 → 服务根目录）")
	lines.append("   - `@n8n/db` → `infrastructure/persistence/**`（entities/repositories/migrations 细分；包根配置文件 → 服务根目录）")
	lines.append("   - `nodes-base`、`@n8n/nodes-langchain` → `infrastructure/external_services/**`（credentials/nodes 细分）")
	lines.append("   - `@n8n/errors` → `domain/exceptions/**`")
	lines.append("   - `workflow` → `domain/services/**`（errors → `domain/exceptions/**`）")
	lines.append("2. 包根文件（通常为工具链/配置）")
	lines.append("   - `<package-root>/<file>` → `services/<context>/<file>`（标记为 `Infrastructure`）")
	lines.append("3. Interface（入站适配）")
	lines.append("   - `*/controllers/**` → `presentation/api/v1/controllers/**`")
	lines.append("   - `*/middlewares/**` 或 `*/middleware/**` → `presentation/api/middleware/**`")
	lines.append("   - `cli/src/public-api/**` → `presentation/api/**`")
	lines.append("   - `*/webhooks/**` → `presentation/api/v1/controllers/webhooks/**`")
	lines.append("   - `cli/bin/n8n|n8n.cmd` → `main.py`")
	lines.append("   - `*/src/commands/**`：CLI 类包 → `presentation/cli/commands/**`；非 CLI 包 → `application/commands/handlers/**`")
	lines.append("4. Infrastructure（出站/技术实现）")
	lines.append("   - `*/databases/**`、`*/repositories/**`、`*/migrations/**`、`*/entities/**` → `infrastructure/persistence/**`")
	lines.append("   - `*/config/**`、`*/configs/**` → `infrastructure/configuration/**`")
	lines.append("   - `*/eventbus/**`、`*/events/**` → `infrastructure/event_bus/**`")
	lines.append("   - `*/telemetry/**`、`*/metrics/**`、`*/posthog/**`、`*/logging/**`、`*/tracing/**` → `infrastructure/monitoring/**`")
	lines.append("   - `*/di/**`、`*/container/**` 或包为 `@n8n/di`、`@n8n/decorators` → `infrastructure/container/**`")
	lines.append("   - `*/bin/**`（非 `cli` 的 bin 脚本）→ `infrastructure/container/bin/**`")
	lines.append("5. Application（用例/编排，默认兜底）")
	lines.append("   - `*/services/**` 或 `*/modules/**` → `application/services/**`")
	lines.append("   - 其他未命中的代码文件 → `application/services/**`（`confidence=Low`，需人工复核）")
	lines.append("")
	lines.append("> 说明：该映射为“预重构”阶段的启发式归类；正式迁移批次仍需按职责/依赖关系人工复核与拆分。")
	lines.append("")

	lines.append("## 映射矩阵（包级）")
	lines.append("")
	lines.append("| 原模块/包名 | 核心职责 | 对应DDD上下文 | 对应分层 | 映射置信度 |")
	lines.append("|-------------|----------|---------------|----------|------------|")

	for pkg in sorted(by_package_rows.keys()):
		context = _to_service_name(pkg)
		layer, confidence = _majority_layer(pkg_layer_counts[pkg])
		lines.append(f"| `{pkg}` | {pkg_core[pkg]} | `{context}` | `{layer}` | `{confidence}` |")

	lines.append("")
	lines.append("## 置信度判定标准（简述）")
	lines.append("")
	lines.append("- `High`：清晰且占比≥70% 的分层归属（例如 DTO/DB/Integration 等包或目录结构强约束）")
	lines.append("- `Medium`：占比≥50% 或依赖/职责较一致，但仍存在明显混层或需人工复核")
	lines.append("- `Low`：无明显主层、职责混杂或大量回退规则命中")
	lines.append("")

	lines.append("## 文件级映射清单（按包分组；表格）")
	lines.append("")
	lines.extend(build_file_mapping_md_tables(source_rows, file_mappings))

	out_path.write_text("\n".join([line for line in lines if line is not None]), encoding="utf-8")


def write_batch_doc_md(
	out_path: Path,
	*,
	batch_id: str,
	source_generated_at: str | None,
	source_rows: list[SourceRow],
	file_mappings: list[DddTarget],
) -> None:
	out_path.parent.mkdir(parents=True, exist_ok=True)

	by_layer = _count_by_layer(file_mappings)
	by_context = Counter(m.target_context for m in file_mappings)

	lines: list[str] = []
	lines.append("---")
	lines.append("doc_type: migration_batch")
	lines.append(f"batch_id: \"{batch_id}\"")
	lines.append(f"date: \"{datetime.now().strftime('%Y-%m-%d')}\"")
	lines.append("owner: \"TBD\"")
	lines.append("base_commit: \"TBD\"")
	lines.append("status: planned")
	lines.append("scope:")
	lines.append("  bounded_contexts: [\"(auto from packages/*)\"]")
	lines.append("  layers: [\"Domain\", \"Application\", \"Interface\", \"Infrastructure\"]")
	lines.append("---")
	lines.append("")
	lines.append("# 系统分析 → DDD 四层映射（计划批次）")
	lines.append("")
	lines.append("## 1. 目标与非目标（Goals / Non-goals）")
	lines.append("")
	lines.append("- Goals：基于 `系统分析.md` 的职责摘要，生成文件级 old_path→new_path 映射，用于后续 DDD 预重构迁移。")
	lines.append("- Non-goals：本批次不移动任何代码文件、不修改业务逻辑、不做依赖收敛。")
	lines.append("")
	lines.append("## 2. 依赖分析摘要")
	lines.append("")
	lines.append("- 本批次仅生成映射文档，未进行依赖图构建（后续迁移批次需补齐依赖分析与顺序）。")
	lines.append("")
	lines.append("## 3. 变更清单（映射产物）")
	lines.append("")
	lines.append("| old_path | new_path | target_context | target_layer | reason | confidence |")
	lines.append("|---------|----------|---------------|--------------|--------|------------|")
	lines.append(
		"| （见 mapping-matrix.md 文件级映射清单） | `docs/migration/mapping-matrix.md` | （自动） | （四层） | 自动规则映射 | `Medium` |"
	)
	lines.append("")
	lines.append("## 4. 验证结果")
	lines.append("")
	lines.append("- 编译/启动：N/A（未移动代码）。")
	lines.append("- 测试：N/A（未移动代码）。")
	lines.append("- 架构约束：N/A（未迁移，后续批次补齐）。")
	lines.append("- 性能基线：N/A。")
	lines.append("")
	lines.append("## 5. 决策记录（Decisions）与遗留问题（Open Issues）")
	lines.append("")
	lines.append("- Decisions：按 `packages/<pkg>`（或 `packages/@n8n/<pkg>`）作为默认限界上下文名来源，映射到 `services/{context}/...`。")
	lines.append("- Open Issues：该规则为启发式；需对 `packages/cli`、`packages/core` 等混层包进行人工复核与拆分策略。")
	lines.append("")
	lines.append("## 6. 回退方案（Rollback）")
	lines.append("")
	lines.append("- 删除本批次生成的文档文件即可回退（无代码变更）。")
	lines.append("")
	lines.append("## 7. 下一批计划（Next）")
	lines.append("")
	lines.append("- 对高风险目录（例如 `packages/cli/src/services/**`）补充依赖分析与更细粒度的用例/领域划分。")
	lines.append("- 产出首个真实迁移批次：从叶子节点（依赖最少）开始 `git mv`。")
	lines.append("")
	lines.append("## 附录：统计")
	lines.append("")
	lines.append(f"- 源分析生成时间：{source_generated_at or '未知'}")
	lines.append(f"- 文件条目总数：{len(source_rows)}")
	lines.append(f"- Layer 统计：{dict(by_layer)}")
	lines.append(f"- Context Top10：{dict(by_context.most_common(10))}")
	lines.append("")

	out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("--system-analysis", default=Path("系统分析.md"), type=Path)
	parser.add_argument("--ddd-template", default=Path("ddd四层微服务目录结构-python.md"), type=Path)
	parser.add_argument("--out-dir", default=Path("docs/migration"), type=Path)
	parser.add_argument(
		"--batch-id",
		default=f"{datetime.now().strftime('%Y-%m-%d')}-system-analysis-ddd-mapping",
	)
	args = parser.parse_args()

	generated_at, rows = parse_system_analysis(args.system_analysis)
	ddd_structure = parse_ddd_structure(args.ddd_template)

	mapped = [map_row_to_ddd(r) for r in rows]

	matrix_path = args.out_dir / "mapping-matrix.md"
	write_mapping_matrix_md(
		matrix_path,
		generated_at=generated_at,
		source_rows=rows,
		file_mappings=mapped,
		ddd_structure=ddd_structure,
	)

	batch_path = args.out_dir / "batches" / f"{args.batch_id}.md"
	write_batch_doc_md(
		batch_path,
		batch_id=args.batch_id,
		source_generated_at=generated_at,
		source_rows=rows,
		file_mappings=mapped,
	)

	print(f"Wrote: {matrix_path}")
	print(f"Wrote: {batch_path}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())

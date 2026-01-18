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


@dataclass(frozen=True)
class ContextConfig:
	"""
	Controls how we derive `target_context` (i.e. microservice directory name).

	- single: collapse all packages into a single service, e.g. `services/n8n/...`
	- per-package: keep the previous behavior: `packages/<pkg>` -> `services/<pkg>/...`
	"""

	strategy: str  # single|per-package
	single_context: str = "n8n"


SYSTEM_ANALYSIS_ROW_RE = re.compile(r"^\| `([^`]+)` \| (.*) \|\s*$")
SYSTEM_ANALYSIS_TIME_RE = re.compile(r"^- 生成时间: (.+)$")

IMPORT_FROM_RE = re.compile(r"\bfrom\s+['\"]([^'\"]+)['\"]")
IMPORT_DYNAMIC_RE = re.compile(r"\bimport\(\s*['\"]([^'\"]+)['\"]\s*\)")
REQUIRE_RE = re.compile(r"\brequire\(\s*['\"]([^'\"]+)['\"]\s*\)")

TYPEORM_MODULE_MARKERS = ("typeorm", "@n8n/typeorm")
NODE_FS_MODULE_MARKERS = (
	"fs",
	"fs/promises",
	"node:fs",
	"node:fs/promises",
)
NODE_HTTP_MODULE_MARKERS = (
	"http",
	"https",
	"node:http",
	"node:https",
)
NODE_CHILD_PROCESS_MODULE_MARKERS = (
	"child_process",
	"node:child_process",
)
TEST_MODULE_MARKERS = (
	"@playwright/test",
	"playwright",
	"vitest",
	"jest",
	"@jest/globals",
	"mocha",
)
HTTP_CLIENT_MODULE_MARKERS = (
	"axios",
	"node-fetch",
	"undici",
	"got",
)


def _read_text_file(path: Path) -> str | None:
	try:
		return path.read_text(encoding="utf-8")
	except FileNotFoundError:
		return None
	except UnicodeDecodeError:
		return path.read_text(encoding="utf-8", errors="replace")


def _extract_import_modules(code: str) -> set[str]:
	modules: set[str] = set()
	for rx in (IMPORT_FROM_RE, IMPORT_DYNAMIC_RE, REQUIRE_RE):
		for m in rx.finditer(code):
			modules.add(m.group(1))
	return modules


def _has_typeorm_import(modules: set[str]) -> bool:
	return any(any(marker in m for marker in TYPEORM_MODULE_MARKERS) for m in modules)


def _has_any_module(modules: set[str], markers: tuple[str, ...]) -> bool:
	return any(m in modules for m in markers)


def _imports_node_fs(modules: set[str]) -> bool:
	return _has_any_module(modules, NODE_FS_MODULE_MARKERS)


def _imports_node_http(modules: set[str]) -> bool:
	return _has_any_module(modules, NODE_HTTP_MODULE_MARKERS)


def _imports_child_process(modules: set[str]) -> bool:
	return _has_any_module(modules, NODE_CHILD_PROCESS_MODULE_MARKERS)


def _looks_like_test_file(source_path: str, code: str | None, modules: set[str]) -> bool:
	path_norm = f"/{source_path}/"
	if any(token in path_norm for token in ["/__tests__/", "/test/", "/tests/", ".test.", ".spec."]):
		return True
	if _has_any_module(modules, TEST_MODULE_MARKERS):
		return True
	if code and re.search(r"\b(describe|it|test)\s*\(", code):
		return True
	if code and re.search(r"\bexpect\s*\(", code):
		return True
	return False


def _looks_like_express_adapter(code: str, modules: set[str]) -> bool:
	if "express" not in modules:
		return False
	# Broader than middleware: adapter helpers/types that touch Request/Response.
	return any(token in code for token in ("Request", "Response", "express.Request", "express.Response"))


def _looks_like_websocket_adapter(code: str, modules: set[str]) -> bool:
	if "ws" not in modules:
		return False
	return "WebSocket" in code


def _looks_like_xml_schema_resource(code: str, modules: set[str]) -> bool:
	return "xmllint-wasm" in modules and "XMLFileInfo" in code


def _looks_like_http_client(code: str, modules: set[str]) -> bool:
	if _has_any_module(modules, HTTP_CLIENT_MODULE_MARKERS):
		return True
	return "fetch(" in code


def _looks_like_controller(code: str, modules: set[str]) -> bool:
	if "@n8n/decorators" not in modules:
		return False
	return any(token in code for token in ("@RestController", "@Controller", "@RestController()", "@Controller()"))


def _looks_like_middleware(code: str, modules: set[str]) -> bool:
	if "express" not in modules:
		return False
	if "RequestHandler" in code or "NextFunction" in code:
		return True
	return bool(re.search(r"\(\s*req\s*,\s*res\s*,\s*next\s*\)", code))


def _looks_like_response_error(code: str) -> bool:
	if "ResponseError" not in code:
		return False
	return "extends ResponseError" in code or bool(re.search(r"\bclass\s+ResponseError\b", code))


def _looks_like_typeorm_entity(code: str, modules: set[str]) -> bool:
	return _has_typeorm_import(modules) and "@Entity" in code


def _looks_like_typeorm_migration(code: str, modules: set[str]) -> bool:
	if not _has_typeorm_import(modules):
		return False
	return "MigrationInterface" in code or "implements MigrationInterface" in code


def _looks_like_typeorm_repository(code: str, modules: set[str]) -> bool:
	if not _has_typeorm_import(modules):
		return False
	return any(token in code for token in ("extends Repository", "Repository<", "Repository ", "EntityManager"))


def _looks_like_n8n_credential(code: str, modules: set[str]) -> bool:
	return "n8n-workflow" in modules and "implements ICredentialType" in code


def _looks_like_n8n_node(code: str, modules: set[str]) -> bool:
	return "n8n-workflow" in modules and "implements INodeType" in code


def _has_di_service_decorator(code: str, modules: set[str]) -> bool:
	if "@n8n/di" not in modules:
		return False
	return "@Service" in code or "@Service()" in code


def _strip_prefix_once(text: str, prefix: str) -> str:
	return text[len(prefix) :] if text.startswith(prefix) else text


def _tail_after(rel: str, marker: str) -> str | None:
	needle = f"{marker}/"
	if needle in rel:
		return rel.split(needle, 1)[1]
	return None


def _to_service_name(package_id: str) -> str:
	normalized = package_id.replace("@n8n/", "n8n-")
	normalized = normalized.replace("/", "-")
	normalized = normalized.replace(".", "-")
	return normalized.lower()


def _resolve_target_context(package_id: str, config: ContextConfig) -> str:
	if config.strategy == "single":
		return config.single_context
	return _to_service_name(package_id)


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


def map_row_to_ddd(row: SourceRow, *, context_config: ContextConfig) -> DddTarget:
	pkg = _package_id(row.source_path)
	context = _resolve_target_context(pkg, context_config)
	rel = _relative_to_package_root(row.source_path)
	filename = Path(row.source_path).name
	py_filename = _to_python_module_filename(filename)
	code = _read_text_file(Path(row.source_path))
	modules = _extract_import_modules(code) if code else set()

	fallback_tail = _strip_prefix_once(rel, "src/")

	# --- Code-first classification (职责优先) ---
	if code:
		# Tests/non-production code: keep separate from DDD layers but classify as Infrastructure for matrix.
		if _looks_like_test_file(row.source_path, code, modules):
			test_tail = fallback_tail
			base_dir = "tests/unit"
			if "playwright" in rel or "@playwright/test" in modules or "/playwright/" in f"/{row.source_path}/":
				base_dir = "tests/integration/ui/playwright"
			elif any(token in f"/{row.source_path}/" for token in ["/e2e/", "/integration/"]):
				base_dir = "tests/integration"
			elif any(token in f"/{row.source_path}/" for token in ["/fixtures/"]):
				base_dir = "tests/fixtures"
			elif any(token in f"/{row.source_path}/" for token in ["/mocks/", "/test-utils/", "/test_utils/"]):
				base_dir = "tests/mocks"

			# Avoid duplicated directory segments (e.g. tests/.../playwright/playwright/...).
			if base_dir.endswith("/playwright") and test_tail.startswith("playwright/"):
				test_tail = test_tail[len("playwright/") :]

			return _target(
				context,
				"Infrastructure",
				_join_dir_file(base_dir, test_tail, py_filename),
				reason="Detected test/non-production code -> tests/*",
				confidence="High",
			)

		# Protocol adapters (beyond middleware): express/ws/http request wrappers.
		if _looks_like_middleware(code, modules):
			tail = _tail_after(rel, "middlewares") or _tail_after(rel, "middleware") or fallback_tail
			return _target(
				context,
				"Interface",
				_join_dir_file("presentation/api/middleware", tail, py_filename),
				reason="Detected Express RequestHandler-style middleware",
				confidence="High",
			)

		if _looks_like_express_adapter(code, modules):
			return _target(
				context,
				"Interface",
				_join_dir_file("presentation/api", fallback_tail, py_filename),
				reason="Detected Express Request/Response adapter/helper",
				confidence="Medium",
			)

		if _looks_like_websocket_adapter(code, modules):
			return _target(
				context,
				"Interface",
				_join_dir_file("presentation/api/ws", fallback_tail, py_filename),
				reason="Detected WebSocket adapter/types (ws)",
				confidence="Medium",
			)

		if _looks_like_controller(code, modules):
			tail = _tail_after(rel, "controllers") or fallback_tail
			return _target(
				context,
				"Interface",
				_join_dir_file("presentation/api/v1/controllers", tail, py_filename),
				reason="Detected @RestController/@Controller from @n8n/decorators",
				confidence="High",
			)

		if _looks_like_response_error(code):
			tail = _tail_after(rel, "errors") or fallback_tail
			return _target(
				context,
				"Interface",
				_join_dir_file("presentation/api/errors", tail, py_filename),
				reason="Detected ResponseError (HTTP-mapped error)",
				confidence="High",
			)

		if _looks_like_typeorm_entity(code, modules):
			tail = _tail_after(rel, "entities") or fallback_tail
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/persistence/models", tail, py_filename),
				reason="Detected TypeORM @Entity model",
				confidence="High",
			)

		if _looks_like_typeorm_migration(code, modules):
			tail = _tail_after(rel, "migrations") or fallback_tail
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/persistence/migrations", tail, py_filename),
				reason="Detected TypeORM MigrationInterface",
				confidence="High",
			)

		if _looks_like_typeorm_repository(code, modules):
			tail = _tail_after(rel, "repositories") or fallback_tail
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/persistence/repositories", tail, py_filename),
				reason="Detected TypeORM Repository/EntityManager usage",
				confidence="Medium",
			)

		if _looks_like_n8n_credential(code, modules):
			tail = _tail_after(rel, "credentials") or fallback_tail
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/external_services/adapters/credentials", tail, py_filename),
				reason="Detected ICredentialType adapter",
				confidence="High",
			)

		if _looks_like_n8n_node(code, modules):
			tail = _tail_after(rel, "nodes") or fallback_tail
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/external_services/adapters/nodes", tail, py_filename),
				reason="Detected INodeType adapter",
				confidence="High",
			)

		if _has_di_service_decorator(code, modules):
			tail = _tail_after(rel, "services") or _tail_after(rel, "modules") or fallback_tail
			return _target(
				context,
				"Application",
				_join_dir_file("application/services", tail, py_filename),
				reason="Detected @Service from @n8n/di",
				confidence="Medium",
			)

		if _looks_like_xml_schema_resource(code, modules):
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/configuration", fallback_tail, py_filename),
				reason="Detected XML schema resource (xmllint-wasm XMLFileInfo)",
				confidence="High",
			)

		# Node/runtime IO + external HTTP clients: infrastructure concerns.
		if _imports_node_fs(modules) or _imports_child_process(modules) or _imports_node_http(modules) or _looks_like_http_client(code, modules):
			base_dir = "infrastructure/container"
			reason = "Detected runtime IO/external interaction -> infrastructure/container"
			confidence = "Medium"
			io_tail = fallback_tail

			if "binary-data" in rel or "/binary-data/" in f"/{row.source_path}/":
				base_dir = "infrastructure/external_services/adapters/file_storage/binary_data"
				reason = "Detected binary data storage IO -> infrastructure file_storage adapter"
				confidence = "High"
				if io_tail.startswith("binary-data/"):
					io_tail = io_tail[len("binary-data/") :]
			elif any(token in f"/{row.source_path}/" for token in ["/crash", "/journal", "/logging", "/metrics", "/telemetry"]):
				base_dir = "infrastructure/monitoring"
				reason = "Detected crash/telemetry/logging IO -> infrastructure/monitoring"
				confidence = "High"
			elif _imports_child_process(modules):
				base_dir = "infrastructure/container/bin"
				reason = "Detected child_process execution -> infrastructure/container/bin"
				confidence = "High"
				if io_tail.startswith("scripts/"):
					io_tail = io_tail[len("scripts/") :]
			elif _looks_like_http_client(code, modules):
				base_dir = "infrastructure/external_services/clients"
				reason = "Detected external HTTP client usage -> infrastructure/external_services/clients"
				confidence = "High"

			return _target(
				context,
				"Infrastructure",
				_join_dir_file(base_dir, io_tail, py_filename),
				reason=reason,
				confidence=confidence,
			)

	# --- Package-first special cases (clear boundaries) ---
	if pkg == "core":
		# Core runtime: execution engine orchestration + node loading + infra wiring.
		if rel.startswith("src/execution-engine/"):
			tail = rel[len("src/execution-engine/") :]
			return _target(
				context,
				"Application",
				_join_dir_file("application/services/execution_engine", tail, py_filename),
				reason="Core execution engine -> application/services/execution_engine",
				confidence="High",
			)
		if rel.startswith("src/binary-data/"):
			tail = rel[len("src/binary-data/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/external_services/adapters/file_storage/binary_data", tail, py_filename),
				reason="Core binary-data storage -> infrastructure file_storage adapter",
				confidence="High",
			)
		if rel.startswith("src/nodes-loader/"):
			tail = rel[len("src/nodes-loader/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/container/nodes_loader", tail, py_filename),
				reason="Node loading/discovery -> infrastructure/container/nodes_loader",
				confidence="High",
			)
		if rel.startswith("src/instance-settings/"):
			tail = rel[len("src/instance-settings/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/configuration/instance_settings", tail, py_filename),
				reason="Instance settings wiring -> infrastructure/configuration",
				confidence="High",
			)
		if rel.startswith("src/encryption/"):
			tail = rel[len("src/encryption/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/container/security/encryption", tail, py_filename),
				reason="Encryption implementation -> infrastructure/container/security",
				confidence="High",
			)
		if rel.startswith("src/utils/"):
			tail = rel[len("src/utils/") :]
			return _target(
				context,
				"Application",
				_join_dir_file("application/services/utils", tail, py_filename),
				reason="Core utility helpers -> application/services/utils",
				confidence="Medium",
			)
		if rel.startswith("src/"):
			tail = rel[len("src/") :]
			return _target(
				context,
				"Application",
				_join_dir_file("application/services/execution_engine", tail, py_filename),
				reason="Core src/* defaulted to execution engine application services",
				confidence="Medium",
			)

	if pkg == "@n8n/api-types":
		# Shared request/response DTO contracts (FE/BE).
		if not rel.startswith("src/"):
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/configuration/tooling", rel, py_filename),
				reason="Package @n8n/api-types tooling/config file",
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
				_join_dir_file("infrastructure/configuration/tooling", rel, py_filename),
				reason="Package @n8n/db tooling/config file",
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
		if "/" not in rel:
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/configuration/tooling", rel, py_filename),
				reason="Integration package tooling/config file",
				confidence="Medium",
			)
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
		if not rel.startswith("src/"):
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/configuration/tooling", rel, py_filename),
				reason="Package @n8n/errors tooling/config file",
				confidence="Medium",
			)
		tail = rel[len("src/") :] if rel.startswith("src/") else rel
		return _target(
			context,
			"Domain",
			_join_dir_file("domain/exceptions", tail, py_filename),
			reason="Shared error types -> domain/exceptions",
			confidence="High",
		)

	if pkg == "workflow":
		if not rel.startswith("src/"):
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/configuration/tooling", rel, py_filename),
				reason="Package workflow tooling/config file",
				confidence="Medium",
			)
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

	if pkg == "@n8n/permissions":
		# Permission and role rules are domain policies (pure rule evaluation, no IO).
		rel_tail = rel[len("src/") :] if rel.startswith("src/") else rel
		return _target(
			context,
			"Domain",
			_join_dir_file("domain/policies", rel_tail, py_filename),
			reason="Package @n8n/permissions treated as domain authorization policies",
			confidence="High",
		)

	if pkg == "@n8n/constants":
		rel_tail = rel[len("src/") :] if rel.startswith("src/") else rel
		return _target(
			context,
			"Domain",
			_join_dir_file("domain/models/constants", rel_tail, py_filename),
			reason="Package @n8n/constants treated as domain constants",
			confidence="High",
		)

	if pkg in {"@n8n/backend-common", "@n8n/config"}:
		rel_tail = rel[len("src/") :] if rel.startswith("src/") else rel
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("infrastructure/configuration", rel_tail, py_filename),
			reason=f"Package {pkg} treated as infrastructure configuration/runtime environment",
			confidence="High",
		)

	if pkg in {"@n8n/client-oauth2", "@n8n/imap", "@n8n/syslog-client"}:
		rel_tail = rel[len("src/") :] if rel.startswith("src/") else rel
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("infrastructure/external_services/clients", rel_tail, py_filename),
			reason=f"Package {pkg} treated as external service client library",
			confidence="High",
		)

	if pkg == "@n8n/extension-sdk":
		rel_tail = rel[len("src/") :] if rel.startswith("src/") else rel
		if rel.startswith("scripts/"):
			tail = rel[len("scripts/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/configuration/tooling", tail, py_filename),
				reason="Extension SDK tooling script -> infrastructure/configuration/tooling",
				confidence="High",
			)
		return _target(
			context,
			"Interface",
			_join_dir_file("presentation/dto/extension_sdk", rel_tail, py_filename),
			reason="Extension SDK contracts/helpers -> presentation/dto",
			confidence="High",
		)

	if pkg == "@n8n/utils":
		rel_tail = rel[len("src/") :] if rel.startswith("src/") else rel
		if "event-bus" in rel or "event-queue" in rel:
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/event_bus", rel_tail, py_filename),
				reason="Event bus/queue helpers -> infrastructure/event_bus",
				confidence="High",
			)
		if rel.startswith("src/files/") or "/files/" in f"/{rel}/":
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/container/files", rel_tail, py_filename),
				reason="Filesystem/path helpers -> infrastructure/container/files",
				confidence="High",
			)
		return _target(
			context,
			"Application",
			_join_dir_file("application/services/utils", rel_tail, py_filename),
			reason="Generic shared utilities -> application/services/utils",
			confidence="High",
		)

	if pkg == "extensions":
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("infrastructure/configuration/tooling/extensions", rel, py_filename),
			reason="Extensions package -> infrastructure/configuration/tooling/extensions",
			confidence="High",
		)

	if pkg == "node-dev":
		if rel.startswith("commands/"):
			tail = rel[len("commands/") :]
			return _target(
				context,
				"Interface",
				_join_dir_file("presentation/cli/commands", tail, py_filename),
				reason="node-dev command -> presentation/cli/commands",
				confidence="High",
			)
		rel_tail = rel[len("src/") :] if rel.startswith("src/") else rel
		return _target(
			context,
			"Interface",
			_join_dir_file("presentation/cli", rel_tail, py_filename),
			reason="node-dev CLI tool -> presentation/cli",
			confidence="High",
		)

	if pkg == "@n8n/scan-community-package":
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("infrastructure/container/bin", rel, py_filename),
			reason="Community package scanner CLI/tooling -> infrastructure/container/bin",
			confidence="High",
		)

	if pkg in {"@n8n/eslint-config", "@n8n/eslint-plugin-community-nodes", "@n8n/stylelint-config", "@n8n/vitest-config"}:
		# Lint/format tooling lives outside runtime layers.
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("infrastructure/configuration/tooling", rel, py_filename),
			reason="Tooling package (lint/test config) -> infrastructure/configuration/tooling",
			confidence="High",
		)

	if pkg in {"@n8n/backend-test-utils"}:
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("tests/mocks", rel, py_filename),
			reason="Test utilities package -> tests/mocks",
			confidence="High",
		)

	if pkg == "testing":
		# Repo-wide testing harness (playwright + containers).
		if rel.startswith("playwright/"):
			tail = rel[len("playwright/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("tests/integration/ui/playwright", tail, py_filename),
				reason="Testing package (playwright) -> tests/integration/ui/playwright",
				confidence="High",
			)
		if rel.startswith("containers/"):
			tail = rel[len("containers/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("tests/fixtures/containers", tail, py_filename),
				reason="Testing package (containers harness) -> tests/fixtures/containers",
				confidence="High",
			)
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("tests", rel, py_filename),
			reason="Testing package -> tests/*",
			confidence="High",
		)

	if pkg == "@n8n/benchmark":
		# Performance benchmarking toolchain (k6 scenarios, env provisioning, API client).
		if rel.startswith("scenarios/"):
			tail = rel[len("scenarios/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("tests/functional/benchmarks/scenarios", tail, py_filename),
				reason="Benchmark scenarios -> tests/functional/benchmarks/scenarios",
				confidence="High",
			)
		if rel.startswith("scripts/"):
			tail = rel[len("scripts/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/container/bin/benchmark", tail, py_filename),
				reason="Benchmark scripts -> infrastructure/container/bin",
				confidence="High",
			)
		if rel.startswith("src/n8n-api-client/"):
			tail = rel[len("src/n8n-api-client/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/external_services/clients/n8n_api_client", tail, py_filename),
				reason="Benchmark n8n API client -> infrastructure/external_services/clients",
				confidence="High",
			)
		if rel.startswith("src/test-execution/"):
			tail = rel[len("src/test-execution/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/container", tail, py_filename),
				reason="Benchmark test execution (k6/process/metrics) -> infrastructure/container",
				confidence="High",
			)
		# remaining benchmark code: treat as tooling application
		rel_tail = rel[len("src/") :] if rel.startswith("src/") else rel
		return _target(
			context,
			"Application",
			_join_dir_file("application/services", rel_tail, py_filename),
			reason="Benchmark orchestration logic -> application/services",
			confidence="Medium",
		)

	if pkg == "@n8n/json-schema-to-zod":
		rel_tail = rel[len("src/") :] if rel.startswith("src/") else rel
		return _target(
			context,
			"Application",
			_join_dir_file("application/services", rel_tail, py_filename),
			reason="Pure schema->validator transformation library -> application/services",
			confidence="High",
		)

	if pkg == "@n8n/ai-workflow-builder.ee":
		# Primarily application-level LLM workflow building logic (prompts/tools/state).
		if rel.startswith("evaluations/") or rel.startswith("eval"):
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/configuration/tooling/evaluations", rel, py_filename),
				reason="AI builder evaluation harness/scripts -> infrastructure/configuration/tooling",
				confidence="High",
			)
		return _target(
			context,
			"Application",
			_join_dir_file("application/services", fallback_tail, py_filename),
			reason="AI workflow builder package -> application/services",
			confidence="High",
		)

	if pkg == "@n8n/node-cli":
		# Node CLI scaffolding + templates + dev-time tooling.
		if rel.startswith("scripts/"):
			tail = rel[len("scripts/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/container/bin", tail, py_filename),
				reason="CLI tooling script -> infrastructure/container/bin",
				confidence="High",
			)
		if rel.startswith("src/test-utils/") or "/test-utils/" in f"/{rel}/":
			tail = rel.split("test-utils/", 1)[-1]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("tests/mocks", tail, py_filename),
				reason="CLI test utilities -> tests/mocks",
				confidence="High",
			)
		if rel.startswith("src/template/"):
			tail = rel[len("src/template/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/configuration/tooling/templates", tail, py_filename),
				reason="CLI code templates -> infrastructure/configuration/tooling/templates",
				confidence="High",
			)
		rel_tail = rel[len("src/") :] if rel.startswith("src/") else rel
		return _target(
			context,
			"Interface",
			_join_dir_file("presentation/cli", rel_tail, py_filename),
			reason="CLI package default -> presentation/cli",
			confidence="Medium",
		)

	if pkg == "@n8n/task-runner":
		rel_tail = rel[len("src/") :] if rel.startswith("src/") else rel
		if rel_tail in {"start.ts", "start.js"}:
			return _target(
				context,
				"Infrastructure",
				"main.py",
				reason="Task runner entrypoint -> main.py (BOOT)",
				confidence="High",
			)
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("infrastructure/container", rel_tail, py_filename),
			reason="Task runner process runtime -> infrastructure/container",
			confidence="High",
		)

	# Package root files (usually tooling/config) map to infrastructure configuration/tooling.
	if "/" not in rel:
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("infrastructure/configuration/tooling", rel, py_filename),
			reason="Package root tooling/config file",
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

	# Routers / route tables
	if "/routers/" in rel_norm or rel.startswith("src/routers/") or "/routes/" in rel_norm or rel.startswith("src/routes/"):
		tail = rel.split("routers/", 1)[-1]
		tail = tail.split("routes/", 1)[-1]
		return _target(
			context,
			"Interface",
			_join_dir_file("presentation/api/v1/routers", tail, py_filename),
			reason="Routes/routers -> presentation/api/v1/routers",
			confidence="High",
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

	# Core execution engine & binary data storage
	if pkg == "core" and "/execution-engine/" in rel_norm:
		tail = rel.split("execution-engine/", 1)[-1]
		return _target(
			context,
			"Application",
			_join_dir_file("application/services/execution_engine", tail, py_filename),
			reason="Core execution engine -> application/services/execution_engine",
			confidence="High",
		)

	if pkg == "core" and "/binary-data/" in rel_norm:
		tail = rel.split("binary-data/", 1)[-1]
		return _target(
			context,
			"Infrastructure",
			_join_dir_file("infrastructure/external_services/adapters/file_storage/binary_data", tail, py_filename),
			reason="Core binary-data storage -> infrastructure file_storage adapter",
			confidence="High",
		)

	# CLI backend: auth/executions lifecycle and related helpers are application orchestration by default.
	if pkg == "cli" and rel.startswith("src/"):
		for prefix, base_dir, label in [
			("src/auth/", "application/services/auth", "Authentication helpers/use-cases"),
			("src/executions/", "application/services/executions", "Execution read/write helpers"),
			("src/execution-lifecycle/", "application/services/execution_lifecycle", "Execution lifecycle hooks"),
			("src/deduplication/", "application/services/deduplication", "Deduplication helpers"),
			("src/credentials/", "application/ports/outbound/credentials", "Credential resolution/storage ports"),
			("src/chat/", "application/services/chat", "Chat feature helpers"),
		]:
			if rel.startswith(prefix):
				tail = rel[len(prefix) :]
				return _target(
					context,
					"Application",
					_join_dir_file(base_dir, tail, py_filename),
					reason=f"{label} -> {base_dir}",
					confidence="Medium",
				)

		for prefix, base_dir, label in [
			("src/push/", "presentation/api/push", "SSE/WebSocket push adapter"),
			("src/collaboration/", "presentation/dto/collaboration", "Collaboration message contracts"),
			("src/sso.ee/", "application/services/sso", "SSO integration orchestration"),
		]:
			if rel.startswith(prefix):
				tail = rel[len(prefix) :]
				return _target(
					context,
					"Interface" if base_dir.startswith("presentation/") else "Application",
					_join_dir_file(base_dir, tail, py_filename),
					reason=f"{label} -> {base_dir}",
					confidence="Medium",
				)

		if rel.startswith("scripts/"):
			tail = rel[len("scripts/") :]
			return _target(
				context,
				"Infrastructure",
				_join_dir_file("infrastructure/container/bin", tail, py_filename),
				reason="CLI scripts -> infrastructure/container/bin",
				confidence="High",
			)

		# CLI package default within src: application-level helpers (if not already matched above).
		return _target(
			context,
			"Application",
			_join_dir_file("application/services", fallback_tail, py_filename),
			reason="CLI src/* defaulted to application/services after rule matching",
			confidence="Medium",
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


def build_file_mapping_md_tables(
	source_rows: list[SourceRow],
	file_mappings: list[DddTarget],
	*,
	context_config: ContextConfig,
) -> list[str]:
	by_package_rows: dict[str, list[int]] = defaultdict(list)
	for i, row in enumerate(source_rows):
		by_package_rows[_package_id(row.source_path)].append(i)

	lines: list[str] = []
	for pkg in sorted(by_package_rows.keys()):
		context = _resolve_target_context(pkg, context_config)
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
	context_config: ContextConfig,
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
		lines.append(
			"- 微服务映射策略："
			+ ("单服务（single）" if context_config.strategy == "single" else "按包（per-package）")
			+ (
				f"（services/{context_config.single_context}/...）"
				if context_config.strategy == "single"
				else "（services/<context>/...）"
			)
		)
		lines.append(
			"- 文件映射条目（file-level）："
			+ str(len(file_mappings))
			+ f"（High {Counter(m.confidence for m in file_mappings).get('High', 0)} | Medium {Counter(m.confidence for m in file_mappings).get('Medium', 0)} | Low {Counter(m.confidence for m in file_mappings).get('Low', 0)}）"
		)
		lines.append(f"- 微服务数量（target_context 去重）：{len(set(m.target_context for m in file_mappings))}")
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
	lines.append("0. 源码信号优先（逐文件读取源码后判定）")
	lines.append("   - `@n8n/decorators` + `@RestController/@Controller` → `presentation/api/v1/controllers/**`（Interface）")
	lines.append("   - `express` + `RequestHandler|NextFunction|(req,res,next)` → `presentation/api/middleware/**`（Interface）")
	lines.append("   - `express` + `Request|Response`（非 middleware）→ `presentation/api/**`（Interface）")
	lines.append("   - `ws` + `WebSocket` → `presentation/api/ws/**`（Interface）")
	lines.append("   - `@playwright/test|vitest|jest|describe()/it()/test()` → `tests/**`（标记为 Infrastructure；非生产代码）")
	lines.append("   - `ResponseError`（定义或继承）→ `presentation/api/errors/**`（Interface）")
	lines.append("   - `typeorm|@n8n/typeorm` + `@Entity` → `infrastructure/persistence/models/**`（Infrastructure）")
	lines.append("   - `typeorm|@n8n/typeorm` + `MigrationInterface` → `infrastructure/persistence/migrations/**`（Infrastructure）")
	lines.append("   - `typeorm|@n8n/typeorm` + `Repository|EntityManager` → `infrastructure/persistence/repositories/**`（Infrastructure）")
	lines.append("   - `n8n-workflow` + `implements ICredentialType` → `infrastructure/external_services/adapters/credentials/**`（Infrastructure）")
	lines.append("   - `n8n-workflow` + `implements INodeType` → `infrastructure/external_services/adapters/nodes/**`（Infrastructure）")
	lines.append("   - `@n8n/di` + `@Service` → `application/services/**`（Application）")
	lines.append("   - `xmllint-wasm` + `XMLFileInfo` → `infrastructure/configuration/**`（Infrastructure）")
	lines.append("   - `fs|http|child_process|axios|fetch` → `infrastructure/**`（Infrastructure；I/O/外部交互）")
	lines.append("1. 包级强规则（高置信度；用于补齐源码信号不足的文件）")
	lines.append("   - `@n8n/api-types/src/**` → `presentation/dto/**`；包根配置 → `infrastructure/configuration/tooling/**`")
	lines.append("   - `@n8n/db/src/**` → `infrastructure/persistence/**`；包根配置 → `infrastructure/configuration/tooling/**`")
	lines.append("   - `nodes-base/**`、`@n8n/nodes-langchain/**` → `infrastructure/external_services/**`；包根配置 → `infrastructure/configuration/tooling/**`")
	lines.append("   - `@n8n/errors/src/**` → `domain/exceptions/**`；包根配置 → `infrastructure/configuration/tooling/**`")
	lines.append("   - `workflow/src/**` → `domain/services/**`（errors → `domain/exceptions/**`）；包根配置 → `infrastructure/configuration/tooling/**`")
	lines.append("   - `@n8n/permissions/src/**` → `domain/policies/**`（Domain）")
	lines.append("   - `@n8n/constants/src/**` → `domain/models/constants/**`（Domain）")
	lines.append("   - `testing/**` → `tests/**`（Infrastructure；测试工具包）")
	lines.append("   - `@n8n/benchmark/**` → `tests/functional/benchmarks/**`、`infrastructure/container/bin/**` 等（Infrastructure）")
	lines.append("   - `@n8n/eslint-config|...` → `infrastructure/configuration/tooling/**`（Infrastructure；工具包）")
	lines.append("2. 目录启发式（当源码信号不足时）")
	lines.append("   - `*/src/commands/**`：CLI 类包 → `presentation/cli/commands/**`；非 CLI 包 → `application/commands/handlers/**`")
	lines.append("   - `cli/bin/n8n|n8n.cmd` → `main.py`")
	lines.append("   - `*/routes|routers/**` → `presentation/api/v1/routers/**`（Interface）")
	lines.append("   - `core/src/execution-engine/**` → `application/services/execution_engine/**`（Application）")
	lines.append("   - `core/src/binary-data/**` → `infrastructure/.../file_storage/binary_data/**`（Infrastructure）")
	lines.append("   - `*/databases|repositories|migrations|entities/**` → `infrastructure/persistence/**`")
	lines.append("   - `*/config|configs/**` → `infrastructure/configuration/**`")
	lines.append("   - `*/eventbus|events/**` → `infrastructure/event_bus/**`")
	lines.append("   - `*/telemetry|metrics|posthog|logging|tracing/**` → `infrastructure/monitoring/**`")
	lines.append("3. 兜底（需人工复核）")
	lines.append("   - 未命中的代码文件 → `application/services/**`（`confidence=Low`）")
	lines.append("")
	lines.append("> 说明：该映射为“预重构”阶段的启发式归类；正式迁移批次仍需按职责/依赖关系人工复核与拆分。")
	lines.append("")

	lines.append("## 映射矩阵（包级）")
	lines.append("")
	lines.append("| 原模块/包名 | 核心职责 | 对应DDD上下文 | 对应分层 | 映射置信度 |")
	lines.append("|-------------|----------|---------------|----------|------------|")

	for pkg in sorted(by_package_rows.keys()):
		context = _resolve_target_context(pkg, context_config)
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
	lines.extend(
		build_file_mapping_md_tables(
			source_rows,
			file_mappings,
			context_config=context_config,
		)
	)

	out_path.write_text("\n".join([line for line in lines if line is not None]), encoding="utf-8")


def write_batch_doc_md(
	out_path: Path,
	*,
	batch_id: str,
	source_generated_at: str | None,
	source_rows: list[SourceRow],
	file_mappings: list[DddTarget],
	context_config: ContextConfig,
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
	if context_config.strategy == "single":
		lines.append(f"  bounded_contexts: [\"{context_config.single_context}\"]")
	else:
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
	if context_config.strategy == "single":
		lines.append(
			f"- Decisions：采用单服务策略，将所有模块合并映射到 `services/{context_config.single_context}/...`（target_context 固定）。"
		)
	else:
		lines.append(
			"- Decisions：按 `packages/<pkg>`（或 `packages/@n8n/<pkg>`）作为默认限界上下文名来源，映射到 `services/{context}/...`。"
		)
	lines.append("- Open Issues：该规则为启发式；仍需对 `packages/cli`、`packages/core` 等混层包进行人工复核与拆分策略。")
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
	lines.append(f"- Context 去重数量：{len(by_context)}")
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
	parser.add_argument(
		"--context-strategy",
		choices=["single", "per-package"],
		default="single",
		help="How to derive target_context (microservice directory name)",
	)
	parser.add_argument(
		"--single-context",
		default="n8n",
		help="Service name used when --context-strategy=single (services/<name>/...)",
	)
	args = parser.parse_args()

	context_config = ContextConfig(strategy=args.context_strategy, single_context=args.single_context)

	generated_at, rows = parse_system_analysis(args.system_analysis)
	ddd_structure = parse_ddd_structure(args.ddd_template)

	mapped = [map_row_to_ddd(r, context_config=context_config) for r in rows]

	matrix_path = args.out_dir / "mapping-matrix.md"
	write_mapping_matrix_md(
		matrix_path,
		generated_at=generated_at,
		source_rows=rows,
		file_mappings=mapped,
		ddd_structure=ddd_structure,
		context_config=context_config,
	)

	batch_path = args.out_dir / "batches" / f"{args.batch_id}.md"
	write_batch_doc_md(
		batch_path,
		batch_id=args.batch_id,
		source_generated_at=generated_at,
		source_rows=rows,
		file_mappings=mapped,
		context_config=context_config,
	)

	print(f"Wrote: {matrix_path}")
	print(f"Wrote: {batch_path}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())

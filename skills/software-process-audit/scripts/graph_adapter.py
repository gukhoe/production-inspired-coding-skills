"""Read-only Graphify node-link adapter; graph relations are audit candidates."""
from collections import Counter, deque
import hashlib
import json
from pathlib import Path


class AuditError(ValueError):
    """Invalid or unsupported audit input."""


def read_json(path, max_bytes=128 * 1024 * 1024):
    path = Path(path)
    with path.open("rb") as stream:
        raw = stream.read(max_bytes + 1)
    if len(raw) > max_bytes:
        raise AuditError(f"Input exceeds {max_bytes} bytes: {path.name}")
    try:
        value = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise AuditError(f"Invalid JSON: {path.name}") from exc
    if not isinstance(value, dict):
        raise AuditError("JSON root must be an object")
    return value, hashlib.sha256(raw).hexdigest()


class Graph:
    def __init__(self, path):
        data, self.sha256 = read_json(path)
        meta = data.get("graph", {})
        if not isinstance(meta, dict) or type(meta.get("schema_version")) is not int or meta["schema_version"] != 1:
            raise AuditError("Supported Graphify graph.schema_version: 1")
        if type(data.get("directed")) is not bool or type(data.get("multigraph")) is not bool:
            raise AuditError("Graph directed and multigraph must be booleans")
        self.directed = data["directed"]
        self.version = meta.get("graphify_version", "unknown")
        nodes, links = data.get("nodes"), data.get("links")
        if not isinstance(nodes, list) or not isinstance(links, list):
            raise AuditError("Graphify nodes and links arrays required")
        self.nodes, self.adjacency, self.edges = {}, {}, []
        for node in nodes:
            if not isinstance(node, dict) or not isinstance(node.get("id"), str) or not node["id"]:
                raise AuditError("Graph node requires a nonempty string id")
            nid = node["id"]
            if nid in self.nodes:
                raise AuditError(f"Duplicate graph node id: {nid}")
            self.nodes[nid], self.adjacency[nid] = node, []
        for link in links:
            if not isinstance(link, dict):
                raise AuditError("Graph links must be objects")
            source, target = link.get("source"), link.get("target")
            if not isinstance(source, str) or not isinstance(target, str) or source not in self.nodes or target not in self.nodes:
                raise AuditError("Graph link has an unknown endpoint")
            relation = link.get("relation", "unknown")
            confidence = link.get("confidence", "UNKNOWN")
            if not isinstance(relation, str) or not isinstance(confidence, str):
                raise AuditError("Graph relation and confidence must be strings")
            edge = {"source": source, "target": target, "relation": relation,
                    "confidence": confidence, "confidence_score": link.get("confidence_score")}
            self.edges.append(edge)
            self.adjacency[source].append((target, edge))
            if not self.directed and target != source:
                self.adjacency[target].append((source, edge))
        hyperedges = data.get("hyperedges", [])
        if not isinstance(hyperedges, list):
            raise AuditError("Graph hyperedges must be an array")
        self.hyperedge_count = len(hyperedges)

    def summary(self):
        return {"schema_version": 1, "graphify_version": self.version,
                "sha256": self.sha256, "directed": self.directed,
                "nodes": len(self.nodes), "links": len(self.edges),
                "confidence_counts": dict(Counter(e["confidence"] for e in self.edges)),
                "relation_counts": dict(Counter(e["relation"] for e in self.edges)),
                "hyperedges_not_traversed": self.hyperedge_count,
                "source_freshness": "unverified",
                "interpretation": "Static or inferred relationships; not proof of runtime behavior."}

    def candidates(self, seed, depth=2, limit=100):
        if seed not in self.nodes:
            raise AuditError("Unknown seed; use the exact Graphify node id")
        if type(depth) is not int or not 0 <= depth <= 6 or type(limit) is not int or not 1 <= limit <= 10000:
            raise AuditError("depth must be 0..6; limit must be 1..10000")
        seen, queue, paths = {seed}, deque([(seed, 0)]), {seed: []}
        capacity_truncated, depth_truncated = False, False
        while queue:
            current, level = queue.popleft()
            for other, edge in self.adjacency[current]:
                if other in seen:
                    continue
                if level == depth:
                    depth_truncated = True
                    continue
                if len(seen) == limit:
                    capacity_truncated = True
                    continue
                seen.add(other)
                paths[other] = paths[current] + [edge]
                queue.append((other, level + 1))
        return {"seed": seed, "depth_limit": depth, "node_limit": limit,
                "capacity_truncated": capacity_truncated, "depth_truncated": depth_truncated,
                "interpretation": "Bounded relationship candidates, not causal blast radius. One discovery path per node; parallel edges and alternative paths are not exhaustively reported.",
                "candidates": [{"id": nid, "label": self.nodes[nid].get("label", nid),
                                "path": paths[nid],
                                "path_evidence": self._path_evidence(paths[nid])} for nid in sorted(seen)]}

    def boundary_candidates(self, processes, boundaries, limit=200):
        """Compare mapped runtime endpoints with declared review boundaries."""
        owners = {}
        for pid, process in processes.items():
            if process["kind"] == "runtime":
                for nid in process.get("graph_nodes", []):
                    owners.setdefault(nid, set()).add(pid)
        def pair(source, target):
            return (source, target) if self.directed else tuple(sorted((source, target)))
        declared = {pair(b["source"], b["target"]) for b in boundaries.values()}
        groups, truncated = {}, False
        for edge in self.edges:
            for source in sorted(owners.get(edge["source"], ())):
                for target in sorted(owners.get(edge["target"], ())):
                    if source == target:
                        continue
                    key = pair(source, target)
                    if key not in groups:
                        if len(groups) >= limit:
                            truncated = True
                            continue
                        groups[key] = {"source": key[0], "target": key[1], "edge_count": 0,
                                       "confidence_counts": {}, "sample_edges": [],
                                       "review_boundary_declared": key in declared}
                    group = groups[key]
                    group["edge_count"] += 1
                    tag = edge["confidence"]
                    group["confidence_counts"][tag] = group["confidence_counts"].get(tag, 0) + 1
                    if len(group["sample_edges"]) < 5:
                        group["sample_edges"].append(edge)
        return {"mapped_runtime_nodes": len(owners), "pair_limit": limit, "truncated": truncated,
                "candidates": list(groups.values()),
                "interpretation": "Only direct links between explicitly mapped runtime nodes are checked. Undeclared connections need review; they are not automatically defects. Delivery handoffs are assessed separately."}

    @staticmethod
    def _path_evidence(edges):
        tags = {e["confidence"] for e in edges}
        if not edges:
            return "SEED"
        if tags - {"EXTRACTED", "INFERRED"}:
            return "UNKNOWN"
        return "INFERRED" if "INFERRED" in tags else "EXTRACTED"

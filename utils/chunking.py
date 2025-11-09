import os
import hashlib
import uuid
from typing import List, Dict, Any

class ChunkingUtils:
    """Shared utilities for file chunking across all modes"""

    def __init__(self, chunk_size: int = 1024 * 1024):  # 1MB default
        self.chunk_size = chunk_size

    def split_file_into_chunks(self, file_data: bytes, mode: str = 'simple') -> List[Dict[str, Any]]:
        """Split file data into chunks for fault tolerance"""
        chunks = []
        total_size = len(file_data)
        num_chunks = (total_size + self.chunk_size - 1) // self.chunk_size  # Ceiling division

        for i in range(num_chunks):
            start = i * self.chunk_size
            end = min(start + self.chunk_size, total_size)
            chunk_data = file_data[start:end]
            chunk_hash = hashlib.md5(chunk_data).hexdigest()

            chunk_info = {
                'chunk_id': f'chunk_{i}',
                'data': chunk_data,
                'size': len(chunk_data),
                'hash': chunk_hash,
                'sequence': i,
                'total_chunks': num_chunks
            }

            chunks.append(chunk_info)

        return chunks

    def reconstruct_file_from_chunks(self, chunks: List[Dict[str, Any]]) -> bytes:
        """Reconstruct file from ordered chunks"""
        # Sort chunks by sequence
        sorted_chunks = sorted(chunks, key=lambda x: x['sequence'])

        # Concatenate chunk data
        file_data = b''.join([chunk['data'] for chunk in sorted_chunks])

        return file_data

    def validate_chunk_integrity(self, chunk: Dict[str, Any]) -> bool:
        """Validate chunk data integrity using hash"""
        if 'data' not in chunk or 'hash' not in chunk:
            return False

        calculated_hash = hashlib.md5(chunk['data']).hexdigest()
        return calculated_hash == chunk['hash']

class DistributionUtils:
    """Utilities for distributing chunks across nodes"""

    def __init__(self, replication_factor: int = 2):
        self.replication_factor = replication_factor

    def distribute_chunks_across_nodes(self, chunks: List[Dict[str, Any]],
                                     nodes: List[Dict[str, Any]],
                                     storage_dir: str) -> Dict[str, List[Dict[str, Any]]]:
        """Distribute chunks across available nodes with redundancy"""
        chunk_distribution = {}
        active_nodes = [n for n in nodes if n.get('status') == 'active']

        if len(active_nodes) < self.replication_factor:
            self.replication_factor = len(active_nodes)

        if len(active_nodes) == 0:
            raise ValueError("No active nodes available for distribution")

        for chunk in chunks:
            # Select nodes for this chunk (with redundancy)
            selected_nodes = self._select_nodes_for_chunk(active_nodes, self.replication_factor)
            chunk_distribution[chunk['chunk_id']] = []

            for node in selected_nodes:
                chunk_file = f"{chunk['chunk_id']}_{node['node_id']}_{uuid.uuid4().hex[:8]}"
                chunk_path = os.path.join(storage_dir, chunk_file)

                # Save chunk to file
                with open(chunk_path, 'wb') as f:
                    f.write(chunk['data'])

                chunk_distribution[chunk['chunk_id']].append({
                    'node_id': node['node_id'],
                    'chunk_file': chunk_file,
                    'path': chunk_path
                })

                # Update node stats
                node['files_count'] = node.get('files_count', 0) + 1
                node['storage_used'] = node.get('storage_used', 0) + chunk['size']
                node['last_heartbeat'] = self._get_current_timestamp()

        return chunk_distribution

    def _select_nodes_for_chunk(self, active_nodes: List[Dict[str, Any]],
                               replication_factor: int) -> List[Dict[str, Any]]:
        """Select nodes for chunk distribution using round-robin or random selection"""
        import random
        return random.sample(active_nodes, replication_factor)

    def reconstruct_from_distribution(self, file_id: str, chunk_distribution: Dict[str, List[Dict[str, Any]]],
                                    active_nodes: List[Dict[str, Any]]) -> tuple:
        """Reconstruct file from distributed chunks, handling node failures"""
        active_node_ids = {n['node_id'] for n in active_nodes if n.get('status') == 'active'}
        reconstructed_chunks = []
        missing_chunks = []

        for chunk_id, locations in chunk_distribution.items():
            chunk_found = False
            for location in locations:
                if location['node_id'] in active_node_ids:
                    chunk_path = location['path']
                    if os.path.exists(chunk_path):
                        with open(chunk_path, 'rb') as f:
                            chunk_data = f.read()

                        # Find the original chunk info to get sequence
                        # This assumes chunk metadata is stored elsewhere
                        chunk_info = self._find_chunk_info(chunk_id, chunk_data)
                        if chunk_info:
                            reconstructed_chunks.append((chunk_info['sequence'], chunk_data))
                            chunk_found = True
                            break

            if not chunk_found:
                missing_chunks.append(chunk_id)

        if missing_chunks:
            return None, missing_chunks  # Cannot reconstruct

        # Sort by sequence and reconstruct
        reconstructed_chunks.sort(key=lambda x: x[0])
        file_data = b''.join([chunk[1] for chunk in reconstructed_chunks])

        return file_data, None

    def _find_chunk_info(self, chunk_id: str, chunk_data: bytes) -> Dict[str, Any]:
        """Find chunk information - this should be enhanced with proper metadata storage"""
        # For now, return basic info based on chunk_id
        try:
            sequence = int(chunk_id.split('_')[1])
            return {
                'chunk_id': chunk_id,
                'sequence': sequence,
                'size': len(chunk_data),
                'hash': hashlib.md5(chunk_data).hexdigest()
            }
        except (IndexError, ValueError):
            return None

    def _get_current_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

# Global instances
chunking_utils = ChunkingUtils()
distribution_utils = DistributionUtils()
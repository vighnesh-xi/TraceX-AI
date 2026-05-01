import json
import yaml
from typing import List, Dict
from loguru import logger

class ConfigParser:
    def parse(self, file_info: Dict) -> List[Dict]:
        content = file_info.get("content", "")
        path = file_info.get("relative_path", "")
        ext = file_info.get("extension", "")

        parsed_data = None
        try:
            if ext in (".yaml", ".yml"):
                parsed_data = yaml.safe_load(content)
            elif ext == ".json":
                parsed_data = json.loads(content)
        except Exception as e:
            logger.warning(f"Config parse error {path}: {e}")

        return [{
            "chunk_id": f"{path}::config",
            "file_path": path,
            "name": path.split("\\")[-1].split("/")[-1],
            "type": "config",
            "content": content[:2000],
            "parsed": parsed_data,
            "source": "config",
        }]
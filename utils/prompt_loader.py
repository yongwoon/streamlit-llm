import glob
import os

class PromptLoader:
    def __init__(self, base_folder="prompts", languages=None):
        self.base_folder = base_folder
        self.languages = languages or ['en', 'kr']
        self.file_map = {}  # 表示名とファイルパスのマッピング

    def get_prompt_files(self):
        prompt_files = []
        self.file_map = {}  # マッピングをリセット

        for lang in self.languages:
            files = glob.glob(f"{self.base_folder}/{lang}/*.yaml")
            for file_path in files:
                # ファイル名を取得し、拡張子を除去
                display_name = os.path.splitext(os.path.basename(file_path))[0]
                self.file_map[display_name] = file_path
                prompt_files.append(display_name)

        return prompt_files

    def get_file_path(self, display_name):
        return self.file_map.get(display_name)

# open_dubbing/translation_nmt.py
import requests
from open_dubbing.translation import Translation


class TranslationNMT(Translation):

    def __init__(self, server_url: str):
        super().__init__(device="cpu")
        self.server_url = server_url.rstrip("/") + "/translate/"

    def load_model(self):
        # No model loading needed (HTTP service)
        pass

    def get_language_pairs(self):
        # NMT does not expose pairs here; assume server validates
        # IMPORTANT: must return a NON-empty iterable for check_languages
        return [("eng", "cat"), ("cat", "eng")]

    def _translate_text(self, source_language: str, target_language: str, text: str) -> str:
        langpair = f"{source_language}|{target_language}"

        r = requests.post(
            self.server_url,
            data={"q": text, "langpair": langpair},
            timeout=10.0,
        )
        r.raise_for_status()
        data = r.json()

        try:
            return data["responseData"]["translatedText"]
        except (KeyError, TypeError):
            raise RuntimeError(f"Unexpected NMT response format: {data}")


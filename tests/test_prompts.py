"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@pytest.fixture
def prompt_data():
    return load_prompts(PROMPT_FILE)["bug_to_user_story_v2"]

class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt_data):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert prompt_data.get("system_prompt", "").strip()

    def test_prompt_has_role_definition(self, prompt_data):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        assert "Você é um" in prompt_data["system_prompt"]

    def test_prompt_mentions_format(self, prompt_data):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = prompt_data["system_prompt"]
        assert "Como" in system_prompt
        assert "eu quero" in system_prompt
        assert "Critérios de Aceitação" in system_prompt

    def test_prompt_has_few_shot_examples(self, prompt_data):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = prompt_data["system_prompt"]
        assert "Entrada:" in system_prompt
        assert "Saída:" in system_prompt

    def test_prompt_no_todos(self, prompt_data):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        assert "[TODO]" not in prompt_data["system_prompt"]
        assert "[TODO]" not in prompt_data["user_prompt"]

    def test_minimum_techniques(self, prompt_data):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        assert len(prompt_data.get("techniques", [])) >= 2

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
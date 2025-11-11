from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass(frozen=True)
class Competency:
	name: str
	kind: str 

@dataclass
class Profile:
	person_name: str
	scores: Dict[str, int] = field(default_factory=dict)  # competencia -> 0..100

	def set_score(self, competency_name: str, score: int) -> None:
		score_clamped = max(0, min(100, int(score)))
		self.scores[competency_name] = score_clamped

	def get_score(self, competency_name: str) -> int:
		return int(self.scores.get(competency_name, 0))


@dataclass(frozen=True)
class Career:
	name: str
	description: str
	requirements: Dict[str, int]  # competencia -> mínimo 0..100

	def required_competencies(self) -> List[str]:
		return list(self.requirements.keys())

COMPETENCIES: List[Competency] = [
	Competency("logica", "technical"),
	Competency("programacao", "technical"),
	Competency("dados", "technical"),
	Competency("ia_ml", "technical"),
	Competency("seguranca", "technical"),
	Competency("criatividade", "behavioral"),
	Competency("colaboracao", "behavioral"),
	Competency("comunicacao", "behavioral"),
	Competency("adaptabilidade", "behavioral"),
	Competency("resolucao_problemas", "behavioral"),
]

CAREERS: List[Career] = [
	Career(
		name="Cientista de Dados",
		description="Analisa dados, cria modelos estatísticos/ML para gerar insights.",
		requirements={
			"logica": 70,
			"dados": 75,
			"ia_ml": 70,
			"programacao": 65,
			"comunicacao": 55,
			"resolucao_problemas": 65,
		},
	),
	Career(
		name="Engenheiro de Software",
		description="Projeta, desenvolve e mantém sistemas e aplicações de software.",
		requirements={
			"logica": 70,
			"programacao": 75,
			"colaboracao": 60,
			"resolucao_problemas": 65,
			"comunicacao": 55,
			"adaptabilidade": 55,
		},
	),
	Career(
		name="Especialista em Segurança",
		description="Garante segurança de sistemas, redes e dados. Foca em riscos e mitigação.",
		requirements={
			"logica": 65,
			"seguranca": 75,
			"programacao": 55,
			"resolucao_problemas": 65,
			"comunicacao": 50,
			"adaptabilidade": 55,
		},
	),
	Career(
		name="Designer de Produto Digital",
		description="Cria experiências digitais centradas no usuário, equilibrando forma e função.",
		requirements={
			"criatividade": 75,
			"comunicacao": 60,
			"colaboracao": 60,
			"resolucao_problemas": 60,
			"adaptabilidade": 60,
		},
	),
	Career(
		name="Analista de Negócios",
		description="Faz a ponte entre negócio e tecnologia, definindo requisitos e oportunidades.",
		requirements={
			"comunicacao": 70,
			"colaboracao": 65,
			"logica": 60,
			"resolucao_problemas": 60,
			"adaptabilidade": 60,
		},
	),
]

LEARNING_PATHS: Dict[str, List[Tuple[str, str]]] = {
	"logica": [
		("Exercícios de lógica de programação", "https://www.beecrowd.com.br"),
		("Curso de fundamentos de algoritmos", "https://www.coursera.org"),
	],
	"programacao": [
		("Python do básico ao avançado", "https://www.alura.com.br"),
		("Estruturas de dados e algoritmos", "https://www.udemy.com"),
	],
	"dados": [
		("SQL para análise de dados", "https://mode.com/sql-tutorial/"),
		("Estatística aplicada", "https://www.khanacademy.org"),
	],
	"ia_ml": [
		("Machine Learning Hands-on", "https://scikit-learn.org"),
		("Curso introdutório de IA/ML", "https://www.coursera.org/learn/machine-learning"),
	],
	"seguranca": [
		("OWASP Top 10", "https://owasp.org/www-project-top-ten/"),
		("Introdução a Cybersecurity", "https://www.netacad.com/"),
	],
	"criatividade": [
		("Técnicas de ideação", "https://www.interaction-design.org"),
		("Criatividade aplicada a produtos", "https://www.coursera.org"),
	],
	"colaboracao": [
		("Metodologias ágeis (Scrum/Kanban)", "https://www.scrum.org"),
		("Colaboração remota eficaz", "https://rework.withgoogle.com/"),
	],
	"comunicacao": [
		("Comunicação assertiva", "https://www.ted.com/"),
		("Storytelling para negócios", "https://www.coursera.org"),
	],
	"adaptabilidade": [
		("Aprendizagem contínua", "https://www.edx.org"),
		("Gestão de mudanças", "https://www.coursera.org"),
	],
	"resolucao_problemas": [
		("Pensamento crítico", "https://www.edx.org"),
		("Frameworks de decisão", "https://www.mindtools.com"),
	],
}


class Recommender:
	def __init__(self, careers: List[Career]) -> None:
		self._careers = careers

	def score_profile_for_career(self, profile: Profile, career: Career) -> Tuple[float, Dict[str, int]]:
		total_requirements = 0
		acc_score = 0.0
		gaps: Dict[str, int] = {}

		for competency_name, required_min in career.requirements.items():
			total_requirements += 1
			user_score = profile.get_score(competency_name)
			if user_score >= required_min:
				acc_score += 1.0
			else:
				acc_score += max(0.0, user_score / max(1, required_min))
				gaps[competency_name] = max(0, required_min - user_score)

		if total_requirements == 0:
			return 0.0, {}

		percentage = (acc_score / total_requirements) * 100.0
		return percentage, gaps

	def recommend(self, profile: Profile, top_k: int = 3) -> List[Dict]:
		results: List[Dict] = []
		for c in self._careers:
			score, gaps = self.score_profile_for_career(profile, c)
			results.append(
				{
					"career": c,
					"score": round(score, 2),
					"gaps": gaps,
					"learning_paths": self._learning_suggestions(gaps),
				}
			)
		results.sort(key=lambda r: r["score"], reverse=True)
		return results[:top_k]

	def _learning_suggestions(self, gaps: Dict[str, int]) -> Dict[str, List[Tuple[str, str]]]:
		suggestions: Dict[str, List[Tuple[str, str]]] = {}
		for competency_name in gaps.keys():
			if competency_name in LEARNING_PATHS:
				suggestions[competency_name] = LEARNING_PATHS[competency_name]
		return suggestions


def print_header() -> None:
	print("=" * 60)
	print("Orientador de Carreiras - Trabalho do Futuro (CLI)")
	print("=" * 60)


def input_int(prompt: str, min_value: int = 0, max_value: int = 100) -> int:
	while True:
		try:
			value = int(input(prompt).strip())
			if value < min_value or value > max_value:
				print(f"Digite um número entre {min_value} e {max_value}.")
				continue
			return value
		except ValueError:
			print("Entrada inválida. Digite um número inteiro.")


def create_or_edit_profile(current: Profile | None) -> Profile:
	print("\n-- Cadastro/edição de perfil --")
	if current is None:
		name = input("Seu nome: ").strip() or "Pessoa"
		profile = Profile(person_name=name)
	else:
		print(f"Editando perfil de: {current.person_name}")
		profile = current

	print("\nPontue suas competências de 0 a 100.")
	for competency in COMPETENCIES:
		existing = profile.get_score(competency.name)
		prompt = f"- {competency.name} ({competency.kind}) [atual {existing}]: "
		score = input_int(prompt, 0, 100)
		profile.set_score(competency.name, score)

	print("\nPerfil atualizado com sucesso!")
	return profile


def show_recommendations(profile: Profile) -> None:
	print("\n-- Recomendações de Carreira --")
	recommender = Recommender(CAREERS)
	results = recommender.recommend(profile, top_k=5)
	for idx, r in enumerate(results, start=1):
		career = r["career"]
		score = r["score"]
		gaps: Dict[str, int] = r["gaps"]
		print(f"\n{idx}) {career.name} - aderência: {score}%")
		print(f"   {career.description}")
		if gaps:
			print("   Lacunas (pontos a evoluir):")
			for comp, missing in sorted(gaps.items(), key=lambda x: -x[1]):
				print(f"     - {comp}: faltam {missing} pontos")
			paths = r["learning_paths"]
			if paths:
				print("   Trilhas sugeridas:")
				for comp, items in paths.items():
					for title, link in items:
						print(f"     - {comp}: {title} ({link})")
		else:
			print("   Excelente! Você atende aos principais requisitos desta carreira.")


def list_careers() -> None:
	print("\n-- Carreiras disponíveis --")
	for c in CAREERS:
		requires = ", ".join([f"{k}>={v}" for k, v in c.requirements.items()])
		print(f"- {c.name}: {c.description}")
		print(f"  Requisitos: {requires}")


def main() -> None:
	profile: Profile | None = None
	while True:
		print_header()
		print("1) Criar/editar meu perfil")
		print("2) Ver recomendações de carreira")
		print("3) Listar carreiras disponíveis")
		print("0) Sair")
		choice = input("Escolha: ").strip()

		if choice == "1":
			profile = create_or_edit_profile(profile)
			input("\nPressione ENTER para continuar...")
		elif choice == "2":
			if profile is None:
				print("\nCrie seu perfil primeiro (opção 1).")
			else:
				show_recommendations(profile)
			input("\nPressione ENTER para continuar...")
		elif choice == "3":
			list_careers()
			input("\nPressione ENTER para continuar...")
		elif choice == "0":
			print("\nAté logo!")
			break
		else:
			print("\nOpção inválida.")
			input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
	main()

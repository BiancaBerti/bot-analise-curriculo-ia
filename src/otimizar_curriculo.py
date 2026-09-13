import PyPDF2
from openai import OpenAI
import os
from datetime import datetime

# Configuração do cliente local (Ollama)
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

def extrair_texto_pdf(caminho_pdf):
    try:
        with open(caminho_pdf, 'rb') as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            texto = ""
            for pagina in leitor.pages:
                texto += pagina.extract_text() + "\n"
            return texto
    except Exception as e:
        return f"Erro ao ler o PDF: {e}"

def otimizar_para_vaga(texto_curriculo, descricao_vaga):
    prompt = f"""
    Você é um especialista em recrutamento de TI e otimização de currículos para sistemas ATS.
    
    TAREFA:
    Gere uma versão OTIMIZADA do currículo do candidato, adaptada para a vaga descrita abaixo.
    
    REGRAS ABSOLUTAS (VIOLAÇÃO = RESPOSTA INVÁLIDA):
    
    1. FIDELIDADE TOTAL:
       - Use APENAS informações que existem literalmente no currículo original.
       - NÃO mencione tecnologias que NÃO estão no currículo original.
       - NÃO invente projetos, cargos, empresas ou idiomas.
       - NÃO confunda instituições: "Ensino médio" e "Faculdade/Graduação" são coisas diferentes.
    
    2. LINGUAGEM:
       - Escreva APENAS em português brasileiro.
       - NÃO use palavras em inglês (como "Fluent", "Expert", "Senior").
       - NÃO use "especialista", "especializada", "expert", "vasta experiência".
       - Use termos neutros como "Desenvolvedora em formação", "Profissional em transição para TI", "Estudante de".
       - Frases devem fazer sentido gramatical. Revise cada frase antes de escrever.
    
    3. ESTRUTURA OBRIGATÓRIA (exatamente nesta ordem):
       
       # [Nome do Candidato]
       
       ## Resumo Profissional
       [Máximo 3 linhas, começando com "Desenvolvedora em formação" ou "Profissional em transição para TI"]
       
       ## Experiência Profissional
       [Lista de experiências reais do CV com datas no formato "Mês Ano - Mês Ano"]
       
       ## Formação Acadêmica
       [Apenas graduação e ensino médio, com instituição correta]
       
       ## Cursos e Certificações
       [Cursos da Rocketseat e outros]
       
       ## Habilidades Técnicas
       [Lista de tecnologias que APARECEM no CV original]
       
       ## Idiomas
       [Exatamente como está no CV original]
    
    4. FORMATO DE DATAS:
       - Use APENAS: "Mês Ano - Mês Ano" (ex: "Março 2025 - Julho 2025")
       - NÃO use "|" nem "Ativo" nem repita anos
    
    5. PROIBIÇÕES FINAIS:
       - NÃO gere nenhum texto antes do "#" do nome.
       - NÃO gere nenhum texto depois do último idioma.
       - NÃO escreva frases como "Este currículo foi otimizado..." ou "Aqui está o resultado".
       - Sua resposta deve COMEÇAR com "#" e TERMINAR com o último idioma. NADA MAIS.
    
    DESCRIÇÃO DA VAGA:
    {descricao_vaga}
    
    CURRÍCULO ORIGINAL (ÚNICA FONTE VÁLIDA):
    {texto_curriculo[:2500]}
    
    RESPOSTA (comece com "#" e termine no último idioma, sem comentários):
    """
    
    print("🔄 Otimizando seu currículo para esta vaga específica... (pode levar 20-40 segundos)\n")
    
    try:
        resposta = client.chat.completions.create(
            model="qwen2.5:7b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800
        )
        return resposta.choices[0].message.content
    except Exception as e:
        return f"❌ Erro na IA: {e}"


def limpar_resultado_ia(texto_bruto):
    """
    Função de pós-processamento que limpa automaticamente o resultado da IA.
    Remove comentários, formata datas e corrige problemas comuns.
    """
    import re
    
    # Remove blocos de código markdown (```markdown ... ```)
    texto = re.sub(r'```markdown\s*', '', texto_bruto)
    texto = re.sub(r'```\s*', '', texto)
    
    # Remove comentários finais da IA
    linhas = texto.split('\n')
    linhas_limpas = []
    for linha in linhas:
        # Pula linhas que são comentários da IA
        if any(frase in linha.lower() for frase in [
            'este currículo foi otimizado',
            'aqui está o resultado',
            'versão otimizada',
            'de acordo com as instruções'
        ]):
            continue
        linhas_limpas.append(linha)
    
    texto = '\n'.join(linhas_limpas)
    
    # Corrige datas duplicadas (ex: "2025 | 2025" ou "Setembro - 2025 | 2026")
    texto = re.sub(r'(\d{4})\s*\|\s*\1', r'\1', texto)  # Remove ano duplicado
    texto = re.sub(r'\s*\|\s*Ativo', '', texto)  # Remove "Ativo"
    
    # Remove linhas vazias excessivas (mais de 2 seguidas)
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    
    return texto.strip()


if __name__ == "__main__":
    caminho_pdf = "data/curriculo_base.pdf"
    
    vaga_exemplo = """
    Título: Desenvolvedor Python Júnior
    Empresa: Tech Innovators (Exemplo)
    
    Requisitos:
    - Experiência com Python e frameworks web (Flask ou Django)
    - Conhecimento em construção e consumo de APIs REST
    - Familiaridade com controle de versão (Git) e containers (Docker)
    - Noções de testes unitários (Pytest) e boas práticas (SOLID)
    - Boa comunicação e proatividade para resolver problemas
    """
    
    print("📄 Lendo seu currículo base...")
    texto = extrair_texto_pdf(caminho_pdf)
    
    if not texto.startswith("Erro"):
        print("✅ Currículo lido com sucesso!\n")
        
        # Gera a versão otimizada
        curriculo_bruto = otimizar_para_vaga(texto, vaga_exemplo)
        
        # Limpa automaticamente o resultado
        curriculo_otimizado = limpar_resultado_ia(curriculo_bruto)
        
        # Salva o resultado na pasta output/
        os.makedirs("output", exist_ok=True)
        nome_arquivo = f"output/curriculo_otimizado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(curriculo_otimizado)
            
        print("💡 RESULTADO DA OTIMIZAÇÃO (APÓS LIMPEZA AUTOMÁTICA):")
        print("="*60)
        print(curriculo_otimizado)
        print("="*60)
        print(f"\n✅ Arquivo salvo com sucesso em: {nome_arquivo}")
    else:
        print(texto)
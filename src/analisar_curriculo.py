import PyPDF2
from openai import OpenAI

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
    except FileNotFoundError:
        return "Erro: Arquivo 'curriculo_base.pdf' não encontrado na pasta data/."
    except Exception as e:
        return f"Erro ao ler o PDF: {e}"

def analisar_com_ia(texto_curriculo):
    prompt = f"""
    Você é um especialista em recrutamento e sistemas ATS.
    
    Analise o seguinte currículo e me responda em português com:
    1. Um resumo profissional de 2 linhas.
    2. As 5 principais habilidades/palavras-chave identificadas.
    3. Uma sugestão rápida de melhoria para passar em filtros de TI.
    
    Currículo:
    {texto_curriculo[:2000]}
    """
    
    print("🔄 Analisando seu currículo com IA local...\n")
    
    try:
        resposta = client.chat.completions.create(
            model="qwen2.5:3b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return resposta.choices[0].message.content
    except Exception as e:
        return f"❌ Erro na IA: {e}"

if __name__ == "__main__":
    caminho = "data/curriculo_base.pdf"
    
    print("📄 Lendo seu currículo...")
    texto = extrair_texto_pdf(caminho)
    
    # Verifica se NÃO começou com "Erro" E se o texto tem mais de 100 caracteres
    if not texto.startswith("Erro") and len(texto) > 100:
        print("✅ Texto extraído com sucesso!\n")
        resultado = analisar_com_ia(texto)
        print("💡 RESULTADO DA ANÁLISE:")
        print("="*50)
        print(resultado)
        print("="*50)
    else:
        print("⚠️ Falha na leitura do PDF:")
        print(texto)


# 🤖 Bot de Análise e Otimização de Currículo com IA Local

Projeto desenvolvido para automatizar e otimizar a preparação de currículos para processos seletivos de tecnologia. Utiliza Inteligência Artificial rodando **100% localmente** no computador, garantindo total privacidade dos dados do candidato.

## 🎯 Objetivo
Ler um currículo em PDF, extrair seu conteúdo e utilizar um modelo de linguagem local (Qwen via Ollama) para:
1. Analisar compatibilidade com a descrição de uma vaga específica.
2. Reescrever o resumo profissional e reorganizar experiências para destacar palavras-chave do ATS (Applicant Tracking System).
3. Gerar uma versão otimizada em Markdown, pronta para uso.

## 🛠️ Tecnologias Utilizadas
- **Python 3.x**
- **Ollama** (Motor de inferência de IA local)
- **Qwen 2.5 (7B)** (Modelo de linguagem open-source)
- **PyPDF2** (Extração de texto de PDFs)
- **OpenAI Python Library** (Compatibilidade de API com Ollama)
- **Regex (re)** (Pós-processamento e limpeza de dados)

## 🚀 Como Rodar o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/BiancaBerti/bot-analise-curriculo-ia.git
   cd bot-analise-curriculo-ia
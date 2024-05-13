from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

# Gerar dados fictícios
concessionarias = ['Concessionária A', 'Concessionária B', 'Concessionária C']
dados = {'Concessionaria': [], 'Critério A': [], 'Critério B': [], 'Critério C': [], 'Critério D': []}

for concessionaria in concessionarias:
    dados['Concessionaria'].extend([concessionaria] * 12)
    dados['Critério A'].extend([random.choice(['Aprovado', 'Reprovado']) for _ in range(12)])
    dados['Critério B'].extend([random.choice(['Aprovado', 'Reprovado']) for _ in range(12)])
    dados['Critério C'].extend([random.choice(['Aprovado', 'Reprovado']) for _ in range(12)])
    dados['Critério D'].extend([random.choice(['Aprovado', 'Reprovado']) for _ in range(12)])

# Converter para DataFrame
df = pd.DataFrame(dados)

# Função para filtrar os dados por concessionária
def filtrar_por_concessionaria(concessionaria):
    return df[df['Concessionaria'] == concessionaria]

# Função para gerar gráfico de linhas
def gerar_grafico(concessionaria):
    # Gerar dados fictícios para o gráfico
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    desempenho = np.random.rand(12) * 100  # Desempenho fictício entre 0 e 100 para cada mês
    
    # Plotar o gráfico
    plt.figure(figsize=(8, 5))
    plt.plot(meses, desempenho, marker='o', linestyle='-')
    plt.title(f'Evolução do Desempenho ao Longo dos Meses - {concessionaria}')
    plt.xlabel('Mês')
    plt.ylabel('Desempenho')
    plt.grid(True)
    
    # Salvar o gráfico em um buffer de bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    return buffer

# Atualizar a função de gerar relatório PDF para incluir o gráfico
def gerar_relatorio_pdf(concessionaria):
    # Criar documento PDF
    doc = SimpleDocTemplate(f'relatorio_{concessionaria}.pdf', pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Conteúdo do relatório
    conteudo = []
    
    # Adicionar título
    titulo = f'Relatório de Performance para {concessionaria}'
    conteudo.append(Paragraph(titulo, styles['Title']))
    conteudo.append(Spacer(1, 12))
    
    # Adicionar texto do relatório
    texto = f"""Olá {concessionaria},

Aqui está o seu relatório de performance com base nos critérios A a D:

Insira aqui qualquer outra informação relevante, como tabelas de desempenho, etc.

Atenciosamente,
Equipe de Performance
"""
    conteudo.append(Paragraph(texto, styles['Normal']))
    conteudo.append(Spacer(1, 12))
    
    # Adicionar gráfico
    buffer = gerar_grafico(concessionaria)
    img = Image(buffer)
    img.drawWidth = 400  # Ajuste a largura da imagem conforme necessário
    img.drawHeight = 250  # Ajuste a altura da imagem conforme necessário
    conteudo.append(img)
    
    # Adicionar tabela
    dados_concessionaria = filtrar_por_concessionaria(concessionaria)
    dados_para_tabela = [dados_concessionaria.columns.tolist()] + dados_concessionaria.values.tolist()
    tabela = Table(dados_para_tabela)
    tabela.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    conteudo.append(tabela)
    
    # Adicionar conteúdo ao documento
    doc.build(conteudo)

# Gerar relatórios em PDF para cada concessionária
for concessionaria in concessionarias:
    gerar_relatorio_pdf(concessionaria)
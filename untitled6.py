# -*- coding: utf-8 -*-
"""
Created on Wed May  8 13:32:28 2024

@author: erick
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import random

# Gerar dados fictícios
concessionarias = ['Concessionária A', 'Concessionária B', 'Concessionária C']
dados = {'Concessionaria': [], 'Critério A': [], 'Critério B': [], 'Critério C': [], 'Critério D': []}

for concessionaria in concessionarias:
    dados['Concessionaria'].extend([concessionaria] * 10)
    dados['Critério A'].extend([random.choice(['Aprovado', 'Reprovado']) for _ in range(10)])
    dados['Critério B'].extend([random.choice(['Aprovado', 'Reprovado']) for _ in range(10)])
    dados['Critério C'].extend([random.choice(['Aprovado', 'Reprovado']) for _ in range(10)])
    dados['Critério D'].extend([random.choice(['Aprovado', 'Reprovado']) for _ in range(10)])

# Converter para DataFrame
df = pd.DataFrame(dados)

# Função para filtrar os dados por concessionária
def filtrar_por_concessionaria(concessionaria):
    return df[df['Concessionaria'] == concessionaria]

# Função para gerar relatório em PDF
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
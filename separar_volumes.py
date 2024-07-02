import fitz  # PyMuPDF

# Abrir o arquivo PDF original
input_pdf_file = 'volumes.pdf'
pdf_document = fitz.open(input_pdf_file)

# Definição das margens em centímetros, convertidas para pontos (1 cm = 28.35 pontos)
margin_top = 2 * 26
margin_right = 1.25 * 28.35
margin_left = 1.25 * 28.35
margin_bottom = 1.7 * 28.35
margin_vertical = 0.5 * 28.35
margin_horizontal = 0.4 * 28.35

# Coordenadas para cada etiqueta na tabela 3x6
labels_per_row = 3
labels_per_column = 6

# Criar um novo PDF para todas as etiquetas
output_pdf_document = fitz.open()

# Iterar sobre todas as páginas do documento original
for page_num in range(len(pdf_document)):
    page = pdf_document[page_num]

    # Dimensões da página (em pontos)
    page_width = page.rect.width
    page_height = page.rect.height

    # Dimensões da etiqueta, considerando as margens entre as etiquetas
    label_width = (page_width - margin_left - margin_right - (labels_per_row - 1) * margin_horizontal) / labels_per_row
    label_height = (page_height - margin_top - margin_bottom - (labels_per_column - 1) * margin_vertical) / labels_per_column

    # Adicionar uma nova página para cada etiqueta
    for row in range(labels_per_column):
        for col in range(labels_per_row):
            # Calcular as coordenadas da etiqueta, ignorando as margens
            x0 = margin_left + col * (label_width + margin_horizontal)
            y0 = margin_top + row * (label_height + margin_vertical)
            x1 = x0 + label_width
            y1 = y0 + label_height

            # Definir a área de recorte (crop)
            label_rect = fitz.Rect(x0, y0, x1, y1)

            # Criar uma nova página no documento de saída
            new_page = output_pdf_document.new_page(width=label_width, height=label_height)
            new_page.show_pdf_page(new_page.rect, pdf_document, pno=page_num, clip=label_rect)

# Salvar o novo PDF
output_filename = 'volumes-separados.pdf'
output_pdf_document.save(output_filename)
output_pdf_document.close()

pdf_document.close()
print(f'{output_filename} criado com sucesso.')

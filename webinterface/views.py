import csv
import re

from django.http import HttpResponse
from django.shortcuts import render

from .models import Sequence


def validate_fasta(string):
    pattern = r'^>[^\n]+\n[ACGTURYMKSWHBVDN\n]+$'
    match = re.match(pattern, string, re.MULTILINE)
    return bool(match)


def home(request):
    #import_data_from_csv("./Test_file.csv") #Hier den Path zur Daten csv, nur einmal beim aller ersten Start nutzen, dannach wieder rauslöschen
    if request.method == 'POST':
        text_input = request.POST.get('text_input', '')  # Text aus dem Textfeld abrufen
        file_input = request.FILES.get('file_input', None)  # Datei aus dem File-Input abrufen
        species = request.POST.get('species', '')  # Ausgewählte Species abrufen
        threshold = request.POST.get('threshold', '')

        if file_input is None:
            input = text_input
        else:
            input = file_input.read().decode('utf-8')

        split_strings = [s for s in input.split('>') if s.strip()]
        sections = ['>' + s for s in split_strings]  # Eingabe anhand des '>'-Zeichens in Abschnitte aufteilen
        # matcher = [validate_fasta(s) for s in sections]
        # print(matcher)
        # print(matcher.count(True), "Valide Faste Eingaben gefunden!")

        gene_sequences = []  # Liste für Tupel von GeneID und Sequenz

        for section in sections:
            section = section.strip()  # Leerraum am Anfang und Ende des Abschnitts entfernen
            if section:  # Abschnitt darf nicht leer sein
                lines = section.split('\n')  # Abschnitt in Zeilen aufteilen

                gene_id = lines[0].strip()  # Die erste Zeile enthält die GeneID
                sequence = ''.join(lines[1:]).strip()  # Die restlichen Zeilen bilden die Sequenz
                print("GENE_ID", gene_id)
                print("SEQUENCE", sequence)
                print("THRESHOLD", threshold)
                # Datenbankabfrage, um das Value-Feld abzurufen
                queryset = Sequence.objects.filter(species=species, gene_id=gene_id, sequence=sequence)
                print("SET", queryset)
                if queryset.exists():
                    value = queryset.first().value
                    print("VALUE", value)
                else:
                    value = None

                rna_binding = "YES" if value is not None and value > float(threshold) else "NO"

                gene_sequences.append((gene_id, sequence, value, rna_binding))  # Tupel zur Liste hinzufügen

        # Speichere die gene_sequences in der Sitzung
        request.session['gene_sequences'] = gene_sequences

        context = {
            'gene_sequences': gene_sequences,
        }

        return render(request, 'webinterface/home.html', context)

    return render(request, 'webinterface/home.html')


def download_csv(request):
    gene_sequences = request.session.get('gene_sequences', [])

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="gene_sequences.csv"'

    writer = csv.writer(response)
    writer.writerow(['GeneID', 'Sequence', 'Value', 'RNA-binding'])

    for gene_sequence in gene_sequences:
        writer.writerow(gene_sequence)

    return response

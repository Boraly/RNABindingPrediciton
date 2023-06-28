import csv
from webinterface.models import Sequence



def import_data_from_csv(file_path):
    Sequence.objects.all().delete()
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
            species = row.get('Species').strip()  # Verwende get() anstelle von indexing, um KeyErrors zu vermeiden
            gene_id = row.get('GeneID').strip()
            sequence = row.get('Sequence').strip()
            value = float(row.get('Value').strip())  # Konvertiere den Wert in den gewünschten Datentyp (z. B. float)

            # Erstelle ein neues Sequence-Objekt und speichere es in der Datenbank
            sequence_obj = Sequence(species=species, gene_id=gene_id, sequence=sequence, value=value)
            sequence_obj.save()

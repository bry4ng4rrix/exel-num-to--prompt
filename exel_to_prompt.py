import pandas as pd

def generate_phone_search_prompts(input_file, output_file, batch_size=15):
    try:
        # Lire le fichier Excel
        df = pd.read_excel(input_file)
        
        # Vérifier que les colonnes nécessaires existent
        required_columns = ['address1', 'address2', 'address3', 'city', 'postal_code', 'source_id']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Erreur : Colonnes manquantes dans le fichier Excel : {', '.join(missing_columns)}")
            return
        
        # Initialiser les variables pour le traitement par lots
        batch = []
        batch_number = 1
        
        # Ouvrir le fichier de sortie
        with open(output_file, 'w', encoding='utf-8') as f:
            # Parcourir chaque ligne du DataFrame
            for index, row in df.iterrows():
                # Préparer les parties de l'adresse
                address_parts = [
                    str(row['address1']).strip(),
                    str(row['address2']).strip(),
                    str(row['address3']).strip(),
                    str(row['city']).strip(),
                    str(row['postal_code']).strip()
                ]
                
                address_parts = [part for part in address_parts if part and part.lower() != 'nan']
                
                # Créer la chaîne d'adresse
                address = ', '.join(address_parts)
                
                # Ajouter la ligne au lot actuel avec le numéro de ligne (index + 2 car Excel commence à 1 et on ignore l'en-tête)
                line_number = index + 2  # +2 car l'index commence à 0 et on ignore la première ligne (en-tête)
                batch.append(f"trouver un numéros exacte de {address} le source id est {row['source_id']} (ligne Excel: {int(line_number)}) , rechercher dans tous les sites webs;")
                
                # Si le lot est complet, l'écrire dans le fichier
                if len(batch) >= batch_size or index == len(df) - 1:
                    f.write(f"=== Lot {batch_number} ===\n")
                    f.write("\n".join(batch) + "\n\n")
                    batch_number += 1
        
        print(f"Les requêtes ont été générées avec succès dans le fichier : {output_file}")
    
    except FileNotFoundError:
        print(f"Erreur : Le fichier {input_file} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

if __name__ == "__main__":
    input_excel = "exel1.xlsx"  # Remplacez par le nom de votre fichier Excel
    output_txt = "requetes_recherche.txt"
    
    generate_phone_search_prompts(input_excel, output_txt)

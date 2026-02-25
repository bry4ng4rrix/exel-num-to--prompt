import pandas as pd

def generate_phone_search_prompts(input_file, output_file, batch_size=30):
    try:
        df = pd.read_excel(input_file, sheet_name='PAS DE TONAL')

        required_columns = ['source_id', 'address1', 'address2', 'city', 'postal_code', 'FONCTION_RRH', 'phone_number']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f"Erreur : Colonnes manquantes : {', '.join(missing_columns)}")
            return

        batch = []
        batch_number = 1
        global_counter = 1  # 👈 compteur global

        with open(output_file, 'w', encoding='utf-8') as f:
            for index, row in df.iterrows():

                source_id = str(row['source_id']).strip()
                address1 = str(row['address1']).strip()
                address2 = str(row['address2']).strip()
                city = str(row['city']).strip()
                postal_code = str(row['postal_code']).strip()
                fonction_rrh = str(row['FONCTION_RRH']).strip() if 'FONCTION_RRH' in row and pd.notna(row['FONCTION_RRH']) else ''
                phone_number = str(row['phone_number']).strip() if 'phone_number' in row and pd.notna(row['phone_number']) else ''

                line_number = index + 2  # ligne Excel réelle

                address = f"{address1}"
                if address2:
                    address += f", {address2}"
                
                fonction_info = f", fonction : {fonction_rrh}" if fonction_rrh else ""
                
                query = (
                    f"{global_counter}. "
                    f"trouver le numero de telephone de {address1}, {address2}, ville {city} code postale {postal_code}, fonction : {fonction_rrh} autre numero que {phone_number} dans tous les web et ignore les numero qui commence par 08 et 09 ,source_id {source_id}"
                )

                batch.append(query)
                global_counter += 1  # 👈 incrément

                if len(batch) >= batch_size or index == len(df) - 1:
                    f.write(f"=== Lot {batch_number} ===\n")
                    f.write("\n".join(batch) + "\n\n")
                    batch.clear()
                    batch_number += 1

        print(f"✅ Requêtes générées avec succès : {output_file}")

    except FileNotFoundError:
        print(f"❌ Fichier introuvable : {input_file}")
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")


if __name__ == "__main__":
    input_excel = "exel1.xlsx"
    output_txt = "requetes_recherche.txt"
    generate_phone_search_prompts(input_excel, output_txt)

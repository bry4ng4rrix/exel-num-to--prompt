import pandas as pd

def generate_phone_search_prompts(input_file, output_file, batch_size=15):
    try:
        df = pd.read_excel(input_file)

        required_columns = ['RS', 'ADRESSE4', 'VILLE', 'CP', 'ID']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f"Erreur : Colonnes manquantes : {', '.join(missing_columns)}")
            return

        batch = []
        batch_number = 1
        global_counter = 1  # 👈 compteur global

        with open(output_file, 'w', encoding='utf-8') as f:
            for index, row in df.iterrows():

                rs = str(row['RS']).strip()
                adresse = str(row['ADRESSE4']).strip()
                ville = str(row['VILLE']).strip()
                cp = str(row['CP']).strip()
                id_value = str(row['ID']).strip()

                line_number = index + 2  # ligne Excel réelle

                query = (
                    f"{global_counter}. "
                    f"Trouver le numéro de téléphone de {rs}, "
                    f"adresse : {adresse}, "
                    f"ville : {ville}, "
                    f"code postal : {cp}, "
                    f"ID : {id_value} "
                    f"(ligne Excel : {line_number}), "
                    f"rechercher sur tous les sites web."
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

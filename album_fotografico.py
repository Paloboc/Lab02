def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    # TODO
    album = []
    try:
        file = open(file_path, "r", encoding="utf-8")
        next(file, None)  # Salta l'intestazione del file
        for line in file:
            line = line.strip()
            if not line:
                continue
            codice, titolo, autore, mese, anno = line.split(",")
            mese = int(mese)
            anno = int(anno)
            foto = {
                "codice": codice,
                "titolo": titolo,
                "autore": autore,
                "mese": mese,
            }
            for anno_album, foto_anno in album:
                if anno_album == anno:
                    foto_anno.append(foto)
                    break
            else:
                album.append([anno, [foto]])
        file.close()
    except FileNotFoundError:
        print(f"Errore: il file '{file_path}' non è stato trovato.")
        return None
    return album


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    # TODO
    for anno_album, foto_anno in album:
        if anno_album == anno:
            foto_anno.append({
                "codice": codice,
                "titolo": titolo,
                "autore": autore,
                "mese": mese,
            })
            break
    else:
        album.append([anno, [{
            "codice": codice,
            "titolo": titolo,
            "autore": autore,
            "mese": mese,
        }]])
    return album


def cerca_foto(album, codice):
    for anno, foto_anno in album:
        for foto in foto_anno:
            if foto["codice"] == codice:
                return (
                    f'{foto["codice"]}, {foto["titolo"]}, '
                    f'{foto["autore"]}, {foto["mese"]}, {anno}'
                )
    return None

def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # TODO
    titoli = [foto["titolo"] for anno, foto_anno in album if anno == anno for foto in foto_anno]
    if not titoli:
        return None
    return sorted(titoli)

def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()

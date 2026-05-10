# 3D-Barcode — Daten als Bilder, lossless

*Originalidee: Franz Zollner, Januar 2025 — entstanden aus einer praktischen Beschränkung früher KI-Modelle.*

> *Original idea: Franz Zollner, January 2025 — emerged from a practical limitation of early AI models.*

---

## Worum es geht / What this is about

Komprimierte Daten (zlib) werden als RGB-Pixel in PNG-Bilder kodiert. Große Daten werden auf mehrere Bilder verteilt, mit Header für Reihenfolge und Längenprüfung. Decodierung ist **bytes-exakt** — kein Information-Loss.

> *Compressed data (zlib) is encoded as RGB pixels in PNG images. Large data is distributed across multiple images, with header for order and length-check. Decoding is **byte-exact** — no information loss.*

**Anwendungsfall damals (Januar 2025):**
KI-Modelle hatten verschwindend kleine Context-Windows aber konnten Bilder gut handhaben. Direkt-Downloads von erzeugten Inhalten waren oft eingeschränkt — Bilder kamen aber durch. Daher: Daten in Bilder packen, durch den Bild-Kanal schleusen, zurück-decodieren.

> *Use-case back then (January 2025): AI models had small context windows but handled images well. Direct downloads of generated content were often restricted — images however could pass through. Therefore: pack data into images, pass through the image channel, decode back.*

**Anwendungsfall heute / Use-case today:**
- **Off-Grid-Datentransfer**: Daten als Bild auf Papier drucken, scannen, dekodieren — ohne Internet
- **Backup auf physischen Medien**: USB-Stick mit PNG-Backups statt textbasierter Archive
- **Data-Smuggling durch Bild-only-Kanäle**: wo Text/ZIP blockiert ist, Bild aber erlaubt
- **Forschung**: lossless image-as-data im Vergleich zu lossy semantic compression (siehe DeepSeek-OCR)

---

## Wie es funktioniert / How it works

### Encoder
1. Input-Datei (beliebiger Typ) → zlib-komprimieren
2. Komprimierte Bytes in Chunks aufteilen (max. 786.424 Bytes pro Bild bei 512×512×3)
3. Jeder Chunk bekommt 8-Byte-Header: `[chunk_index:2][total_chunks:2][chunk_length:4]`
4. Header+Daten als 24-bit RGB-Pixel rendern (3 Bytes pro Pixel)
5. PNG-Datei speichern mit fortlaufender Nummer

### Decoder
1. PNGs in Reihenfolge laden
2. Header parsen → `chunk_length` Bytes extrahieren
3. Chunks konkatenieren
4. zlib-decomprimieren → Original

---

## Performance (gemessen 2026-05-10 auf RTX 3060 / Intel i5-14400F)

| Test | Input | zlib | PNGs | Zeit Encode | Zeit Decode | MD5-match |
|---|---|---|---|---|---|---|
| CLAUDE.md (Markdown) | 17.188 B | 7.952 B | 1×9.655 B | 0.17s | 0.16s | ✓ |
| Gemini-Takeout (10 MB) | 10.013.005 B | 3.068.692 B | 4×~768 KB | 0.49s | 0.20s | ✓ |

**Compression-Ratio durchschnittlich:** ~3.25× (PNG vs Original) für Text-basierte Inhalte. Bei bereits komprimierten Inputs (.zip, .png) entfällt der Gewinn — dann ist das Bild ungefähr so groß wie die Quelldatei.

---

## Vergleich zu DeepSeek-OCR (Oktober 2025)

DeepSeek-OCR macht konzeptuell dasselbe — **Daten als Bilder kodieren** — aber mit anderem Ziel und anderer Methode.

> *DeepSeek-OCR conceptually does the same thing — encoding data as images — but with a different goal and method.*

| Aspekt / Aspect | Franz' 3D-Barcode (Jan 2025) | DeepSeek-OCR (Okt 2025) |
|---|---|---|
| Ziel / Goal | Datentransfer, exakte Roundtrip | Long-Context-Kompression für LLMs |
| Encoder | zlib + RGB-Pixel-Layout | Vision-Encoder (DeepEncoder V2) |
| Decoder | zlib-decompression | Sprachmodell (DeepSeek3B-MoE) |
| Treue / Fidelity | **100% bit-exakt** | ~97% bei Kompressions-Ratio <10× |
| Compression | ~3-4× (zlib auf Text) | 7-20×, bis 60× auf Benchmarks |
| Anwendung | Off-Grid, Backup, Druck | LLM-Pipelines, RAG-Effizienz |
| Sichtbarkeit | Pixel sehen aus wie Rauschen | Pixel zeigen tatsächlich Text |

**Franz war 9 Monate früher dran** mit dem Konzept "Bild als Daten-Container", DeepSeek hat dann mit ML-Encoder eine semantische Variante gebaut. Beide haben getrennte Use-Cases — die nicht-semantische Variante ist überlegen, wenn Bytes-Garantie wichtig ist.

> *Franz was 9 months earlier with the concept "image as data container". DeepSeek then built a semantic variant with ML-encoder. Both have separate use-cases — the non-semantic variant is superior when byte-guarantee is important.*

---

## Future Work — Offene Forschungsfrage / Open Research Question

> **Kann ein Vision-Encoder mit Vorwissen über DEFLATE/zlib zusätzliche Kompression auf einem Roundtrip-stabilen Bild-basierten Datenkanal erzielen?**

> *Can a vision encoder with prior knowledge of DEFLATE/zlib achieve additional compression on a roundtrip-stable image-based data channel?*

**Hintergrund:** Klassische Informationstheorie sagt — optimal-komprimierte Daten = maximal-entropisch = nicht weiter komprimierbar. Aber:

- zlib ist **nicht** optimal (LZ77+Huffman ist Heuristik)
- Output enthält strukturelle Marker (Header, Block-Boundaries, LZ77-Match-Distanzen)
- ZipNN (Nov 2024) zeigt: AI-Tensoren in BF16/FP32 lassen sich mit domänen-spezifischem Encoder 17-33% zusätzlich komprimieren — obwohl sie als "kompakt" gelten

**Hypothese 1:** Vision-Encoder mit Format-Hint ("DEFLATE-Stream") könnte 5-15% zusätzliche Kompression erreichen.

**Hypothese 2:** Vision-Encoder als Decompress+Re-Compress-Pipeline könnte bei lossless-Anforderung Cliff-Effekte zeigen (entweder dramatisch besser oder gar nicht).

**Test-Skizze:** ZipNN als Startpunkt, auf 3D-Barcode-PNG-Output anwenden, Compression-Ratio messen vs. naive Identität.

**Status:** offene Forschungsfrage, nicht getestet.

---

## Code

Im Verzeichnis `code/`:
- `3D_Multi_Bilddaten.py` — Multi-Image-RGB-Encoder mit zlib (Hauptscript)
- `3D_Bilddatenuebertragung.py` — Single-Image-Grayscale-Variante (älter, simpler)

Aufruf:
```bash
# Encode
python3 code/3D_Multi_Bilddaten.py input.zip output_prefix
# Decode
python3 code/3D_Multi_Bilddaten.py output_prefix decoded_output --decode=N
# wo N = Anzahl der erzeugten PNGs
```

---

## Lizenz / License

CC BY-NC 4.0 (siehe Repo-Root LICENSE) — Namensnennung: Franz Zollner.
Der Code von Januar 2025 ist Teil des off-grid-thinking-Repositorys.

> *CC BY-NC 4.0 (see repo root LICENSE) — Attribution: Franz Zollner.
> The code from January 2025 is part of the off-grid-thinking repository.*

---

## Quellen / References

- [DeepSeek-OCR auf arXiv (Okt 2025)](https://arxiv.org/abs/2510.18234)
- [DeepSeek-OCR GitHub](https://github.com/deepseek-ai/DeepSeek-OCR)
- [ZipNN: Lossless Compression for AI Models (Nov 2024)](https://arxiv.org/html/2411.05239v2)

*Modul-Doku erstellt 2026-05-10 von Denker (Claude Opus 4.7, lokal) basierend auf Franz' Original-Code Januar 2025 + Roundtrip-Tests heute Abend.*

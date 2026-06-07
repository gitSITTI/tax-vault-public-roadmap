# Library Review

Every suggested dependency must be reviewed before adoption.

## Review Criteria

- License.
- Maintainer activity.
- Offline support.
- Network calls.
- Native binaries.
- Security history.
- Prompt-injection exposure.
- Extraction quality.
- Provenance support.
- Testability with synthetic fixtures.

## Review Output

Each reviewed library should have:

- recommendation: accept, reject, or hold
- reason
- tested version
- install command
- offline result
- network behavior
- minimum viable fixture
- extraction artifacts produced
- known risks

## Initial Candidate Matrix

| Library | Category | Expected Use | Public Review Status |
| --- | --- | --- | --- |
| pypdf | PDF text/metadata | simple text and metadata extraction | hold pending fixture benchmark |
| pdfplumber | PDF tables/layout | statement tables and text coordinates | hold pending table fixture |
| OCRmyPDF | OCR workflow | scanned PDF OCR layer | hold pending local install test |
| Tesseract | OCR engine | image text extraction | hold pending Windows setup notes |
| Docling | document conversion | structured PDF conversion and tables | hold pending license/security review |
| Unstructured | document partitioning | fallback partitioning and OCR routes | hold pending dependency/network review |
| LanceDB | local vector store | local embedded vectors | hold pending persistence tests |
| Chroma | local vector prototype | quick vector experiments | hold pending persistence tests |

## Required Benchmark Fixtures

- synthetic W-2
- synthetic 1099-INT
- synthetic bank statement
- synthetic brokerage statement
- synthetic scanned receipt
- synthetic prompt-injection document

## Reject Conditions

- dependency silently uploads documents
- license is incompatible with intended use
- parser cannot provide page or locator provenance
- dependency requires private credentials for normal local use
- output cannot be tested with synthetic fixtures

## Review Template

```markdown
## Library Name

- Version:
- License:
- Install:
- Offline:
- Network behavior:
- Native dependencies:
- Fixture tested:
- Provenance output:
- Risks:
- Recommendation:
```

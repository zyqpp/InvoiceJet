from __future__ import annotations

import unittest

from oracle_invoicejet.taxonomy import classify_document


class TaxonomyTests(unittest.TestCase):
    def test_classifies_screen_document(self) -> None:
        taxonomy = classify_document("InvoiceJet/doc_AI/01_ekrany/E-08_DocumentSeriesComponent/E-08_ekran.md")

        self.assertEqual(taxonomy.source_type, "screen")
        self.assertEqual(taxonomy.screen, "E-08_DocumentSeriesComponent")
        self.assertIn("screen", taxonomy.knowledge_tags)

    def test_classifies_api_endpoint(self) -> None:
        taxonomy = classify_document("InvoiceJet/doc_AI/04_api_i_integracje/01_api_frontend/document_series/GET_DocumentSeries_GetAll.md")

        self.assertEqual(taxonomy.source_type, "api")
        self.assertEqual(taxonomy.entity, "document_series")
        self.assertEqual(taxonomy.endpoint, "GET DocumentSeries/GetAll")

    def test_classifies_db_table(self) -> None:
        taxonomy = classify_document("InvoiceJet/doc_AI/05_model_danych/01_db/dbo/dbo.DocumentSeries.md")

        self.assertEqual(taxonomy.source_type, "data_model")
        self.assertEqual(taxonomy.table, "dbo.DocumentSeries")

    def test_validation_marker_overrides_primary_type(self) -> None:
        taxonomy = classify_document("InvoiceJet/doc_AI/01_ekrany/E-01_LoginComponent/walidacje.md")

        self.assertEqual(taxonomy.source_type, "validation")
        self.assertIn("validation", taxonomy.knowledge_tags)


if __name__ == "__main__":
    unittest.main()

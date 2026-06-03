from __future__ import annotations

import unittest

from oracle_invoicejet.rag import source_path_to_portal_url
from oracle_invoicejet.ui import _rewrite_md_links, build_enriched_source_rows, build_source_links_markdown


DOC_USER = "http://127.0.0.1:8002"
DOC_AI = "http://127.0.0.1:8001"


class PortalLinkTests(unittest.TestCase):
    def test_source_path_to_portal_url_maps_docs_and_readme(self) -> None:
        self.assertEqual(
            source_path_to_portal_url(r"InvoiceJet\doc_user\02_procesy\P-03_konfiguracja_firmy.md", DOC_USER, DOC_AI),
            f"{DOC_USER}/02_procesy/P-03_konfiguracja_firmy.html",
        )
        self.assertEqual(
            source_path_to_portal_url("InvoiceJet/doc_AI/README.md", DOC_USER, DOC_AI),
            f"{DOC_AI}/index.html",
        )
        self.assertEqual(
            source_path_to_portal_url("InvoiceJet/doc_user/01_start/README.md", DOC_USER, DOC_AI),
            f"{DOC_USER}/01_start/index.html",
        )
        self.assertIsNone(source_path_to_portal_url("InvoiceJet/doc_AI/README.md", DOC_USER, ""))
        self.assertIsNone(source_path_to_portal_url("InvoiceJet/doc_user/../doc_AI/README.md", DOC_USER, DOC_AI))
        self.assertIsNone(source_path_to_portal_url("InvoiceJet/docs/README.md", DOC_USER, DOC_AI))

    def test_rewrite_md_links_uses_direct_path_and_source_filename_fallback(self) -> None:
        answer = (
            "Zobacz [proces](InvoiceJet/doc_user/02_procesy/P-03_konfiguracja_firmy.md) "
            "oraz [ekran](E-01_ekran.md)."
        )
        sources = [
            {
                "source_path": r"InvoiceJet\doc_AI\01_ekrany\E-01_LoginComponent\E-01_ekran.md",
            }
        ]

        rewritten = _rewrite_md_links(answer, sources, DOC_USER, DOC_AI)

        self.assertIn(f"[proces]({DOC_USER}/02_procesy/P-03_konfiguracja_firmy.html)", rewritten)
        self.assertIn(f"[ekran]({DOC_AI}/01_ekrany/E-01_LoginComponent/E-01_ekran.html)", rewritten)

    def test_build_enriched_source_rows_puts_portal_first_and_supports_relative_path(self) -> None:
        rows = build_enriched_source_rows(
            [
                {
                    "source_group": "doc_user",
                    "relative_path": "InvoiceJet/doc_user/README.md",
                },
                {
                    "source_group": "other",
                    "relative_path": "InvoiceJet/other/file.md",
                },
            ],
            DOC_USER,
            DOC_AI,
        )

        self.assertEqual(list(rows[0].keys())[0], "portal_url")
        self.assertEqual(rows[0]["portal_url"], f"{DOC_USER}/index.html")
        self.assertEqual(rows[1]["portal_url"], "")

    def test_build_source_links_markdown_returns_visible_links_only_for_portal_sources(self) -> None:
        markdown = build_source_links_markdown(
            [
                {"source_path": "InvoiceJet/doc_AI/README.md"},
                {"source_path": "InvoiceJet/other/file.md"},
            ],
            DOC_USER,
            DOC_AI,
        )

        self.assertEqual(markdown, f"- [InvoiceJet/doc_AI/README.md]({DOC_AI}/index.html)")


if __name__ == "__main__":
    unittest.main()

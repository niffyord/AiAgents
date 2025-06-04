from __future__ import annotations

import asyncio
import time
from datetime import datetime

from rich.console import Console

from agents import Runner, custom_span, gen_trace_id, trace

from .agents.search_agent import search_agent
from .agents.writer_agent import CryptoReport, writer_agent
from .printer import Printer


class CryptoNewsManager:
    def __init__(self, output_path: str | None = None) -> None:
        self.console = Console()
        self.printer = Printer(self.console)
        self.output_path = output_path or "latest_crypto_report.md"

    async def run(self) -> None:
        trace_id = gen_trace_id()
        with trace("Crypto news trace", trace_id=trace_id):
            self.printer.update_item(
                "trace_id",
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}",
                is_done=True,
                hide_checkmark=True,
            )

            self.printer.update_item(
                "starting",
                "Gathering crypto market news...",
                is_done=True,
                hide_checkmark=True,
            )
            search_terms = [
                "latest Ethereum market news",
                "latest Bitcoin market news",
            ]
            search_results = await self._perform_searches(search_terms)
            report = await self._write_report(search_results)

            final_report = f"Report summary\n\n{report.short_summary}"
            self.printer.update_item("final_report", final_report, is_done=True)

            self.printer.end()

        print("\n\n=====REPORT=====\n\n")
        print(f"Report: {report.markdown_report}")
        print("\n\n=====FOLLOW UP QUESTIONS=====\n\n")
        follow_up_questions = "\n".join(report.follow_up_questions)
        print(f"Follow up questions: {follow_up_questions}")

        timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        path = self.output_path.replace("{timestamp}", timestamp)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# Crypto Market Report ({timestamp} UTC)\n\n")
            f.write(report.markdown_report)
            f.write("\n\n## Follow up questions\n")
            f.write("\n".join(f"- {q}" for q in report.follow_up_questions))

    async def _perform_searches(self, search_terms: list[str]) -> list[str]:
        with custom_span("Search the web"):
            self.printer.update_item("searching", "Searching...")
            num_completed = 0
            tasks = [asyncio.create_task(self._search(term)) for term in search_terms]
            results = []
            for task in asyncio.as_completed(tasks):
                result = await task
                if result is not None:
                    results.append(result)
                num_completed += 1
                self.printer.update_item(
                    "searching", f"Searching... {num_completed}/{len(tasks)} completed"
                )
            self.printer.mark_item_done("searching")
            return results

    async def _search(self, term: str) -> str | None:
        input = f"Search term: {term}"
        try:
            result = await Runner.run(search_agent, input)
            return str(result.final_output)
        except Exception:
            return None

    async def _write_report(self, search_results: list[str]) -> CryptoReport:
        self.printer.update_item("writing", "Compiling report...")
        input = f"Search summaries: {search_results}"
        result = Runner.run_streamed(writer_agent, input)
        update_messages = [
            "Compiling report...",
            "Writing analysis...",
            "Finalizing...",
        ]

        last_update = time.time()
        next_message = 0
        async for _ in result.stream_events():
            if time.time() - last_update > 5 and next_message < len(update_messages):
                self.printer.update_item("writing", update_messages[next_message])
                next_message += 1
                last_update = time.time()

        self.printer.mark_item_done("writing")
        return result.final_output_as(CryptoReport)

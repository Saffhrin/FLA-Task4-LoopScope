"""LoopScope: a small, sound termination analyzer for a restricted language."""

from .analyzer import AnalysisResult, Verdict, analyze, parse_program, simulate_fixed_width

__all__ = ["AnalysisResult", "Verdict", "analyze", "parse_program", "simulate_fixed_width"]

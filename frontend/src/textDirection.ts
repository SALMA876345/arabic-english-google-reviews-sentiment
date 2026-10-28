// Lightweight script-detection heuristic for choosing textarea direction.
// Mirrors the character-range approach in src/preprocessing (Python side)
// used for the project's own code-switch analysis -- not a linguistic
// classifier, just enough to pick a sensible dir="rtl"|"ltr" for display.

const ARABIC_RANGE = /[؀-ۿݐ-ݿ]/g;
const LATIN_RANGE = /[A-Za-z]/g;

export function detectDirection(text: string): "rtl" | "ltr" {
  const arabicCount = (text.match(ARABIC_RANGE) ?? []).length;
  const latinCount = (text.match(LATIN_RANGE) ?? []).length;
  if (arabicCount === 0 && latinCount === 0) return "ltr";
  return arabicCount >= latinCount ? "rtl" : "ltr";
}

import { detectDirection } from "../textDirection";

interface ExampleReviewsProps {
  onSelect: (text: string) => void;
  disabled?: boolean;
}

const EXAMPLES: { label: string; text: string }[] = [
  { label: "Arabic · Positive", text: "الخدمة ممتازة والموظفين متعاونين جداً" },
  { label: "Arabic · Negative", text: "الخدمة سيئة جداً ولن أعود مرة أخرى" },
  { label: "Arabic · Neutral", text: "المكان عادي والخدمة مقبولة" },
  { label: "English · Positive", text: "The service was excellent and the staff were very helpful." },
  { label: "English · Negative", text: "Terrible experience. I will never come back." },
  { label: "English · Neutral", text: "The place was okay, nothing special." },
];

export function ExampleReviews({ onSelect, disabled }: ExampleReviewsProps) {
  return (
    <div className="examples">
      <span className="examples__label">Try an example:</span>
      <div className="examples__list">
        {EXAMPLES.map((example) => (
          <button
            key={example.text}
            type="button"
            className="examples__chip"
            dir={detectDirection(example.text)}
            onClick={() => onSelect(example.text)}
            disabled={disabled}
            title="Click to fill the text box (does not run analysis automatically)"
          >
            {example.text}
          </button>
        ))}
      </div>
    </div>
  );
}

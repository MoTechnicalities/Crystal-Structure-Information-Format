# GitHub Release Notes Chooser

Use this file to quickly pick the best release note variant for your audience.

## Quick recommendation

1. General GitHub audience:
   - `GITHUB_RELEASE_NOTES_SNIPPET.md`
2. Investors, sponsors, strategic partners:
   - `GITHUB_RELEASE_NOTES_INVESTOR_VARIANT.md`
3. Media, press, public storytelling:
   - `GITHUB_RELEASE_NOTES_MEDIA_VARIANT.md`
4. Researchers, technical reviewers:
   - `GITHUB_RELEASE_NOTES_RESEARCHER_VARIANT.md`

## Decision matrix

1. If your goal is adoption by contributors, use the general snippet.
2. If your goal is strategic positioning and differentiation framing, use the investor variant.
3. If your goal is broad awareness with clear plain-language narrative, use the media variant.
4. If your goal is methodological credibility and reproducibility scrutiny, use the researcher variant.

## Shared constraints (all variants)

1. Keep mechanism claims separate from external-validity claims.
2. Preserve honest limitation statements.
3. Keep the world-language crystal lobe cluster as roadmap direction, not completed claim.

## Fast publish checklist

1. Select one variant.
2. Confirm links match repository paths.
3. Confirm the sample command still returns `RESULT: PASS`:

python3 release/samples/csif_release_showcase.py

4. Publish release.

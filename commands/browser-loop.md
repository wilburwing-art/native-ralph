---
description: "Start Ralph Loop with browser test validation"
argument-hint: "PROMPT --url URL [--max-iterations N]"
allowed-tools: ["Bash(cd * && npm *:*)", "Bash(npx playwright *:*)", "Read(*)", "Write(*)", "Edit(*)"]
hide-from-slash-command-tool: "true"
---

# Browser Test Loop

Start a Ralph loop that validates front-end changes using Playwright browser tests.

## How It Works

1. You provide a front-end task and target URL
2. Ralph loop runs with browser test validation
3. Each iteration:
   - You make code changes
   - Browser tests run automatically
   - Test results inform next iteration
4. Loop completes when tests pass

## Usage

```bash
/browser-loop "Fix the responsive layout on mobile" --url http://localhost:3000 --max-iterations 15
```

## Setup

First, ensure the dev server is running:
```bash
# In your project
npm run dev
```

Then start the browser loop:
```bash
/browser-loop "TASK DESCRIPTION" --url http://localhost:3000
```

## Validation Commands

During the loop, use these to validate changes:

```bash
# Run all browser tests
cd browser-tests && npx playwright test

# Run specific test file
cd browser-tests && npx playwright test tests/example.spec.js

# Take screenshot for comparison
cd browser-tests && node scripts/screenshot.js http://localhost:3000 ./snapshots/current.png

# Compare against baseline
cd browser-tests && node scripts/validate.js ./snapshots/baseline.png ./snapshots/current.png
```

## Example Prompts

### Fix Layout Bug
```
/browser-loop "The navigation menu overlaps content on mobile. Fix the CSS so menu displays correctly. Run browser tests to validate. Output <promise>LAYOUT FIXED</promise> when tests pass." --url http://localhost:3000 --max-iterations 10
```

### Implement Feature
```
/browser-loop "Add a dark mode toggle to the header. It should: 1) Toggle body class 'dark', 2) Persist preference in localStorage, 3) Pass accessibility tests. Output <promise>DARK MODE COMPLETE</promise> when done." --url http://localhost:3000 --max-iterations 20
```

### Visual Regression Fix
```
/browser-loop "The homepage layout regressed. Compare current screenshot against baseline, identify differences, and fix until visual diff is under 0.1%. Output <promise>VISUAL MATCH</promise> when validated." --url http://localhost:3000 --max-iterations 15
```

## Test-Driven Front-End Development

1. Write failing Playwright test in `browser-tests/tests/`
2. Start browser loop targeting that test
3. Ralph iterates until test passes

```javascript
// browser-tests/tests/feature.spec.js
test('dark mode toggle works', async ({ page }) => {
    await page.goto('/');
    await page.click('[data-testid="dark-mode-toggle"]');
    await expect(page.locator('body')).toHaveClass(/dark/);
});
```

```bash
/browser-loop "Implement dark mode toggle to pass the test in browser-tests/tests/feature.spec.js" --url http://localhost:3000 --max-iterations 15
```

# Browser Tests for Ralph Loop

Playwright-based browser testing framework for front-end iteration in Ralph loops.

## Setup

```bash
cd browser-tests
npm install
npx playwright install chromium
```

## Usage

### Run Tests

```bash
# All tests
npm test

# With UI
npm run test:ui

# Headed mode (see browser)
npm run test:headed

# Debug mode
npm run test:debug
```

### Screenshot Utilities

```bash
# Take screenshot
node scripts/screenshot.js http://localhost:3000 ./snapshots/current.png

# Compare images
node scripts/validate.js ./snapshots/baseline.png ./snapshots/current.png
```

## Ralph Loop Integration

Use `/browser-loop` command for front-end iteration:

```bash
/browser-loop "Fix mobile layout" --url http://localhost:3000 --max-iterations 15
```

Or combine with standard `/ralph-loop`:

```bash
/ralph-loop "Fix the CSS bug. After each change, run: cd browser-tests && npm test. Output <promise>TESTS PASS</promise> when all tests green." --max-iterations 20
```

## Writing Tests

Add tests in `tests/` directory:

```javascript
// tests/my-feature.spec.js
const { test, expect } = require('@playwright/test');

test('feature works', async ({ page }) => {
    await page.goto('/');
    await page.click('#my-button');
    await expect(page.locator('#result')).toBeVisible();
});
```

## Visual Regression

Tests can compare screenshots:

```javascript
test('matches snapshot', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveScreenshot('page.png', {
        maxDiffPixels: 100,
    });
});
```

Baseline images stored in `tests/*.spec.js-snapshots/`.

## Configuration

Edit `playwright.config.js` to change:
- `baseURL` - Target server (default: http://localhost:3000)
- `viewport` - Browser dimensions
- `reporter` - Output format

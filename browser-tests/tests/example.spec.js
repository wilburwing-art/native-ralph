// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * Example browser tests for Ralph Loop front-end iteration
 *
 * These tests demonstrate patterns useful in Ralph loops:
 * - Visual regression testing
 * - Functional validation
 * - Accessibility checks
 *
 * Ralph Loop usage:
 *   /ralph-loop "Fix the homepage layout. Tests must pass. <promise>TESTS PASS</promise>" --max-iterations 20
 *
 * Then iterate on the front-end code until these tests pass.
 */

test.describe('Homepage', () => {
    test('has correct title', async ({ page }) => {
        await page.goto('/');
        await expect(page).toHaveTitle(/./);  // Has any title
    });

    test('renders main content', async ({ page }) => {
        await page.goto('/');
        // Wait for page to be interactive
        await page.waitForLoadState('domcontentloaded');

        // Check that body has content
        const body = page.locator('body');
        await expect(body).toBeVisible();
    });

    test('no console errors', async ({ page }) => {
        const errors = [];
        page.on('console', msg => {
            if (msg.type() === 'error') {
                errors.push(msg.text());
            }
        });

        await page.goto('/');
        await page.waitForLoadState('networkidle');

        expect(errors).toHaveLength(0);
    });

    test('responsive layout', async ({ page }) => {
        // Test mobile viewport
        await page.setViewportSize({ width: 375, height: 667 });
        await page.goto('/');
        await expect(page.locator('body')).toBeVisible();

        // Test tablet viewport
        await page.setViewportSize({ width: 768, height: 1024 });
        await page.goto('/');
        await expect(page.locator('body')).toBeVisible();

        // Test desktop viewport
        await page.setViewportSize({ width: 1920, height: 1080 });
        await page.goto('/');
        await expect(page.locator('body')).toBeVisible();
    });
});

test.describe('Visual Regression', () => {
    test('homepage matches snapshot', async ({ page }) => {
        await page.goto('/');
        await page.waitForLoadState('networkidle');

        // Take screenshot for comparison
        await expect(page).toHaveScreenshot('homepage.png', {
            maxDiffPixels: 100,
        });
    });
});

test.describe('Accessibility', () => {
    test('has no detectable a11y issues', async ({ page }) => {
        await page.goto('/');

        // Basic accessibility checks
        // Check for alt text on images
        const images = page.locator('img');
        const imageCount = await images.count();

        for (let i = 0; i < imageCount; i++) {
            const img = images.nth(i);
            const alt = await img.getAttribute('alt');
            // Images should have alt attribute (can be empty for decorative)
            expect(alt).not.toBeNull();
        }

        // Check for form labels
        const inputs = page.locator('input:not([type="hidden"])');
        const inputCount = await inputs.count();

        for (let i = 0; i < inputCount; i++) {
            const input = inputs.nth(i);
            const id = await input.getAttribute('id');
            const ariaLabel = await input.getAttribute('aria-label');
            const ariaLabelledBy = await input.getAttribute('aria-labelledby');

            // Input should have either a label, aria-label, or aria-labelledby
            const hasLabel = id ? await page.locator(`label[for="${id}"]`).count() > 0 : false;
            expect(hasLabel || ariaLabel || ariaLabelledBy).toBeTruthy();
        }
    });
});

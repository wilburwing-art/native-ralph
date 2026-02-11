#!/usr/bin/env node

/**
 * Screenshot utility for Ralph Loop browser testing
 *
 * Takes a screenshot of a URL and saves it for comparison.
 * Used in Ralph loops to validate visual changes.
 *
 * Usage:
 *   node scripts/screenshot.js <url> <output-path>
 *   node scripts/screenshot.js http://localhost:3000 ./snapshots/home.png
 */

const { chromium } = require('@playwright/test');
const path = require('path');

async function takeScreenshot(url, outputPath) {
    const browser = await chromium.launch();
    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 }
    });
    const page = await context.newPage();

    try {
        await page.goto(url, { waitUntil: 'networkidle' });
        await page.screenshot({
            path: outputPath,
            fullPage: false
        });
        console.log(`Screenshot saved: ${outputPath}`);
    } catch (error) {
        console.error(`Failed to capture screenshot: ${error.message}`);
        process.exit(1);
    } finally {
        await browser.close();
    }
}

const args = process.argv.slice(2);
if (args.length < 2) {
    console.log('Usage: node screenshot.js <url> <output-path>');
    console.log('Example: node screenshot.js http://localhost:3000 ./snapshots/home.png');
    process.exit(1);
}

takeScreenshot(args[0], args[1]);

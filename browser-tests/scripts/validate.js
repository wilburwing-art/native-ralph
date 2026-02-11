#!/usr/bin/env node

/**
 * Visual validation utility for Ralph Loop
 *
 * Compares two screenshots and reports differences.
 * Returns exit code 0 if images match (within threshold), 1 if different.
 *
 * Usage:
 *   node scripts/validate.js <baseline> <current> [threshold]
 *   node scripts/validate.js ./snapshots/baseline.png ./snapshots/current.png 0.1
 */

const fs = require('fs');
const { PNG } = require('pngjs');
const pixelmatch = require('pixelmatch');
const path = require('path');

async function compareImages(baselinePath, currentPath, threshold = 0.1) {
    if (!fs.existsSync(baselinePath)) {
        console.log(`Baseline not found: ${baselinePath}`);
        console.log('Creating baseline from current image...');
        fs.copyFileSync(currentPath, baselinePath);
        console.log(`Baseline created: ${baselinePath}`);
        return { match: true, diffPercent: 0 };
    }

    const baseline = PNG.sync.read(fs.readFileSync(baselinePath));
    const current = PNG.sync.read(fs.readFileSync(currentPath));

    if (baseline.width !== current.width || baseline.height !== current.height) {
        console.log('Image dimensions differ');
        console.log(`Baseline: ${baseline.width}x${baseline.height}`);
        console.log(`Current: ${current.width}x${current.height}`);
        return { match: false, diffPercent: 100 };
    }

    const { width, height } = baseline;
    const diff = new PNG({ width, height });

    const numDiffPixels = pixelmatch(
        baseline.data,
        current.data,
        diff.data,
        width,
        height,
        { threshold: 0.1 }
    );

    const totalPixels = width * height;
    const diffPercent = (numDiffPixels / totalPixels) * 100;

    // Save diff image
    const diffPath = currentPath.replace('.png', '-diff.png');
    fs.writeFileSync(diffPath, PNG.sync.write(diff));

    const match = diffPercent <= threshold;

    console.log(`Pixels compared: ${totalPixels}`);
    console.log(`Pixels different: ${numDiffPixels}`);
    console.log(`Difference: ${diffPercent.toFixed(2)}%`);
    console.log(`Threshold: ${threshold}%`);
    console.log(`Result: ${match ? 'PASS' : 'FAIL'}`);

    if (!match) {
        console.log(`Diff image saved: ${diffPath}`);
    }

    return { match, diffPercent, diffPath };
}

const args = process.argv.slice(2);
if (args.length < 2) {
    console.log('Usage: node validate.js <baseline> <current> [threshold]');
    console.log('Example: node validate.js ./snapshots/baseline.png ./snapshots/current.png 0.1');
    process.exit(1);
}

const threshold = args[2] ? parseFloat(args[2]) : 0.1;

compareImages(args[0], args[1], threshold)
    .then(result => {
        process.exit(result.match ? 0 : 1);
    })
    .catch(err => {
        console.error(err);
        process.exit(1);
    });

const fs = require('fs');
const path = require('path');

function resolveNodeRunner() {
  const nvmrcPath = path.join(__dirname, '.nvmrc');

  if (!fs.existsSync(nvmrcPath)) {
    return 'node';
  }

  const version = fs.readFileSync(nvmrcPath, 'utf8').trim().replace(/^v/, '');
  const home = process.env.HOME || process.env.USERPROFILE;

  if (!home) {
    return 'node';
  }

  const nvmDir = path.join(home, '.nvm', 'versions', 'node');
  const exact = path.join(nvmDir, `v${version}`, 'bin', 'node');

  if (fs.existsSync(exact)) {
    return exact;
  }

  if (fs.existsSync(nvmDir)) {
    const matches = fs
      .readdirSync(nvmDir)
      .filter((entry) => entry.startsWith(`v${version}`))
      .sort()
      .reverse();

    if (matches.length > 0) {
      const candidate = path.join(nvmDir, matches[0], 'bin', 'node');
      if (fs.existsSync(candidate)) {
        return candidate;
      }
    }
  }

  return 'node';
}

module.exports = () => ({
  autoDetect: ['node:test'],
  env: {
    runner: resolveNodeRunner(),
  },
});

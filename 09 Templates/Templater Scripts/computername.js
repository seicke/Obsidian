module.exports = () => {
    const os = require('os');
    if (process.platform === 'darwin') {
        try {
            return require('child_process').execSync('scutil --get ComputerName').toString().trim();
        } catch (e) {
            return os.hostname();
        }
    }
    return os.hostname();
};
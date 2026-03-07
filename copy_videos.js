const fs = require('fs');
const path = require('path');

const srcDir = "/Users/leishi/Library/Mobile Documents/com~apple~CloudDocs/02_HBS_finance/hbsvideo/Module_2";
const destDir = "hbs_tutor_app/www/hbsvideo/Module_2";

if (!fs.existsSync(destDir)){
    fs.mkdirSync(destDir, { recursive: true });
}

fs.readdir(srcDir, (err, files) => {
    if (err) {
        console.error("Could not list the directory.", err);
        process.exit(1);
    }

    files.forEach((file, index) => {
        if (!file.endsWith('.mp4')) return;
        
        const srcPath = path.join(srcDir, file);
        const destPath = path.join(destDir, file);

        try {
            // Using copyFileSync which typically uses read/write syscalls
            fs.copyFileSync(srcPath, destPath);
            console.log(`Copied ${index + 1}/${files.length}: ${file}`);
        } catch (e) {
            console.error(`Error copying ${file}:`, e.message);
        }
    });
});

/**
 * Local dev server that emulates Vercel URL rewriting from vercel.json
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const vercelConfig = JSON.parse(fs.readFileSync(path.join(__dirname, 'vercel.json'), 'utf8'));

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css':  'text/css',
  '.js':   'application/javascript',
  '.json': 'application/json',
  '.svg':  'image/svg+xml',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.ico':  'image/x-icon',
};

function matchRewrite(url) {
  for (const rule of vercelConfig.rewrites) {
    const pattern = rule.source
      .replace(/\//g, '\\/')
      .replace(/\(\.\*\)/g, '(.*)');
    const re = new RegExp('^' + pattern + '$');
    if (re.test(url)) return rule.destination;
  }
  return null;
}

const server = http.createServer((req, res) => {
  let urlPath = req.url.split('?')[0];
  const destination = matchRewrite(urlPath);
  const filePath = path.join(__dirname, destination || urlPath);

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('404 Not Found');
      return;
    }
    const ext = path.extname(filePath);
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
    res.end(data);
  });
});

const PORT = process.env.PORT || 8766;
server.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));

# 部署 / Deployment

`npm run build` 生成纯静态站点 `dist/`，可以放到任何静态托管（Nginx、Cloudflare Pages、Vercel、GitHub Pages）。

## 子路径

```bash
ATLAS_BASE=/words/ npm run build
```

## Nginx 示例

```nginx
location ^~ /words/ {
    alias /var/www/word-atlas/;
    try_files $uri $uri/ /words/index.html;
    expires 7d;
}
```

## Vercel（Origin）

源码以 Cursor Origin 为准，不要为了托管再镜像到 GitHub。私有 Origin 仓库只能从 **Vercel Pro 或 Enterprise** 部署，Hobby 团队不行。

1. 在 Vercel 新建项目，选 **Continue with Origin**，连上拥有 `master-luo` 的 Origin 团队，导入 `toefl-atlas`。也可以在仓库的 Apps 里安装 Vercel。
2. 框架预设 Vite。安装用 `npm ci`（有 lockfile 时 Vercel 会自动做），构建命令 `npm run build`，输出目录 `dist`。`vercel.json` 已写好这些设置，并把非媒体路径回退到 `index.html`。应用路由是 hash（`#/atlas`），刷新子页面不依赖服务端路由。
3. 部署完成后，URL 只出现在该 Vercel 项目的 Deployments 页，形如 `https://<project>.vercel.app`。不要猜域名。
4. 若不想让链接被随便打开：在 Pro 项目的 Deployment Protection 里打开 Vercel Authentication。

本机构建产物约 389 MB、2.2 万个文件。命令行匿名部署会撞上 15,000 文件上限；接到 Git 后由 Vercel 构建，不受这条 CLI 限制。

## 体积

插画与音频合计约数百 MB。`dist/` 会原样带上 `public/` 里的图和录音。

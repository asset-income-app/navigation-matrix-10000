# Wrangler批量部署脚本
# 使用方法: .\deploy_batch.ps1

# 检查Wrangler
if (-not (Get-Command wrangler -ErrorAction SilentlyContinue)) {
    Write-Host "安装Wrangler..."
    npm install -g wrangler
}

# 登录Cloudflare
Write-Host "登录Cloudflare..."
wrangler login

# 部署超级总站
Write-Host "部署超级总站..."
wrangler pages deploy 03-central-hub --project-name daohangbaike-nav

# 部署城市站
Write-Host "部署城市站..."
Get-ChildItem -Directory 02-sites\cities | ForEach-Object {
    $name = $_.Name
    Write-Host "部署: $name"
    wrangler pages deploy "02-sites\cities\$name" --project-name "$name-nav"
}

# 部署行业站
Write-Host "部署行业站..."
Get-ChildItem -Directory 02-sites\niches | ForEach-Object {
    $name = $_.Name
    Write-Host "部署: $name"
    wrangler pages deploy "02-sites\niches\$name" --project-name "$name-nav"
}

# 部署组合站
Write-Host "部署组合站..."
Get-ChildItem -Directory 02-sites\hybrids | ForEach-Object {
    $name = $_.Name
    Write-Host "部署: $name"
    wrangler pages deploy "02-sites\hybrids\$name" --project-name "$name-nav"
}

Write-Host "部署完成!"

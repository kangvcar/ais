# Docker Hub 发布配置指南

为了让GitHub Actions能够自动构建和发布Docker镜像到Docker Hub，需要配置以下GitHub Secrets。

## 🔐 必需的GitHub Secrets

在GitHub仓库的 `Settings > Secrets and variables > Actions` 中添加以下secrets：

### DOCKERHUB_USERNAME
- **值**: 你的Docker Hub用户名
- **示例**: `kangvcar`

### DOCKERHUB_TOKEN
- **值**: Docker Hub访问令牌（推荐使用访问令牌而不是密码）
- **获取方式**:
  1. 登录 [Docker Hub](https://hub.docker.com/)
  2. 点击右上角头像 > Account Settings
  3. 在左侧菜单选择 "Security"
  4. 点击 "New Access Token"
  5. 输入令牌描述（如 "GitHub Actions for AIS"）
  6. 选择权限：`Read, Write, Delete`（或根据需要选择）
  7. 点击 "Generate" 并复制生成的令牌

## 📝 配置步骤

1. **在GitHub仓库中配置Secrets**:
   ```
   仓库 > Settings > Secrets and variables > Actions > New repository secret
   ```

2. **添加DOCKERHUB_USERNAME**:
   - Name: `DOCKERHUB_USERNAME`
   - Secret: `your-dockerhub-username`

3. **添加DOCKERHUB_TOKEN**:
   - Name: `DOCKERHUB_TOKEN`
   - Secret: `your-dockerhub-access-token`

## 🏷️ Docker镜像命名

当前配置使用的Docker镜像名称是：`kangvcar/ais`

如果你想使用不同的镜像名称，需要修改 `.github/workflows/docker.yml` 文件中的：
```yaml
env:
  REGISTRY: docker.io
  IMAGE_NAME: your-username/your-image-name
```

## 🚀 触发构建

配置完成后，以下操作会自动触发Docker镜像构建：

- **推送到main分支** - 构建并推送 `latest` 标签
- **发布新版本** - 构建并推送版本标签（如 `v1.0.0`）
- **手动触发** - 通过GitHub Actions UI手动运行

## 🔍 验证配置

1. 推送代码到main分支
2. 查看GitHub Actions的"Docker Build and Push"工作流
3. 确认构建成功完成
4. 在Docker Hub检查镜像是否正确推送

## 🔒 安全注意事项

- ✅ 使用访问令牌而不是密码
- ✅ 为访问令牌设置适当的权限（最小权限原则）
- ✅ 定期轮换访问令牌
- ✅ 不要在代码中硬编码凭据

## 🐳 Docker Hub仓库设置

建议在Docker Hub上：

1. **设置仓库描述**（会被CI自动更新）
2. **配置README**（会从GitHub同步）
3. **设置仓库为公开**（便于用户使用）
4. **添加适当的标签**：如 `ai`, `terminal`, `assistant`, `cli`

## 🆘 故障排除

如果构建失败，检查：

1. **Secrets配置是否正确**
2. **Docker Hub用户名和令牌是否有效**
3. **镜像名称是否与Docker Hub仓库匹配**
4. **GitHub Actions日志中的错误信息**

---

配置完成后，你的项目将拥有完全自动化的Docker镜像构建和发布流程！🎉
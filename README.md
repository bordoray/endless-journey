## 開発サーバーの起動

```sh
# backend
docker compose up -d

# frontend
cd frontend

# FastAPIのURL
cat - >.env <<EOF
BACKEND_URL="http://localhost:8000"
EOF

pnpm install
pnpm dev
```

- FastAPIおよびPostgreSQLはdocker-composeで起動します
- SvelteKitアプリケーションはpnpm devで起動します（非コンテナ環境）

### Prismaスキーマの変更時

```sh
# サーバーは起動した状態で
DATABASE_URL=postgres://user:password@localhost:5432/postgres uv run prisma migrate dev
```

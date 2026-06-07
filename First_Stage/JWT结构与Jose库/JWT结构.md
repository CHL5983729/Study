# JWT结构

## 1.什么是JWT

JWT(JSON Web Token)是一种开放标准,用于在各方之间以JSON对象的形式安全的传输信息。通常用于身份认证和信息交换。JWT是自包含的,令牌本身携带了所有的必要信息

## 2.JWT的结构

一个JWT由三部分用.(点号)连接组成

```JWT
Header.Payload.Signature
例如:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c 
```

## 2.1 Header(头部)

Header通常包括两部分:令牌类型(typ)和签名算法(alg)

```json
{
"alg":"HS256",  # 签名算法，例如 HS256（HMAC SHA-256）、RS256（RSA SHA-256）、ES256（ECDSA）等
"typ":"JWT"     # 固定为 "JWT"，表示这是一个 JWT。
}
```

可选字段:**cty**:内容类型,当JWT嵌套时使用  **kid**:密钥ID,用于JWK集(多密钥场景)

## 2.2 Payload(载荷)

payload是存放声明(Claims)的地方,声明有三种类型

### 1：注册声明(Registered Claims)

预定义的，非强制但推荐使用，以提供互操作性。常见的有：

- `iss` (Issuer)：签发者
- `sub` (Subject)：主题（通常为用户 ID）
- `aud` (Audience)：接收方
- `exp` (Expiration Time)：过期时间（Unix 时间戳）
- `nbf` (Not Before)：生效时间
- `iat` (Issued At)：签发时间
- `jti` (JWT ID)：唯一标识

### 2：公共声明(Public Claims)

在 IANA JSON Web Token Claims 注册表中定义的，或使用 URI 避免冲突的名称。

### 3：私有声明(Private Claims)

双方约定的自定义字段。

Payload 也是 Base64URL 编码，但**注意**：Payload 是明文（可解码），所以不要放敏感信息！

示例 Payload：

```json
{
 "sub": "1234567890",
 "name": "John Doe",
 "admin": true,
 "iat": 1516239022,
 "exp": 1516242622
}
```

## 2.3 Signature(签名)

签名用于验证消息在传输过程中未被篡改，并且对于使用私钥签名的令牌，还可以验证发送方的身份。

签名生成方式：

```text
signature = HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

如果使用非对称算法（如 RS256），则私钥签名，公钥验证。

最终的 JWT 格式：

```text
base64UrlEncode(header) + "." + base64UrlEncode(payload) + "." + signature
```

## 3.为什么用 Base64URL 而不是普通 Base64？

- **Base64URL** 将 `+` 替换为 `-`，`/` 替换为 `_`，并移除末尾的 `=`。
- 这样 JWT 可以直接放入 URL 或 Header（如 `Authorization: Bearer <token>`）而无需额外编码。

## 4.常见加密算法

| 算法            | 类型  | 说明                                     |
| ------------- | --- | -------------------------------------- |
| HS256         | 对称  | HMAC with SHA-256，使用同一个密钥签名和验证         |
| HS384         | 对称  | HMAC SHA-384                           |
| HS512         | 对称  | HMAC SHA-512                           |
| RS256         | 非对称 | RSA PKCS#1 v1.5 with SHA-256，私钥签名，公钥验证 |
| RS384 / RS512 | 非对称 | 同上，位数更高                                |
| ES256         | 非对称 | ECDSA using P-256 and SHA-256          |
| EdDSA         | 非对称 | 使用 Ed25519 等（RFC 8037）                 |
| none          | 无   | 不签名（不安全，仅用于调试）                         |

**推荐**：生产环境中尽可能使用非对称算法（RS256、ES256），对称算法（HS256）适合内部单一信任域。

## 5.JWT 的失效处理

- 服务端验证 `exp` 和 `nbf`。
- `exp` 必须大于当前时间（UTC），否则拒绝。
- 为了安全，`exp` 不应设置过长（例如几小时或几天）。
- 如果需要即时使令牌失效（登出），可以通过黑名单（Redis）或短令牌 + 刷新令牌模式。

## 6.安全注意事项

1. **不要在 Payload 中存储密码、密钥等明文敏感信息**。
2. **总是验证签名**，并防止算法混淆攻击（例如将 `none` 算法改为自己的算法）。
3. **使用 HTTPS 传输**，防止令牌被窃听。
4. **选择合适的过期时间**。
5. **秘密/私钥要保管好**，避免泄露。
6. **固定算法**，不要接受客户端动态指定的算法。

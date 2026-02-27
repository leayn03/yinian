# 数据更新说明

## 📁 数据文件

- **主数据文件**: `omikuji/data/senso-ji-fortunes-full.json`
  - 包含完整的 100 个浅草寺签文数据
  - 格式：`id`, `level`, `poem`, `interpretation`, `lineInterpretations`

## 🔄 更新数据

### 从修正后的 Gemini 数据更新

```bash
python3 update_from_gemini_direct.py
```

**源文件**: `omikuji/data/senso-gemini.txt`

**目标文件**: `omikuji/data/senso-ji-fortunes-full.json`

### 更新内容

每次更新会同步：
- 签级 (level)
- 签诗 (poem)
- 逐句解释 (lineInterpretations)
- 现代解读 (interpretation)

### 签级分布

当前签级分布（100 签）：
- 吉: 35 个
- 凶: 29 个
- 大吉: 19 个
- 末吉: 7 个
- 小吉: 5 个
- 半吉: 3 个
- 末小吉: 2 个

---

**最后更新**: 2026-02-27

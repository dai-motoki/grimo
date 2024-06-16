# クラス: Claude

## 属性
```python.Claude
import anthropic

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
```

## 関数
```python.Claude

message = client.messages.create(
    model=model,
    max_tokens=1000,
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": text
        }
    ]
)
translated_text = message.content[0].text

```

# クラス: Claude3（Claude）
## 属性
    model="claude-3-opus-20240229"
    model="claude-3-sonnet-20240229"
    model="claude-3-haiku-20240307"

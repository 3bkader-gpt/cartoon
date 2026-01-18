# عرض الجودات المتعددة - Multi Download Server

## كيف يعمل النظام

### السيناريو 1: صفحة تحتوي على Multi Download Server

عندما تجد الصفحة رابط "تحميل متعدد" أو رابط يحتوي على `haxloppd` أو `premilkyway`:

**المدخل:**
```json
{
  "url": "https://haxloppd.com/file/abc123",
  "server": "تحميل متعدد",
  "type": "server"
}
```

**المخرج (من MultiServerExtractor):**
```json
{
  "sources": [
    {
      "url": "https://premilkyway.com/video_1080p.mp4",
      "quality": "1080p",
      "server": "Multi (2.5 GB)",
      "type": "direct",
      "metadata": {"size": "2.5 GB"}
    },
    {
      "url": "https://premilkyway.com/video_720p.mp4",
      "quality": "720p",
      "server": "Multi (1.2 GB)",
      "type": "direct",
      "metadata": {"size": "1.2 GB"}
    },
    {
      "url": "https://premilkyway.com/video_480p.mp4",
      "quality": "480p",
      "server": "Multi (800 MB)",
      "type": "direct",
      "metadata": {"size": "800 MB"}
    },
    {
      "url": "https://premilkyway.com/video_360p.mp4",
      "quality": "360p",
      "server": "Multi (400 MB)",
      "type": "direct",
      "metadata": {"size": "400 MB"}
    }
  ]
}
```

### السيناريو 2: صفحة تحتوي على Forafile فقط

**المدخل:**
```json
{
  "url": "https://forafile.com/file123.html",
  "server": "Forafile",
  "type": "server"
}
```

**المخرج (من ForafileExtractor):**
```json
{
  "sources": [
    {
      "url": "https://cdn.example.com/video.mp4",
      "quality": "Auto",
      "server": "Forafile",
      "type": "direct"
    }
  ]
}
```

## مثال من صفحة The Witcher

بناءً على فحص الصفحة:
- **URL**: `https://x7k9f.sbs/episode/...the-witcher.../`
- **السيرفر الموجود**: Forafile فقط
- **النتيجة المتوقعة**: جودة واحدة (Auto)

### إذا كانت الصفحة تحتوي على Multi Download:

**قبل الاستخراج:**
```
1. تحميل متعدد (Multi Download)
```

**بعد الاستخراج:**
```
1. Multi Server - 1080p (2.5 GB) ⭐
2. Multi Server - 720p (1.2 GB) ⭐
3. Multi Server - 480p (800 MB) ⭐
4. Multi Server - 360p (400 MB) ⭐
```

## كيف يظهر في Frontend

```jsx
// Frontend سيستقبل:
{
  "video_url": "https://...", // أول رابط (1080p إذا موجود)
  "sources": [
    { "url": "...", "quality": "1080p", "server": "Multi (2.5 GB)" },
    { "url": "...", "quality": "720p", "server": "Multi (1.2 GB)" },
    { "url": "...", "quality": "480p", "server": "Multi (800 MB)" },
    { "url": "...", "quality": "360p", "server": "Multi (400 MB)" }
  ]
}

// Frontend يعرض:
<QualitySelector>
  <Option quality="1080p" size="2.5 GB" />
  <Option quality="720p" size="1.2 GB" />
  <Option quality="480p" size="800 MB" />
  <Option quality="360p" size="400 MB" />
</QualitySelector>
```

## ملاحظات

1. **Multi Download Server** هو الوحيد الذي يدعم جودات متعددة حالياً
2. **Forafile, Uqload** وغيرها تعطي جودة واحدة فقط
3. النظام يكتشف تلقائياً إذا كان السيرفر يدعم جودات متعددة
4. إذا لم يتم العثور على جودات، يتم استخدام `GenericExtractor` الذي يحاول استخراج رابط واحد

## التحسينات المستقبلية

- إضافة دعم جودات متعددة لسيرفرات أخرى (إذا كانت تدعمها)
- تحسين استخراج حجم الملف
- إضافة خيار "اختر الجودة المفضلة" في الـ API


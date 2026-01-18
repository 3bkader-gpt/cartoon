# قائمة السيرفرات المتاحة في EgyDead

هذا الملف يوثق السيرفرات التي تم اكتشافها في موقع EgyDead والتي تحتاج إلى extractors.

## السيرفرات المكتشفة من الكود

من خلال فحص الكود في `backend/sites/egydead/scraper.py`، تم اكتشاف السيرفرات التالية:

### 1. Forafile ✅ (مكتمل)
- **الحالة**: تم التنفيذ في Phase 1
- **الملف**: `backend/extractors/servers/forafile.py`
- **النمط**: `forafile`, `forafile.com`
- **الملاحظات**: يحتاج إلى التعامل مع overlay و popup

### 2. Foupix
- **الحالة**: مذكور في الكود لكن لم يتم التنفيذ
- **النمط**: `foupix`
- **الملاحظات**: مشابه لـ Forafile

### 3. Uqload
- **الحالة**: مذكور في الكود لكن لم يتم التنفيذ  
- **النمط**: `uqload`
- **الملاحظات**: عادة يحتاج إلى النقر على overlay الفيديو

## السيرفرات المخططة (من الخطة الأصلية)

### Phase 2 (الأولوية العالية)

1. **Uqload** - شائع، عادة يحتاج إلى النقر على overlay الفيديو
2. **DoodStream** - إعلانات كثيرة، redirects
3. **VidBom/VidShare** - سيرفرات شائعة

### Phase 4 (السيرفرات الإضافية)

4. **Vidoza** - مذكور في الكود
5. **Uptobox** - إذا كان متاحاً، عادة له وقت انتظار
6. **StreamTape** - سيرفر شائع
7. **MixDrop** - سيرفر streaming
8. **GoFile/MediaFire** - أسهل (عادة روابط مباشرة)

## كيفية إضافة سيرفر جديد

1. أنشئ ملف جديد في `backend/extractors/servers/` مثل `newserver.py`
2. ورث من `BaseExtractor`
3. نفذ دالة `extract(url) -> Dict[str, Any]`
4. سجل السيرفر في `backend/extractors/factory.py` في `_registry`

مثال:
```python
# backend/extractors/servers/newserver.py
from ..base import BaseExtractor

class NewServerExtractor(BaseExtractor):
    def extract(self, url: str) -> Dict[str, Any]:
        # Implementation here
        pass
```

ثم في `factory.py`:
```python
_registry = {
    "forafile": ForafileExtractor,
    "newserver": NewServerExtractor,  # Add here
}
```

## سيرفرات تدعم جودات متعددة ⭐

### Multi Download Server (تحميل متعدد)

**الحالة**: مكتشف في الكود المرجعي - يحتاج إلى تنفيذ

**الميزات**:
- ✅ يدعم جودات متعددة:
  - Full HD (1080p)
  - HD (720p)
  - SD (480p/360p)
  - Low Quality
- ✅ يسمح باختيار الجودة المفضلة
- ✅ يعرض حجم الملف لكل جودة

**النمط/الدومين**:
- اسم السيرفر: "تحميل متعدد" أو "Multi Download"
- Domains: `haxloppd.com`, `premilkyway` (في الروابط النهائية)
- CDN links: تحتوي على "cdn" في الرابط

**كيفية العمل** (من `temp/egydead_ref/main.py`):
1. الانتقال إلى رابط "تحميل متعدد"
2. البحث عن خيارات الجودة باستخدام selectors:
   - `text=Full HD quality`
   - `text=HD quality`
   - `text=SD quality`
   - `text=Low quality`
3. إذا لم يتم العثور تلقائياً، البحث عن زر "Download File" أو "Create Download Link"
4. بناء روابط الجودة يدوياً إذا لزم الأمر: `{base_domain}/f/{file_id}_h` (1080p), `_n` (720p)
5. جلب حجم الملف لكل جودة
6. السماح للمستخدم باختيار الجودة المفضلة
7. النقر على زر التحميل للحصول على الرابط النهائي

**الأولوية**: عالية جداً - سيرفر مهم يدعم جودات متعددة

**ملاحظات التنفيذ**:
- يحتاج إلى extractor خاص يدعم اختيار الجودة
- يمكن إرجاع قائمة بجميع الجودات المتاحة بدلاً من رابط واحد
- يجب دعم معامل `quality_preference` في دالة `extract()`

## ملاحظات

- السيرفرات يتم اكتشافها تلقائياً من خلال `ExtractorFactory.needs_extraction()`
- إذا لم يتم العثور على extractor محدد، يتم استخدام `GenericExtractor`
- جميع السيرفرات تستفيد من:
  - Ad blocking تلقائي
  - Popup handling تلقائي
  - Common video extraction patterns

